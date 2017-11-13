from coroweb import get

__author__ = 'jeremaihloo'

__version__ = '0.0.1'

__description__ = 'provide jwt auth'

__home_page__ = 'https://github.com/jeremaihloo/ncms-rbacm'

from app_cores import app_fn

routes = []


@app_fn('__add_route__', 'add_route_to_table', 'on add route do this ')
def add_route_to_table(method, url, params):
    routes.append({
        'method': method,
        'url': url,
        'params': params
    })


@app_fn('__routes__', 'get_routes', 'on add route do this ')
@get('/api/routes')
async def api_get_routes():
    return {
        'routes': routes
    }


@app_fn('__routes__', 'get_api_table', 'get api table')
@get('/apis')
async def api_get_api_tables():
    return {
        'apis': list(filter(lambda x: x['url'].startswith('/api'), routes))
    }
