
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


@app_fn(events.__EVENT_ON_APP_LOADING__, 'on_core_install', 'on_core_install')
async def on_load_check_create_table_for_debug():
    if NcmsConfig.debug:
        database.drop_tables([
            models.User,
            models.Article,
            models.Tag,
            models.UserProfile,
            models.ArticleTagMapping,
            models.Settings
        ], safe=True)
    database.create_tables([
        models.User,
        models.Article,
        models.Tag,
        models.UserProfile,
        models.ArticleTagMapping,
        models.Settings
    ], safe=True)

    await create_debug_data()


async def create_debug_data():
    for index in range(25):
        user, _ = await objects.get_or_create(models.User,
                                              name='username{}'.format(index),
                                              password=hash_pwd('111'))

        await objects.create(models.UserProfile,
                             user=user,
                             email='email{}@ncms.com'.format(index),
                             nick_name='nickname{}'.format(index),
                             phone='phone{}'.format(index),
                             image='image{}'.format(index))

        tag, _ = await objects.get_or_create(models.Tag,
                                             content='Tag{}'.format(index))

        article, _ = await objects.get_or_create(models.Article,
                                                 user=user,
                                                 title='article{}'.format(index),
                                                 content='# article{}'.format(index))

        await objects.get_or_create(models.ArticleTagMapping,
                                    article=article,
                                    tag=tag)
