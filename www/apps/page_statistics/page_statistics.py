import app_cores
from coroweb import get
from app_cores import app_fn


@app_fn(app_cores.__EVENT_REQUEST__, 'add_request_into_db', 'add 1 after request')
async def add_once_request(app, request):
    pass


@app_fn(app_cores.__EVENT_REQUEST__, 'add_request_into_db', 'add 1 after request')
@get('/api/page-statistics')
async def api_get_page_statistics():
    pass
