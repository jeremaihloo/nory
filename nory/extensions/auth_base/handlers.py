import logging

from aiohttp import web

from infrastructures.apps import features
from infrastructures.apps.coros import feature
from extensions.auth_base import white


@feature(features.__FEATURE_AUTH_FALSE__, 'auth_cookie_provider', 'auth_cookie_provider')
async def auth_false_provider(app, request):
    """provider cookie into ncms auth"""
    logging.info('[auth_false_provider] auth white urls : {}'.format(white.__urls__))
    if request.path not in white.__urls__ and not is_static(request.path):
        logging.info('[auth_false] must raise http forbidden')
        raise web.HTTPForbidden()


def is_static(path):
    return path.find('.') > -1
