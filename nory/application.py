#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import signal

import coloredlogs, logging
# from infras.envs.config_loaders import load_configs
#
# configs = load_configs()
#
# from infras.environments.models import NcmsConfig
#
# if NcmsConfig.colored_log:
#     coloredlogs.install(level=NcmsConfig.log_level)
# else:
#     logging.basicConfig(level=NcmsConfig.log_level)
#
# logging.info('[environments] {}'.format(configs))

from collections import OrderedDict

import envtypes
from infras.exts.coros import AppManager
from aiohttp import web
from jinja2 import Environment, FileSystemLoader
from infras.web.coros import add_routes, add_static
from infras import utils, constants
from infras.exts import features
import asyncio, os
from infras.envs.models import Environment as NoryEnvironment


def init_jinja2(app, **kw):
    logging.info('[init jinja2] ...')
    options = dict(
        autoescape=kw.get('autoescape', True),
        block_start_string=kw.get('block_start_string', '{%'),
        block_end_string=kw.get('block_end_string', '%}'),
        variable_start_string=kw.get('variable_start_string', '{{'),
        variable_end_string=kw.get('variable_end_string', '}}'),
        auto_reload=kw.get('auto_reload', True)
    )
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'extensions')
    logging.info('[init_jinja2] set jinja2 template path: %s' % path)

    env = Environment(loader=FileSystemLoader(path), **options)
    filters = app.app_manager.get_worked_features(features.__FEATURE_TEMPLATE_FILTER__)
    if filters is not None:
        for f in filters:
            env.filters[getattr(f, constants.FEATURE_NAME)] = f
    app['__templating__'] = env


async def logger_factory(app, handler):
    async def logger(request):
        logging.info('[logger_factory] Request: %s %s' % (request.method, request.path))
        # await asyncio.sleep(0.3)
        return await handler(request)

    return logger


async def auth_factory(app, handler):
    async def auth(request):
        request.__user__ = None
        logging.info('auth user: %s %s' % (request.method, request.path))
        flag = False
        logging.info(
            '[auth_provider] : {}'.format(app.app_manager.get_worked_features(features.__FEATURE_AUTHING__)))
        for fn in app.app_manager.get_worked_features(features.__FEATURE_AUTHING__):
            auth_flag, msg = await fn(app, request)
            if auth_flag:
                logging.info('[auth] : [{}] passed'.format(getattr(fn, constants.FEATURE_NAME)))
                flag = True
            else:
                logging.info('[auth] : [{}] un_pass'.format(getattr(fn, constants.FEATURE_NAME)))

        if not flag:
            for fn in app.app_manager.get_worked_features(features.__FEATURE_AUTH_FALSE__):
                await fn(app, request)
        return await handler(request)

    return auth


async def data_factory(app, handler):
    async def parse_data(request):
        if request.method == 'POST':
            if request.content_type.startswith('application/json'):
                request.__data__ = await request.json()
                logging.info('request json: %s' % str(request.__data__))
            elif request.content_type.startswith('application/x-nory-form-urlencoded'):
                request.__data__ = await request.post()
                logging.info('request form: %s' % str(request.__data__))
        return await handler(request)

        return parse_data


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


def api_response(r, status_code=200):
    resp = web.Response(status=status_code, body=utils.json_dumps(api_response_body(r)))
    resp.content_type = 'application/json;charset=utf-8'
    return resp


def api_response_body(r, status_code=200):
    o = OrderedDict()
    o['ok'] = True if status_code == 200 else False
    o['body'] = r if r is not None else ('everything is ok !' if status_code == 200 else 'got something bad !')
    return o


async def response_factory(app, handler):
    async def response(request):
        logging.info('Response handler...')
        r = await handler(request)
        logging.info('response is instance of [{}]'.format(type(r)))
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


def add_apps_statics(app):
    for item in app.app_manager.apps.values():
        if not item.info.enabled:
            continue

        for k in item.info.static.keys():
            path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'extensions', item.info.name,
                                item.info.static[k])
            try:
                add_static(app, os.path.join(item.info.name, k), path)
            except Exception as e:
                logging.warning('[add_apps_statics] add app [{}] static error'.format(item.info.name))


async def init(loop):
    app = web.Application(loop=loop, middlewares=[
        logger_factory, auth_factory, response_factory
    ])

    app_manager = AppManager(app)
    await app_manager.load_apps()
    app.app_manager = app_manager

    init_jinja2(app)
    add_routes(app)

    add_apps_statics(app)

    srv = await loop.create_server(app.make_handler(), '0.0.0.0', 9000)

    logging.info('server started at http://0.0.0.0:9000...')
    return srv


class Nory(object):
    def __init__(self, env: NoryEnvironment):
        self.running = False
        self.env = env

    def run(self):
        if self.running:
            return

        self.running = True

        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(init(self.loop))

    def shutdown(self):
        if not self.running:
            pass

        self.loop.stop()
        self.running = False


class NoryHost(object):

    def __init__(self, name='nory'):
        self.name = name
        self.env = NoryEnvironment(name)

    def set_env_mode_from_sys_env(self):
        mode = os.environ.get('mode', envtypes.Development)
        self.env.mode = mode

    def add_config_from_file(self, filename):
        pass

    def build(self):
        n = Nory(self.env)
        return n

    def start(self, gracefull=False):
        pass


def graceful(env: NoryEnvironment):
    n = Nory(env)

    def onSigInt(signo, frame):
        print('Shutdown...')
        n.shutdown()

    def onSigTerm(signo, frame):
        print('Shutdown...')
        n.shutdown()

    def onSigKill(signo, frame):
        print('Shutdown...')
        n.shutdown()

    signal.signal(signal.SIGINT, onSigInt)
    signal.signal(signal.SIGTERM, onSigTerm)

    return n
