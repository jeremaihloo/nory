import logging

import events
from app_cores import feature
from apps.core import models
from apps.core.models import core_models
from apps.rbacm.models import rbacm_models
from apps.rbacm import models as rbacmm
from configs import NcmsConfig
from dbs import database, objects
from utils import hash_pwd

models_all = core_models + rbacm_models


@feature(events.__FEATURE_ON_APP_LOADING__, 'core_debug_init_db', 'core_debug_init_db')
async def app_core_debug_init_db():
    if NcmsConfig.debug:
        database.drop_tables(models_all, safe=True)
    database.create_tables(models_all, safe=True)

    await create_debug_data()

    await create_rbacm_init_data()


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


async def create_rbacm_init_data():
    admin, _ = await objects.get_or_create(models.User,
                                           name='jeremaihloo',
                                           password=hash_pwd('111'))
    logging.info('admin_user: {}'.format(admin))
    admin_profile = await objects.get_or_create(models.UserProfile,
                                                email='1006397539@qq.com',
                                                nick_name='jeremaihloo',
                                                user=admin)

    admin_role, _ = await objects.get_or_create(rbacmm.Role,
                                                name='admin',
                                                title='Administrator',
                                                description='Administrator')
    admin_user_role_map, _ = await objects.get_or_create(rbacmm.UserRoleMappings,
                                                         user=admin,
                                                         role=admin_role)

    admin_user_group, _ = await objects.get_or_create(rbacmm.UserGroup,
                                                      name='admin',
                                                      title='admin',
                                                      description='admin')
    admin_user_group_mapping, _ = await objects.get_or_create(rbacmm.UserGroupMappings,
                                                              group=admin_user_group,
                                                              user=admin)
    create_article_menu, _ = await objects.get_or_create(rbacmm.Menu,
                                                         name='create_article',
                                                         title='create_article',
                                                         href='/core/article',
                                                         target='admin-content')

    create_article_permission, _ = await objects.get_or_create(rbacmm.Permission,
                                                               name='create_article',
                                                               title='create_article',
                                                               type='U')

    create_article_menu_permission_mapping, _ = await objects.get_or_create(rbacmm.PermissionMenuMappings,
                                                                            permission=create_article_permission,
                                                                            menu=create_article_menu)
    create_article_api_operation, _ = await objects.get_or_create(rbacmm.Operation,
                                                                  name='create_article',
                                                                  title='create_article',
                                                                  url_pattern='/api/article')
    create_article_api_operation_permission_mapping, _ = await objects.get_or_create(rbacmm.PermissionOperationMappings,
                                                                                     permission=create_article_permission,
                                                                                     operation=create_article_api_operation)
