import app_cores
import events
from apps.auth_cookie.auth_cookie_utils import COOKIE_NAME, cookie2user, user2cookie
from apps.core.apis import APIValueError
from coroweb import post
from apps.core.models import User
import logging
import hashlib, json
from aiohttp import web
from app_cores import app_fn


@app_fn(events.__EVENT_AUTHING__, 'auth_cookie_provider', 'auth_cookie_provider')
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


@app_fn(events.__EVENT_ROUTING__, 'auth-cookie', 'auth by cookie')
@post('/api/login/auth-cookie')
async def api_auth_cookie_by_email_and_password(*, email, passwd):
    if not email:
        raise APIValueError('email', 'Invalid email.')
    if not passwd:
        raise APIValueError('passwd', 'Invalid password.')
    users = await User.findAll('email=?', [email])
    if len(users) == 0:
        raise APIValueError('email', 'Email not exist.')
    user = users[0]
    # check passwd:
    sha1 = hashlib.sha1()
    sha1.update(user.id.encode('utf-8'))
    sha1.update(b':')
    sha1.update(passwd.encode('utf-8'))
    if user.passwd != sha1.hexdigest():
        raise APIValueError('passwd', 'Invalid password.')
    # authenticate ok, set cookie:
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
    user.passwd = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r
