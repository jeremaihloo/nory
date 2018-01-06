import events
from app_cores import feature
from coroweb import get


@feature(events.__FEATURE_ROUTING__, 'page_welcome', 'page_welcome')
@get('/apps/admin/welcome')
async def page_welcome(request):
    return {
        '__template__': 'welcome/templates/welcome.html',
        'user': request.__user__
    }
