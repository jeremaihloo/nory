import events
from app_cores import app_fn
from apps.core import models
from apps.rbacm.models import Role, Permission, RolePermissionMappings, UserRoleMappings, Menu, RoleMenuMappings
from configs import NcmsConfig
from dbs import database, objects
from utils import hash_pwd


@app_fn(events.__EVENT_ON_APP_LOADING__, 'core_debug_init_db', 'core_debug_init_db')
async def app_core_debug_init_db():
    if NcmsConfig.debug:
        database.drop_tables([
            models.User,
            models.Article,
            models.Tag,
            models.UserProfile,
            models.ArticleTagMapping,
            models.Settings,
            Role,
            Permission,
            RolePermissionMappings,
            UserRoleMappings,
            Menu,
            RoleMenuMappings
        ], safe=True)
    database.create_tables([
        models.User,
        models.Article,
        models.Tag,
        models.UserProfile,
        models.ArticleTagMapping,
        models.Settings,
        Role,
        Permission,
        RolePermissionMappings,
        UserRoleMappings,
        Menu,
        RoleMenuMappings
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
