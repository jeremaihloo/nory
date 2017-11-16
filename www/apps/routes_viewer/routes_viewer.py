import app_cores
from coroweb import get
from app_cores import app_fn

routes = []


@app_fn(app_cores.__EVENT_ADD_ROUTE__, 'add_route_to_table', 'on add route do this ')
def add_route_to_table(method, url, params):
    routes.append({
        'method': method,
        'url': url,
        'params': params
    })


@app_fn(app_cores.__EVENT_ROUTING__, 'get_routes', 'on add route do this ')
@get('/api/routes')
def api_get_routes():
    return  {
        'routes': routes
    }


@app_fn(app_cores.__EVENT_ROUTING__, 'get_api_table', 'get api table')
@get('/apis')
def api_get_api_tables():
    return {
        'apis': list(filter(lambda x: x['url'].startswith('/api'), routes))
    }
