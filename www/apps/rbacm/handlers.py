import logging

from playhouse.shortcuts import model_to_dict

import events
from app_cores import feature
from apps.article.models import User
from apps.rbacm.models import Role, Menu, UserRoleMappings, UserGroup, PageDisplay, FileEntry, \
    Operation, PermissionMenuMappings, PermissionOperationMappings, Permission, PermissionRoleMappings
from coroweb import post, get
from dbs import objects


# ----------------------------------role----------------------------------
@feature(events.__FEATURE_ROUTING__, 'api_create_role', 'api_create_role')
@post('/api/roles')
async def api_create_role(*, name, title, description):
    role = {
        'name': name,
        'title': title,
        'description': description
    }
    saved, _ = await objects.get_or_create(Role, **role)
    return 200, model_to_dict(saved)


@feature(events.__FEATURE_ROUTING__, 'api_get_roles', 'api_get_roles')
@get('/api/roles')
async def api_get_roles():
    roles = await objects.execute(Role.select())
    return 200, [model_to_dict(x) for x in roles]


@feature(events.__FEATURE_ROUTING__, 'api_create_user_role_mappings', 'api_create_user_role_mappings')
@post('/api/user-role-mappings')
async def api_create_user_role_mappings(*, user, role):
    user_role_mapping = {
        'user': user,
        'role': role
    }
    saved = await objects.get_or_create(UserRoleMappings, user_role_mapping)
    return 200, saved


# -----------------------------------user-group---------------------------
@feature(events.__FEATURE_ROUTING__, 'api_create_user_group', 'api_create_user_group')
@post('/api/user-groups')
async def api_create_user_group(*, name, title, description):
    user_group = {
        'name': name,
        'title': title,
        'description': description
    }
    saved, _ = await objects.get_or_create(UserGroup, **user_group)
    return 200, model_to_dict(saved)


@feature(events.__FEATURE_ROUTING__, 'api_get_user_groups', 'api_get_user_groups')
@get('/api/user-groups')
async def api_get_user_groups():
    user_groups = await objects.execute(UserGroup.select())
    return 200, [model_to_dict(x) for x in user_groups]


@feature(events.__FEATURE_ROUTING__, 'api_create_user_group_mapping', 'api_create_user_group_mapping')
@post('/api/user-group-mappings')
async def api_create_user_group_mapping(*, user, group):
    user_group_mapping = {
        'user': user,
        'group': group
    }
    saved, _ = await objects.get_or_create(UserGroup, **user_group_mapping)
    return 200, model_to_dict(saved)


@feature(events.__FEATURE_ROUTING__, 'api_create_user_group_role_mapping', 'api_create_user_group_role_mapping')
@post('/api/user-group-role-mappings')
async def api_create_user_group_role_mapping(*, group, role):
    user_group_role_mapping = {
        'group': group,
        'role': role
    }
    saved, _ = await objects.get_or_create(UserGroup, **user_group_role_mapping)
    return 200, model_to_dict(saved)


# -----------------------------------user-group---------------------------
@feature(events.__FEATURE_ROUTING__, 'api_create_permission', 'api_create_permission')
@post('/api/permissions')
async def api_create_permission(*, name, title, description):
    permission = {
        'name': name,
        'title': title,
        'description': description
    }
    saved, _ = await objects.get_or_create(Permission, **permission)
    return 200, model_to_dict(saved)


@feature(events.__FEATURE_ROUTING__, 'api_get_permissions', 'api_get_permissions')
@get('/api/permissions')
async def api_get_permissions():
    permissions = await objects.execute(Permission.select())
    return 200, [model_to_dict(x) for x in permissions]


@feature(events.__FEATURE_ROUTING__, 'api_create_permission_role_mapping', 'api_create_permission_role_mapping')
@post('/api/permission-role-mappings')
async def api_create_permission_role_mapping(*, permission, role):
    user_group = {
        'permission': permission,
        'role': role
    }
    saved, _ = await objects.get_or_create(UserGroup, **user_group)
    return 200, model_to_dict(saved)


# -----------------------------------user-group---------------------------
@feature(events.__FEATURE_ROUTING__, 'api_create_menu', 'api_create_menu')
@post('/api/menus')
async def api_create_menu(*, name, title, icon, parent, target):
    menu = {
        'name': name,
        'title': title,
        'icon': icon,
        'parent': parent,
        'target': target
    }
    saved, _ = await objects.get_or_create(Menu, **menu)
    return 200, model_to_dict(saved)


