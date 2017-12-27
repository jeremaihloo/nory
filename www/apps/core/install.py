
import events
from app_cores import app_fn
from apps.core import models
from dbs import database, objects
from configs import NcmsConfig
from utils import hash_pwd


@app_fn(events.__EVENT_ON_APP_INSTALLING__, 'on_core_install', 'on_core_install')
async def on_install_create_table():
    database.create_tables([
        models.User,
        models.Article,
        models.Tag,
        models.UserProfile,
        models.ArticleTagMapping,
        models.Settings
    ])
