
import events
from coroweb import get
from app_cores import feature


@feature(events.__FEATURE_BEFORE_REQUEST__, 'add_request_into_db', 'add 1 after request')
async def add_once_request(app, request):
    pass


@feature(events.__FEATURE_BEFORE_REQUEST__, 'add_request_into_db', 'add 1 after request')
@get('/api/page-statistics')
async def api_get_page_statistics():
    pass
