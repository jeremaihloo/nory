from infrastructures import events
from infrastructures.apps.decorators import feature
from apps.auth_base.white import allow_anyone
from infrastructures.web.decorators import get


@allow_anyone
@feature(events.__FEATURE_ROUTING__, 'admin', 'admin manage index')
@get('/admin')
def page_admin():
    return {
        '__template__': 'admin/adminify/dist/index.html'
    }
