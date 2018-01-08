import events
from app_cores import feature
from apps.auth_base.white import allow_anyone
from coroweb import get


@allow_anyone
@feature(events.__FEATURE_ROUTING__, 'admin', 'admin manage index')
@get('/admin')
def page_admin():
    return {
        '__template__': 'admin/adminify/dist/index.html'
    }
