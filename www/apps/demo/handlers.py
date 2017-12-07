import events
from app_cores import app_fn
from coroweb import get


@app_fn(events.__EVENT_ROUTING__, 'demo', 'demo')
@get('/demo')
async def get_demo():
    return {
        '__template__': 'demo/templates/layout.html'
    }
