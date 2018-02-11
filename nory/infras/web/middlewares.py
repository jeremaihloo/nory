import logging
from collections import OrderedDict

from aiohttp import web

from nory.infras import constants
from nory.infras.exts import features
from nory.infras.utils import json_dumps


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