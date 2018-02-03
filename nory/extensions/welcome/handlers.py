from infrastructures.apps import features
from infrastructures.apps.decorators import feature
from infrastructures.web.decorators import get


@feature(features.__FEATURE_ROUTING__, 'page_welcome', 'page_welcome')
@get('/extensions/admin/welcome')
async def page_welcome(request):
    return {
        '__template__': 'welcome/templates/welcome.html',
        'user': request.__user__
    }
