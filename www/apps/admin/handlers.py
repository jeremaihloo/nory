from app_cores import app_fn, __EVENT_ROUTING__
from coroweb import get


@app_fn(__EVENT_ROUTING__, 'admin', 'admin manage index')
@get('/admin')
def page_admin():
    return {
        '__template__': 'admin/templates/index.html'
    }
