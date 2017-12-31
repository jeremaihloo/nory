import events
from app_cores import feature
from coroweb import get


@feature(events.__FEATURE_ROUTING__, 'admin', 'admin manage index')
@get('/admin')
def page_admin():
    return {
        '__template__': 'admin/templates/index.html'
    }
