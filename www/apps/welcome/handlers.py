from infrastructures import events
from infrastructures.apps.coros import feature
from infrastructures.web.coros import get


@feature(events.__FEATURE_ROUTING__, 'page_welcome', 'page_welcome')
@get('/apps/admin/welcome')
async def page_welcome(request):
    return {
        '__template__': 'welcome/templates/welcome.html',
        'user': request.__user__
    }
