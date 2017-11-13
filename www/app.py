#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from collections import OrderedDict

import app_cores
from app_cores import AppManager

__author__ = 'Michael Liao'

'''
async web application.
'''

import logging

logging.basicConfig(level=logging.INFO)

from migrations import MigrationBuilder, MigrationRecord, db_localsystem_migrations

import asyncio, os, json, time
from datetime import datetime

from aiohttp import web
from jinja2 import Environment, FileSystemLoader

from config import configs

import orm
from coroweb import add_routes, add_static


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
    filters = app.plugin_manager.__app_fns__[app_cores.__EVENT_TEMPLATE_FILTER__]
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
        logging.info('auth user: %s %s' % (request.method, request.path))
        flag = False
        for fn in app.plugin_manager.__app_fns__[app_cores.__EVENT_AUTHING__]:
            if await fn(app, request) is True:
                logging.info('auth fn : {} passed'.format(getattr(fn, '__app_fn_name__')))
                flag = True
            else:
                logging.info('auth fn : {} unpass'.format(getattr(fn, '__app_fn_name__')))

        if not flag:
            for fn in app.plugin_manager.__app_fns__[app_cores.__EVENT_AUTH_FLASE__]:
                await fn(app, request)
        return (await handler(request))

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


def api_response(r, status_code=200):
    resp = web.Response(status=status_code, body=json_response_body(api_response_body(r)))
    resp.content_type = 'application/json;charset=utf-8'
    return resp


def api_response_body(r, status_code=200):
    o = OrderedDict()
    o['ok'] = True if status_code == 200 else False
    o['body'] = r if r is not None else ('everything is ok !' if status_code == 200 else 'got something bad !')
    return o


def json_response_body(r):
    return json.dumps(r, ensure_ascii=False, default=lambda o: o.__dict__).encode('utf-8')


async def response_factory(app, handler):
    async def response(request):
        logging.info('Response handler...')
        r = await handler(request)
        logging.info('response is instance of {}'.format(type(r)))
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

        if isinstance(r, tuple) and len(r) == 2:
            t, m = r
            if isinstance(t, int) and t >= 100 and t < 600:
                return api_response(m, status_code=t)
        # default:
        resp = web.Response(body=str(r).encode('utf-8'))
        resp.content_type = 'text/plain;charset=utf-8'
        return resp

    return response


async def init(loop):
    await orm.create_pool(loop=loop, **configs.db)

    await db_localsystem_migrations()

    app = web.Application(loop=loop, middlewares=[
        logger_factory, auth_factory, response_factory
    ])

    plugin_manager = AppManager()
    plugin_manager.load_apps()
    app.plugin_manager = plugin_manager

    init_jinja2(app)
    add_routes(app, 'handlers')

    for item in app.plugin_manager.__apps__:
        try:
            add_static(app, item.name,
                       os.path.join(os.path.dirname(os.path.abspath(__file__)), 'apps', item.name, 'static'))
        except Exception as e:
            logging.warning(str(e))

    srv = await loop.create_server(app.make_handler(), '127.0.0.1', 9000)
    logging.info('server started at http://127.0.0.1:9000...')
    return srv


loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()
