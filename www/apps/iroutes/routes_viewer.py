from infrastructures.apps import features
from infrastructures.web.coros import get
from infrastructures.apps.coros import feature

routes = []


@feature(features.__FEATURE_ADD_ROUTE__, 'add_route_to_table', 'on add route do this ')
def add_route_to_table(method, url, params):
    routes.append({
        'method': method,
        'url': url,
        'params': params
    })


@feature(features.__FEATURE_ROUTING__, 'get_routes', 'on add route do this ')
@get('/api/routes')
def api_get_routes():
    return  {
        'routes': routes
    }


@feature(features.__FEATURE_ROUTING__, 'get_api_table', 'get api table')
@get('/apis')
def api_get_api_tables():
    return {
        'apis': list(filter(lambda x: x['url'].startswith('/api'), routes))
    }
