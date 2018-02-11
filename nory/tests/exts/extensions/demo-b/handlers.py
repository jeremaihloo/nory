from infras.exts import features
from infras.exts.managers import feature
from infras.web.coros import get


@feature(features.__FEATURE_ROUTING__, 'demo-a', 'demo-a')
@get('/demo-a')
async def get_demo():
    return {
        '__template__': 'demo-a/templates/layout.html'
    }
