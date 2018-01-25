from infrastructures import events
from infrastructures.apps.coros import feature
from infrastructures.web.coros import get


@feature(events.__FEATURE_ROUTING__, 'demo-app-for-tests', 'demo-app-for-tests')
@get('/demo-app-for-tests')
async def get_demo():
    return {
        '__template__': 'demo-app-for-tests/templates/layout.html'
    }
