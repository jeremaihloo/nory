from nory.infras.exts import features
from nory.infras.exts.decorators import feature
from nory.infras.web.decorators import get


@feature(features.__FEATURE_ROUTING__, 'demo-a', 'demo-a')
@get('/demo-a')
async def get_demo():
    return '200'
