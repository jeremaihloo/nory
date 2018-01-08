#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import coloredlogs, logging

import utils
from configs import NcmsConfig, __configs__

if NcmsConfig.colored_log:
    coloredlogs.install(level=NcmsConfig.log_level)
else:
    logging.basicConfig(level=NcmsConfig.log_level)

logging.info('[configs] {}'.format(__configs__))

from collections import OrderedDict
from app_cores import AppManager
from utils import singleton
from aiohttp import web
from jinja2 import Environment, FileSystemLoader
from coroweb import add_routes, add_static
import events
import asyncio, os, json


def init_jinja2(app, **kw):
    logging.info('init jinja2...')
    options = dict(
        autoescape=kw.get('autoescape', True),
        block_start_string=kw.get('block_start_string', '{%'),
        block_end_string=kw.get('block_end_string', '%}'),
        variable_start_string=kw.get('variable_start_string', '{{'),
        variable_end_string=kw.get('variable_end_string', '}}'),
        auto_reload=kw.get('auto_reload', True)
    )
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'apps')
    logging.info('set jinja2 template path: %s' % path)

    env = Environment(loader=FileSystemLoader(path), **options)
    filters = app.plugin_manager.__features__[events.__FEATURE_TEMPLATE_FILTER__]
    if filters is not None:
        for f in filters:
            env.filters[getattr(f, '__app_fn_name__')] = f
    app['__templating__'] = env


async def logger_factory(app, handler):
    async def logger(request):
        logging.info('Request: %s %s' % (request.method, request.path))
        # await asyncio.sleep(0.3)
        return (await handler(request))

    return logger


async def auth_factory(app, handler):
    async def auth(request):
        request.__user__ = None
        logging.info('auth user: %s %s' % (request.method, request.path))
        flag = False
        logging.info('[auth_provider] : [{}]'.format(app.plugin_manager.__features__[events.__FEATURE_AUTHING__]))
        for fn in app.plugin_manager.__features__[events.__FEATURE_AUTHING__]:
            auth_flag, msg = await fn(app, request)
            if auth_flag:
                logging.info('[auth] : [{}] passed'.format(getattr(fn, '__app_fn_name__')))
                flag = True
            else:
                logging.info('[auth] : [{}] un_pass'.format(getattr(fn, '__app_fn_name__')))

        if not flag:
            for fn in app.plugin_manager.__features__.get(events.__FEATURE_AUTH_FALSE__, []):
                await fn(app, request)
        return await handler(request)

    return auth


async def data_factory(app, handler):
    async def parse_data(request):
        if request.method == 'POST':
            if request.content_type.startswith('application/json'):
                request.__data__ = await request.json()
                logging.info('request json: %s' % str(request.__data__))
            elif request.content_type.startswith('application/x-www-form-urlencoded'):
                request.__data__ = await request.post()
                logging.info('request form: %s' % str(request.__data__))
        return (await handler(request))

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

        if isinstance(r, int) and r >= 100 and r < 600:
            return api_response(None, status_code=r)

        if isinstance(r, list):
            return api_response(r)

        if isinstance(r, tuple) and len(r) == 2:
            t, m = r
            if isinstance(t, int) and t >= 100 and t < 600:
                return api_response(m, status_code=t)

        # default:
        resp = web.Response(body=str(r ).encode('utf-8'))
        resp.content_type = 'text/plain;charset=utf-8'
        return resp

    return response


async def init(loop):
    app = web.Application(loop=loop, middlewares=[
        logger_factory, auth_factory, response_factory
    ])

    plugin_manager = AppManager(app)
    await plugin_manager.load_apps()
    app.plugin_manager = plugin_manager

    init_jinja2(app)
    add_routes(app)

    for item in app.plugin_manager.__apps__:

        for k in item.static.keys():
            path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'apps', item.name, item.static[k])
            try:
                add_static(app, os.path.join(item.name, k), path)
            except Exception as e:
                logging.warning(str(e))

    srv = await loop.create_server(app.make_handler(), '0.0.0.0', 9000)

    logging.info('server started at http://0.0.0.0:9000...')
    return srv


@singleton
class NCMS(object):
    def __init__(self):
        self.running = False

    def run(self):
        if self.running:
            return

        self.running = True

        loop = asyncio.get_event_loop()
        loop.run_until_complete(init(loop))
        loop.run_forever()


def run():
    n = NCMS()
    n.run()


if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt:
        logging.info('ncms close by keyboard inerrupt')
