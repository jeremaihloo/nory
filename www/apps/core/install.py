import events
from app_cores import app_fn
from apps.core import models
from dbs import database


@app_fn(events.__EVENT_ON_APP_INSTALLING__, 'on_core_install', 'on_core_install')
async def on_install_create_table():
    database.create_tables([
        models.User,
        models.Article,
        models.Tag,
        models.UserProfile,
        models.PostRecord,
        models.ArticleTagMapping,
        models.Settings
    ])


@app_fn(events.__EVENT_ON_APP_LOADING__, 'on_core_install', 'on_core_install')
def on_load_check_create_table():
    database.create_tables([
        models.User,
        models.Article,
        models.Tag,
        models.UserProfile,
        models.PostRecord,
        models.ArticleTagMapping,
        models.Settings
    ])
