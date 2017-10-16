import logging

from aiohttp import web

from handlers import cookie2user, COOKIE_NAME
from plugins import plugin_fn


@plugin_fn('__auth__', 'auth-cookie', 'auth by cookie')
async def auth(app, request):
    # cookie auth-----------------------------
    request.__user__ = None
    cookie_str = request.cookies.get(COOKIE_NAME)
    if cookie_str:
        user = await cookie2user(cookie_str)
        if user:
            logging.info('set current user: %s' % user.email)
            request.__user__ = user
    if request.path.startswith('/manage/') and (request.__user__ is None or not request.__user__.admin):
        return web.HTTPFound('/signin')
        # ----------------------------------------
