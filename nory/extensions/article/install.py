import logging

from infrastructures.apps import features
from infrastructures.apps.decorators import feature
from extensions.article import models
from extensions.article.models import core_models
from extensions.rbacm.models import rbacm_models
from extensions.rbacm import models as rbacmm
from infrastructures.dbs import database, objects
from infrastructures.utils import hash_pwd

models_all = core_models + rbacm_models


@feature(features.__FEATURE_ON_APP_LOADING__, 'core_debug_init_db', 'core_debug_init_db')
async def init_db(app):
    database.create_tables(models_all, safe=True)

    await create_rbacm_init_data()


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

    # ------------------------------------------------------------------------------------------------------------------
    menu, _ = await objects.get_or_create(rbacmm.Menu,
                                          name='create_article',
                                          title='Create Article',
                                          href='/manage/articles#/create',
                                          target='admin-content',
                                          icon='note_add')

    permission, _ = await objects.get_or_create(rbacmm.Permission,
                                                name='create_article',
                                                title='create_article',
                                                type='U')
    permission_role_mapping, _ = await objects.get_or_create(rbacmm.PermissionRoleMappings,
                                                             role=admin_role,
                                                             permission=permission)

    menu_permission_mapping, _ = await objects.get_or_create(rbacmm.PermissionMenuMappings,
                                                             permission=permission,
                                                             menu=menu)
    operation, _ = await objects.get_or_create(rbacmm.Operation,
                                               name='create_article',
                                               title='create_article',
                                               url_pattern='POST:/api/articles')
    operation_permission_mapping, _ = await objects.get_or_create(rbacmm.PermissionOperationMappings,
                                                                  permission=permission,
                                                                  operation=operation)
    # ------------------------------------------------------------------------------------------------------------------
    menu, _ = await objects.get_or_create(rbacmm.Menu,
                                          name='article_list',
                                          title='Articles',
                                          href='/manage/articles#/list',
                                          target='admin-content',
                                          icon='view_list')

    permission, _ = await objects.get_or_create(rbacmm.Permission,
                                                name='article_list',
                                                title='article_list',
                                                type='U')
    permission_role_mapping, _ = await objects.get_or_create(rbacmm.PermissionRoleMappings,
                                                             role=admin_role,
                                                             permission=permission)

    menu_permission_mapping, _ = await objects.get_or_create(rbacmm.PermissionMenuMappings,
                                                             permission=permission,
                                                             menu=menu)
    operation, _ = await objects.get_or_create(rbacmm.Operation,
                                               name='article_list',
                                               title='article_list',
                                               url_pattern='GET:/api/articles')
    operation_permission_mapping, _ = await objects.get_or_create(rbacmm.PermissionOperationMappings,
                                                                  permission=permission,
                                                                  operation=operation)
