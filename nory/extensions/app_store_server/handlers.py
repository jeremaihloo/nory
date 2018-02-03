from extensions.app_store_server.models import AppIndexItem
from infrastructures.apps import features
from infrastructures.apps.decorators import feature
from infrastructures.dbs import objects
from infrastructures.web.decorators import get


@feature(features.__FEATURE_ROUTING__, 'api_app_store_search', 'api_app_store_search')
@get('/api/app-store/search/{key}')
async def api_app_store_search(*, key):
    items = await objects.execute(AppIndexItem.select()
                                  .where(AppIndexItem.name.contains(key) |
                                         AppIndexItem.description.contains(key)))
    return 200, items

