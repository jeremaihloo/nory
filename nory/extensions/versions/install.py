from extensions.versions.models import Version
from infrastructures.apps import features
from infrastructures.apps.decorators import feature
from infrastructures.dbs import database


@feature(features.__FEATURE_ON_APP_INSTALLING__, 'on_app_versions_installing', 'on_app_versions_installing')
async def on_app_versions_installing():
    database.create_tables([Version], True)
