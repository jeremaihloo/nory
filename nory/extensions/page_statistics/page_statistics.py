from infrastructures.apps import features
from infrastructures.apps.decorators import feature
from infrastructures.web.decorators import get


@feature(features.__FEATURE_BEFORE_REQUEST__, 'add_request_into_db', 'add 1 after request')
async def add_once_request(app, request):
    pass


@feature(features.__FEATURE_BEFORE_REQUEST__, 'add_request_into_db', 'add 1 after request')
@get('/api/page-statistics')
async def api_get_page_statistics():
    pass
