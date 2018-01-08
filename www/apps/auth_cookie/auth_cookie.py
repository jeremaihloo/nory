from playhouse.shortcuts import model_to_dict

from infrastructures import events
from apps.auth_base.white import allow_anyone
from apps.auth_cookie.auth_cookie_utils import COOKIE_NAME, cookie2user, user2cookie
from infrastructures.errors import NcmsWebApiValueError
from infrastructures.web.decorators import post, get
from apps.article.models import User, UserProfile
import logging
from aiohttp import web
from infrastructures.apps.decorators import feature
from infrastructures.dbs import objects
from infrastructures.utils import hash_pwd, json_dumps


@feature(events.__FEATURE_AUTHING__, 'auth_cookie_provider', 'auth_cookie_provider')
async def auth_cookie_provider(app, request):
    """provider cookie into ncms auth"""
    cookie_str = request.cookies.get(COOKIE_NAME)

    if cookie_str:
        user = await cookie2user(cookie_str)
        if user:
            logging.info('set current user: %s, %s' % (str(user.id), user.name))
            request.__user__ = user
            return True, 'success set user to request context'
        return False, 'user can not be created from cookie'
    return False, 'cookie str empty'


@allow_anyone
@feature(events.__FEATURE_ROUTING__, 'api_login_using_cookie_by_email_and_password',
         'api_login_using_cookie_by_email_and_password')
@post('/api/login/cookie')
async def api_login_using_cookie_by_email_and_password(*, email, password):
    if not email:
        raise NcmsWebApiValueError('email', 'Invalid email.')
    if not password:
        raise NcmsWebApiValueError('passwd', 'Invalid password.')

    user = await objects.get(
        User.select().join(UserProfile).where(UserProfile.email == email, User.password == hash_pwd(password)))

    # check passwd:
    if user.password != hash_pwd(password):
        raise NcmsWebApiValueError('password', 'Invalid password.')
    # authenticate ok, set cookie:
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
    user.password = '******'
    r.content_type = 'application/json'
    # r.body = json.dumps(model_to_dict(user), default=utils.json_default, ensure_ascii=False).encode('utf-8')
    r.body = json_dumps({
        'ok': True,
        'user': model_to_dict(user)
    })
    return r


@allow_anyone
@feature(events.__FEATURE_ROUTING__, 'api_logout_using_cookie_by_email_and_password',
         'api_logout_using_cookie_by_email_and_password')
@post('/api/logout/cookie')
async def api_logout_using_cookie_by_email_and_password(request):
    if request.__user__ is None:
        return 200

    r = web.Response()
    r.set_cookie(COOKIE_NAME, '', max_age=-1, httponly=True)
    return r


@feature(events.__FEATURE_ROUTING__, 'api_auth_cookie_me', 'api_auth_cookie_me')
@get('/api/auth/cookie/me')
async def api_auth_cookie_me(request):
    if request.__user__ is None:
        return 403

    return 200
