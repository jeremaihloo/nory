from infrastructures import events
from infrastructures.web.coros import get
from infrastructures.apps.coros import feature


@feature(events.__FEATURE_BEFORE_REQUEST__, 'add_request_into_db', 'add 1 after request')
async def add_once_request(app, request):
    pass


@feature(events.__FEATURE_BEFORE_REQUEST__, 'add_request_into_db', 'add 1 after request')
@get('/api/page-statistics')
async def api_get_page_statistics():
    pass
