import logging
from collections import OrderedDict

from aiohttp import web
from jinja2 import Environment, FileSystemLoader

from nory.infras import constants
from nory.infras.envs.models import Configuration
from nory.infras.exts import features
from nory.infras.exts.managers import ExtensionManager
from nory.infras.utils import json_dumps
from nory.infras.web.coros import add_static, add_routes
from nory.infras.web.models import Jinja2Options, WebOptions

import os


async def logger_factory(app, handler):
    l = logging.getLogger('logger_factory')

    async def logger(request):
        l.info('[logger_factory] Request: %s %s' % (request.method, request.path))
        # await asyncio.sleep(0.3)
        return await handler(request)

    return logger


async def auth_factory(app, handler):
    logger = logging.getLogger('auth_factory')

    async def auth(request):
        request.__user__ = None
        logger.info('auth user: %s %s' % (request.method, request.path))
        flag = False
        logger.info(
            '[auth_provider] : {}'.format(app.app_manager.get_worked_features(features.__FEATURE_AUTHING__)))
        for fn in app.app_manager.get_worked_features(features.__FEATURE_AUTHING__):
            auth_flag, msg = await fn(app, request)
            if auth_flag:
                logger.info('[auth] : [{}] passed'.format(getattr(fn, constants.FEATURE_NAME)))
                flag = True
            else:
                logger.info('[auth] : [{}] un_pass'.format(getattr(fn, constants.FEATURE_NAME)))

        if not flag:
            for fn in app.app_manager.get_worked_features(features.__FEATURE_AUTH_FALSE__):
                await fn(app, request)
        return await handler(request)

    return auth


def api_response(r, status_code=200):
    resp = web.Response(status=status_code, body=json_dumps(api_response_body(r)))
    resp.content_type = 'application/json;charset=utf-8'
    return resp


def api_response_body(r, status_code=200):
    o = OrderedDict()
    o['ok'] = True if status_code == 200 else False
    o['body'] = r if r is not None else ('everything is ok !' if status_code == 200 else 'got something bad !')
    return o


async def response_factory(app, handler):
    logger = logging.getLogger('response_factory')

    async def response(request):
        logger.info('Response handler...')
        r = await handler(request)
        logger.info('response is instance of [{}]'.format(type(r)))
        if isinstance(r, web.StreamResponse):
            return r

        if isinstance(r, bytes):
            resp = web.Response(body=r)
            resp.content_type = 'application/octet-stream'
            return resp

        if isinstance(r, str):
            if r.startswith('redirect:'):
                return web.HTTPFound(r[9:])
            resp = web.Response(body=r.encode('utf-8'))
            resp.content_type = 'text/html;charset=utf-8'
            return resp

        if isinstance(r, dict):
            template = r.get('__template__')
            if template is None:
                return api_response(r)
            else:
                r['__user__'] = request.__user__
                resp = web.Response(body=app['__templating__'].get_template(template).render(**r).encode('utf-8'))
                resp.content_type = 'text/html;charset=utf-8'
                return resp

        if isinstance(r, int) and 100 <= r < 600:
            return api_response(None, status_code=r)

        if isinstance(r, list):
            return api_response(r)

        if isinstance(r, tuple) and len(r) == 2:
            t, m = r
            if isinstance(t, int) and 100 <= t < 600:
                return api_response(m, status_code=t)

        # default:
        resp = web.Response(body=str(r).encode('utf-8'))
        resp.content_type = 'text/plain;charset=utf-8'
        return resp

    return response


async def data_factory(app, handler):
    logger = logging.getLogger('data_factory')

    async def parse_data(request):
        if request.method == 'POST':
            if request.content_type.startswith('application/json'):
                request.__data__ = await request.json()
                logger.info('request json: %s' % str(request.__data__))
            elif request.content_type.startswith('application/x-nory-form-urlencoded'):
                request.__data__ = await request.post()
                logger.info('request form: %s' % str(request.__data__))
        return await handler(request)

        return parse_data


class NoryWebService(object):

    def __init__(self, _logger: logging.Logger,
                 _app_manager: ExtensionManager,
                 _jinja2_options: Jinja2Options,
                 _web_options: WebOptions):
        self._logger = _logger
        self._app_manager = _app_manager
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
        filters = self._app_manager.get_worked_features(features.__FEATURE_TEMPLATE_FILTER__)
        if filters is not None:
            for f in filters:
                env.filters[getattr(f, constants.FEATURE_NAME)] = f
        app['__templating__'] = env

    # @web.middleware
    # async def error_middleware(request, handler):
    #     try:
    #         response = await handler(request)
    #         if response.status == 404:
    #             return api_response(response.message, 404)
    #         return response
    #     except web.HTTPException as ex:
    #         if ex.status == 404:
    #             return api_response(ex.reason, 404)
    #         raise

    def add_apps_statics(self, app):
        for item in self._app_manager.extensions.values():
            if not item.info.enabled:
                continue

            for k in item.info.static.keys():
                path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'extensions', item.info.name,
                                    item.info.static[k])
                try:
                    add_static(app, os.path.join(item.info.name, k), path)
                except Exception as e:
                    self._logger.warning('[add_apps_statics] add app [{}] static error'.format(item.info.name))

    async def init(self, loop):
        app = web.Application(loop=loop, middlewares=[
            logger_factory, auth_factory, data_factory, response_factory
        ])

        # await self._app_manager.load_extensions()
        assert isinstance(self._jinja2_options, Configuration)

        self.init_jinja2(app, **self._jinja2_options)

        add_routes(app, self._app_manager)

        self.add_apps_statics(app)

        srv = await loop.create_server(app.make_handler(), self._web_options.host, self._web_options.port)

        self._logger.info('server started at http://{}:{}...'.format(self._web_options.host, self._web_options.port))
        return srv
