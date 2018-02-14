import inspect
import logging
from aiohttp import web
import asyncio
from nory.infras.exts import features
from nory.infras.exts.managers import ExtensionManager
from nory.infras.web.helper import beautify_http_method
from nory.infras.web.middlewares import logger_factory, auth_factory, data_factory, response_factory
from nory.infras.web.models import Jinja2Options, WebOptions
from nory.infras.web.req import RequestHandler
from nory.infras.web.uses import JinJa2, Statics


class NoryWebService(object):

    def __init__(self, _logger: logging.Logger,
                 _ext_manager: ExtensionManager,
                 _jinja2_options: Jinja2Options,
                 _web_options: WebOptions):
        self._logger = _logger
        self._ext_manager = _ext_manager
        self._web_options = _web_options
        self._jinja2_options = _jinja2_options

    def add_route(self, app, fn):
        method = getattr(fn, '__method__', None)
        path = getattr(fn, '__route__', None)
        if path is None or not isinstance(path, str) or method is None or not isinstance(method, str):
            raise ValueError('@get or @post not defined in %s.' % str(fn))
        if not asyncio.iscoroutinefunction(fn) and not inspect.isgeneratorfunction(fn):
            fn = asyncio.coroutine(fn)
        logging.info(
            '[add route] [%s] %s => %s(%s)' % (
                beautify_http_method(method), path, fn.__name__,
                ', '.join(inspect.signature(fn).parameters.keys())))
        app.router.add_route(method, path, RequestHandler(app, fn))

        for item in app.app_manager.get_worked_features(features.__FEATURE_ADD_ROUTE__):
            params = [x for x in inspect.signature(fn).parameters.keys()]
            item(method, path, params)

    def add_routes(self, app, app_manager: ExtensionManager):
        routes = app_manager.get_worked_features(features.__FEATURE_ROUTING__)
        self._logger.info('routes {}'.format(routes))
        for item in routes:
            self.add_route(app, item)

    async def use(self, module, app, _logger: logging.Logger, _ext_manager: ExtensionManager, **kwargs):

        m = module()
        m.initialize(app, _logger, _ext_manager, **kwargs)

    async def init(self, loop):
        app = web.Application(loop=loop, middlewares=[
            logger_factory, auth_factory, data_factory, response_factory
        ])

        await self._ext_manager.load_extensions()

        app.app_manager = self._ext_manager

        await self.use(JinJa2, app, self._logger, self._ext_manager, **self._jinja2_options)
        await self.use(Statics, app, self._logger, self._ext_manager, **dict())

        self.add_routes(app, self._ext_manager)

        srv = await loop.create_server(app.make_handler(), self._web_options.host, self._web_options.port)

        self._logger.info('server started at http://{}:{}...'.format(self._web_options.host, self._web_options.port))
        return srv
