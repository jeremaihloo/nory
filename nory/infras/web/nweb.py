import inspect
import logging
from aiohttp import web
import asyncio

from aiohttp.web import Application

from nory.infras.envs.configs import Environment
from nory.infras.exts import features
from nory.infras.exts.managers import ExtensionManager
from nory.infras.exts.models import ExtensionLoader
from nory.infras.web.helper import beautify_http_method
from nory.infras.web.models import WebOptions
from nory.infras.web.req import RequestHandler
from nory.infras.web.module_features import JinJa2, Statics
from nory.infras.di import di

class Nory(object):
    def __init__(self, name, root_path):
        self.env = Environment(name, root_path)

        self.logger = logging.getLogger('nory')
        self.ext_manager = None  # type: ExtensionManager

        self.web_options = WebOptions()
        self.web_options = self.env.configuration.option('web', self.web_options)

        self.middlewares = []
        self.module_features = []

    def use_ext_manager(self, paths):
        self.ext_manager = ExtensionManager(self.env, ExtensionLoader(self.env, paths))

    def use_middlewares(self, middlewares):
        if not isinstance(middlewares, list):
            middlewares = [middlewares]
        self.middlewares.extend(middlewares)

    def use_module_features(self, ms):
        if not isinstance(ms, list):
            ms = [ms]
        self.module_features.extend(ms)

    def add_route(self, app, fn):
        method = getattr(fn, '__method__', None)
        path = getattr(fn, '__route__', None)
        if path is None or not isinstance(path, str) or method is None or not isinstance(method, str):
            raise ValueError('@get or @post not defined in %s.' % str(fn))
        if not asyncio.iscoroutinefunction(fn) and not inspect.isgeneratorfunction(fn):
            fn = asyncio.coroutine(fn)
        self.logger.info(
            '[add route] [%s] %s => %s(%s)' % (
                beautify_http_method(method), path, fn.__name__,
                ', '.join(inspect.signature(fn).parameters.keys())))
        app.router.add_route(method, path, RequestHandler(app, fn))

        for item in app.app_manager.get_worked_features(features.__FEATURE_ADD_ROUTE__):
            params = [x for x in inspect.signature(fn).parameters.keys()]
            item(method, path, params)

    def add_routes(self, app: Application, app_manager: ExtensionManager):
        routes = app_manager.get_worked_features(features.__FEATURE_ROUTING__)
        self.logger.info('routes {}'.format(routes))
        for item in routes:
            self.add_route(app, item)

    async def use(self, module, app, _logger: logging.Logger, _ext_manager: ExtensionManager, env: Environment):

        m = module()
        m.initialize(app, _logger, _ext_manager, env)

    def run(self):
        loop = asyncio.get_event_loop()
        self.app = web.Application(loop=loop, middlewares=self.middlewares)
        loop.run_until_complete(self._build(self.app))

        web.run_app(self.app, **self.web_options)

    async def _build(self, app: Application):
        self.app.di = di
        self.env.configuration.option('web', self.web_options)

        self.ext_manager.app = app
        await self.ext_manager.load_extensions()

        app.app_manager = self.ext_manager

        await self.use(JinJa2, app, self.logger, self.ext_manager, self.env)
        await self.use(Statics, app, self.logger, self.ext_manager, self.env)

        self.add_routes(app, self.ext_manager)
