import json
import events
from apps.auth_cookie.auth_cookie_utils import COOKIE_NAME, cookie2user, user2cookie
from apps.core.apis import APIValueError
from coroweb import post
from apps.core.models import User, UserProfile
import logging
from aiohttp import web
from app_cores import feature
from dbs import objects
from utils import hash_pwd


@feature(events.__FEATURE_AUTHING__, 'auth_cookie_provider', 'auth_cookie_provider')
async def auth_cookie_provider(app, request):
    """provider cookie into ncms auth"""
    request.__user__ = None
    cookie_str = request.cookies.get(COOKIE_NAME)
    if cookie_str:
        user = await cookie2user(cookie_str)
        if user:
            logging.info('set current user: %s' % user.email)
            request.__user__ = user
            return True, 'success set user to request context'
        return False, 'user can not be created from cookie'
    return False, 'cookie str empty'


@feature(events.__FEATURE_ROUTING__, 'api_login_using_cookie_by_email_and_password',
         'api_login_using_cookie_by_email_and_password')
@post('/api/login/cookie')
async def api_login_using_cookie_by_email_and_password(*, email, password):
    if not email:
        raise APIValueError('email', 'Invalid email.')
    if not password:
        raise APIValueError('passwd', 'Invalid password.')

    user = await objects.get(User.select().join(UserProfile).where(UserProfile.email == email))

    # check passwd:
    if user.password != hash_pwd(password):
        raise APIValueError('password', 'Invalid password.')
    # authenticate ok, set cookie:
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
    user.password = '******'
    r.content_type = 'application/json'
    # r.body = json.dumps(model_to_dict(user), default=utils.json_default, ensure_ascii=False).encode('utf-8')
    r.body = json.dumps({
        'ok': True
    })
    return r
