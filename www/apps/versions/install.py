from apps.versions.models import Version
from infrastructures import events
from infrastructures.apps.decorators import feature
from infrastructures.dbs import database


@feature(events.__FEATURE_ON_APP_INSTALLING__, 'on_app_versions_installing', 'on_app_versions_installing')
async def on_app_versions_installing():
    database.create_tables([Version], True)
