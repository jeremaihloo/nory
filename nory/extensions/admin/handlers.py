from infrastructures.apps import features
from infrastructures.apps.decorators import feature
from extensions.auth_base.white import allow_anyone
from infrastructures.web.decorators import get


@allow_anyone
@feature(features.__FEATURE_ROUTING__, 'admin', 'admin manage index')
@get('/admin')
def page_admin():
    return {
        '__template__': 'admin/adminify/dist/index.html'
    }
