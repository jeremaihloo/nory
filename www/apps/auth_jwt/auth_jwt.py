import app_cores

__author__ = 'jeremaihloo'

__version__ = '0.0.1'

__description__ = 'provide jwt auth'

__home_page__ = 'https://github.com/jeremaihloo/ncms-auth-cookie'

import jwt
from app_cores import app_fn


@app_fn(app_cores.__EVENT_ROUTING__, 'auth-jwt', 'auth use perssions')
async def auth(app, request):
    au_header_value = request.headers.get('Authorization', None)
    if au_header_value is None:
        return False
    decoded = jwt.decode(au_header_value, algorithm='HS256')
    request.__user__ = decoded['user']
    return True
