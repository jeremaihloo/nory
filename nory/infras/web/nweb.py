import inspect
import logging
from aiohttp import web
import asyncio
from jinja2 import Environment, FileSystemLoader
from nory.infras import constants
from nory.infras.exts import features
from nory.infras.exts.managers import ExtensionManager
from nory.infras.web.middlewares import logger_factory, auth_factory, data_factory, response_factory
from nory.infras.web.models import Jinja2Options, WebOptions
from nory.infras.web.req import RequestHandler
import os



class NoryWebService(object):

    def __init__(self, _logger: logging.Logger,
                 _ext_manager: ExtensionManager,
                 _jinja2_options: Jinja2Options,
                 _web_options: WebOptions):
        self._logger = _logger
        self._ext_manager = _ext_manager
        self._jinja2_options = _jinja2_options
        self._web_options = _web_options

    def init_jinja2(self, app, **kw):
        self._logger.info('[init jinja2] ...')
        options = dict(
            autoescape=kw.get('autoescape', True),
            block_start_string=kw.get('block_start_string', '{%'),
            block_end_string=kw.get('block_end_string', '%}'),
            variable_start_string=kw.get('variable_start_string', '{{'),
            variable_end_string=kw.get('variable_end_string', '}}'),
            auto_reload=kw.get('auto_reload', True)
        )
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'extensions')
        self._logger.info('[init_jinja2] set jinja2 template path: %s' % path)

        env = Environment(loader=FileSystemLoader(path), **options)
        filters = self._ext_manager.get_worked_features(features.__FEATURE_TEMPLATE_FILTER__)
        if filters is not None:
            for f in filters:
                env.filters[getattr(f, constants.FEATURE_NAME)] = f
        app['__templating__'] = env

    def add_statics(self, app):
        for item in self._ext_manager.extensions.values():
            if not item.info.enabled:
                continue

            for k in item.info.static.keys():
                path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'extensions', item.info.name,
                                    item.info.static[k])
                try:
                    self.add_static(app, os.path.join(item.info.name, k), path)
                except Exception as e:
                    self._logger.warning('[add_statics] add app [{}] static error'.format(item.info.name))

    def add_route(self, app, fn):
        method = getattr(fn, '__method__', None)
        path = getattr(fn, '__route__', None)
        if path is None or not isinstance(path, str) or method is None or not isinstance(method, str):
            raise ValueError('@get or @post not defined in %s.' % str(fn))
        if not asyncio.iscoroutinefunction(fn) and not inspect.isgeneratorfunction(fn):
            fn = asyncio.coroutine(fn)
        logging.info(
            '[add route] [%s] %s => %s(%s)' % (
                self.beautify_http_method(method), path, fn.__name__,
                ', '.join(inspect.signature(fn).parameters.keys())))
        app.router.add_route(method, path, RequestHandler(app, fn))

        for item in app.app_manager.get_worked_features(features.__FEATURE_ADD_ROUTE__):
            params = [x for x in inspect.signature(fn).parameters.keys()]
            item(method, path, params)

    def beautify_http_method(self, method: str):
        return method.ljust(6, ' ')

    def add_routes(self, app, app_manager: ExtensionManager):
        for item in app_manager.get_worked_features(features.__FEATURE_ROUTING__):
            self.add_route(app, item)

    def add_static(self, app, app_name, path):
        # path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
        if not os.path.exists(path):
            raise Exception('add static error dir not exists : {}'.format(path))
        app.router.add_static('/extensions/' + app_name, path)
        logging.info('add static %s => %s' % ('/extensions/' + app_name, path))

    async def init(self, loop):
        app = web.Application(loop=loop, middlewares=[
            logger_factory, auth_factory, data_factory, response_factory
        ])

        await self._ext_manager.load_extensions()

        app.app_manager = self._ext_manager

        self.init_jinja2(app, **self._jinja2_options)

        self.add_routes(app, self._ext_manager)

        self.add_statics(app)

        srv = await loop.create_server(app.make_handler(), self._web_options.host, self._web_options.port)

        self._logger.info('server started at http://{}:{}...'.format(self._web_options.host, self._web_options.port))
        return srv
