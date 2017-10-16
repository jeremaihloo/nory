import jwt

from plugins import plugin_fn

__author__ = 'jeremaihloo'

__version__ = '0.0.1'

__description__ = 'provide jwt auth'

__home_page__ = 'https://github.com/jeremaihloo/ncms-jwt-auth'

@plugin_fn('__auth__', 'auth-jwt', 'auth use perssions')
async def auth(app, request):
    decoded = jwt.decode(request.body, algorithm='HS256')
    request.__user__ = decoded['user']
    return True