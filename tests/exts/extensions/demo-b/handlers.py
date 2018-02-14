from nory.infras.exts import features
from nory.infras.exts.decorators import feature
from nory.infras.web.decorators import get


@feature(features.__FEATURE_ROUTING__, 'demo-b', 'demo-b')
@get('/demo-b')
async def get_demo():
    return {
        '__template__': 'demo-a/templates/layout.html'
    }
