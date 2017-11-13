from app_cores import app_fn, __EVENT_ROUTING__
from coroweb import get


@app_fn(__EVENT_ROUTING__, 'demo', 'demo')
@get('/demo')
async def get_demo():
    return {
        '__template__': 'demo/templates/index.html'
    }
