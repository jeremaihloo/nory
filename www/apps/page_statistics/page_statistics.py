from coroweb import get
from app_cores import app_fn

__author__ = 'jeremaihloo'

__version__ = '0.0.1'

__description__ = 'provide jwt auth'

__home_page__ = 'https://github.com/jeremaihloo/ncms-rbacm'


@app_fn('__request__', 'add_request_into_db', 'add 1 after request')
async def add_once_request(app, request):
    pass


@app_fn('__request__', 'add_request_into_db', 'add 1 after request')
@get('/api/page-statistics')
async def api_get_page_statistics():
    pass