@feature(events.__FEATURE_ROUTING__, 'api_get_menus', 'api_get_menus')
@get('/api/menus')
async def api_get_menus(request):
    query_role = (Role.select()
        .join(UserRoleMappings)
        .join(User)
        .where(User.id == request.__user__.id))
    roles = await objects.execute(query_role)
    roles = [str(x.id) for x in roles]
    logging.info('[api_get_menus] roles : {}'.format(roles))

    query_permissions = (Permission.select(Permission)
        .join(PermissionRoleMappings)
        .join(Role)
        .where(Role.id in roles))

    permissions = await objects.execute(query_permissions)
    permissions = [str(x.id) for x in permissions]
    logging.info('[api_get_menus] user permissions : {}'.format(permissions))

    query_menu = (Menu.select()
        .join(PermissionMenuMappings)
        .join(Permission)
        .where(Permission.id in [x for x in permissions]))
    menus = await objects.execute(query_menu)

    return 200, [model_to_dict(x) for x in menus]


@feature(events.__FEATURE_ROUTING__, 'api_create_permission_menu_mapping', 'api_create_permission_menu_mapping')
@post('/api/permission-menus-mappings')
async def api_create_permission_menu_mapping(*, permission, menu):
    permission_menu_mapping = {
        'permission': permission,
        'menu': menu
    }
    saved, _ = await objects.get_or_create(PermissionMenuMappings, **permission_menu_mapping)
    return 200, model_to_dict(saved)


# -----------------------------------user-group---------------------------
@feature(events.__FEATURE_ROUTING__, 'api_create_page_display', 'api_create_page_display')
@post('/api/page-display')
async def api_create_page_display(*, name, title, description):
    page_display = {
        'name': name,
        'title': title,
        'description': description
    }
    saved, _ = await objects.get_or_create(PageDisplay, **page_display)
    return 200, model_to_dict(saved)


@feature(events.__FEATURE_ROUTING__, 'api_create_permission_page_display', 'api_create_permission_page_display')
@post('/api/permission-page-display-mappings')
async def api_create_permission_page_display(*, permission, page_display):
    page_display = {
        'permission': permission,
        'page_display': page_display
    }
    saved, _ = await objects.get_or_create(PageDisplay, **page_display)
    return 200, model_to_dict(saved)


@feature(events.__FEATURE_ROUTING__, 'api_get_page_displays', 'api_get_page_displays')
@get('/api/page-displays')
async def api_get_page_displays():
    page_displays = await objects.execute(PageDisplay.select())
    return 200, [model_to_dict(x) for x in page_displays]


# -----------------------------------user-group---------------------------
@feature(events.__FEATURE_ROUTING__, 'api_create_file_entry', 'api_create_file_entry')
@post('/api/file-entry')
async def api_create_file_entry(*, name, title, description):
    file_entry = {
        'name': name,
        'title': title,
        'description': description
    }
    saved, _ = await objects.get_or_create(FileEntry, **file_entry)
    return 200, model_to_dict(saved)


@feature(events.__FEATURE_ROUTING__, 'api_get_page_file_entries', 'api_get_page_file_entries')
@get('/api/page-displays')
async def api_get_page_file_entries():
    file_entries = await objects.execute(FileEntry.select())
    return 200, [model_to_dict(x) for x in file_entries]


@feature(events.__FEATURE_ROUTING__, 'api_create_permission_file_entry', 'api_create_permission_file_entry')
@post('/api/permission-file-entry-mappings')
async def api_create_permission_file_entry(*, permission, entry_file):
    permission_file_entry = {
        'permission': permission,
        'entry_file': entry_file
    }
    saved, _ = await objects.get_or_create(FileEntry, **permission_file_entry)
    return 200, model_to_dict(saved)


# -----------------------------------user-group---------------------------
@feature(events.__FEATURE_ROUTING__, 'api_create_operation', 'api_create_operation')
@post('/api/operations')
async def api_create_operation(*, name, title, description):
    operation = {
        'name': name,
        'title': title,
        'description': description
    }
    saved, _ = await objects.get_or_create(Operation, **operation)
    return 200, model_to_dict(saved)


@feature(events.__FEATURE_ROUTING__, 'api_get_page_operation', 'api_get_page_operation')
@get('/api/operations')
async def api_get_page_operation():
    operations = await objects.execute(Operation.select())
    return 200, [model_to_dict(x) for x in operations]


@feature(events.__FEATURE_ROUTING__, 'api_create_permission_operation', 'api_create_permission_operation')
@post('/api/permission-operation-mappings')
async def api_create_permission_operation(*, permission, operation):
    permission_operation = {
        'permission': permission,
        'operation': operation
    }
    saved, _ = await objects.get_or_create(PermissionOperationMappings, **permission_operation)
    return 200, model_to_dict(saved)
