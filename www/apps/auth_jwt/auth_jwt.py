from playhouse.shortcuts import model_to_dict

import app_cores
import events
from apps.core.apis import APIValueError
from apps.core.models import User, UserProfile
from coroweb import post
from dbs import objects
from utils import hash_pwd

__author__ = 'jeremaihloo'

__version__ = '0.0.1'

__description__ = 'provide jwt auth'

__home_page__ = 'https://github.com/jeremaihloo/ncms-auth-cookie'

import jwt
from app_cores import feature


@feature(events.__FEATURE_ROUTING__, 'auth_jwt_provider', 'auth_jwt_provider')
async def auth_jwt_provider(app, request):
    au_header_value = request.headers.get('Authorization', None)
    if au_header_value is None:
        return False, 'header Authorization not found'
    decoded = jwt.decode(au_header_value, algorithm='HS256')
    request.__user__ = decoded['user']
    return True, 'success set user to request context'


@feature(events.__FEATURE_ROUTING__, 'api_login_jwt_by_password_and_email', 'api_login_jwt_by_password_and_email')
@post('/api/login/jwt')
async def api_login_jwt_by_password_and_email(*, email, password):
    if not email:
        raise APIValueError('email', 'Invalid email.')
    if not password:
        raise APIValueError('passwd', 'Invalid password.')

    user = await objects.get(
        User.select(UserProfile).where(UserProfile.email == email, User.password == hash_pwd(password)))
    if len(user) == 0:
        raise APIValueError('email', 'Email not exist.')

    user = model_to_dict(user, exclude=[User.password])
    encoded = jwt.encode(user)
    return 200, encoded
