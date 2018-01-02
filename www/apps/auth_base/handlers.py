import logging

from aiohttp import web

import events
from app_cores import feature
from apps.auth_base import white


@feature(events.__FEATURE_AUTH_FALSE__, 'auth_cookie_provider', 'auth_cookie_provider')
async def auth_false_provider(app, request):
    """provider cookie into ncms auth"""
    if request.path not in white.__urls__:
        logging.info('[auth_false] must raise http forbidden')
        raise web.HTTPForbidden()
