import events
from app_cores import feature
from apps.rbacm.models import Role, Menu, RoleMenuMappings, UserRoleMappings, UserGroup, PageDisplay, FileEntry, \
    Operation, PermissionMenuMappings, PermissionOperationMappings
from coroweb import post
from dbs import objects


# ----------------------------------role----------------------------------
@feature(events.__FEATURE_ROUTING__, 'api_create_role', 'api_create_role')
@post('/api/roles')
async def api_create_role(name, title, description):
    role = {
        'name': name,
        'title': title,
        'description': description
    }
    saved = await objects.get_or_create(Role, role)
    return 200, saved


@feature(events.__FEATURE_ROUTING__, 'api_create_role', 'api_create_role')
@post('/api/user-role-mappings')
async def api_create_user_role_mappings(user, role):
    user_role_mapping = {
        'user': user,
        'role': role
    }
    saved = await objects.get_or_create(UserRoleMappings, user_role_mapping)
    return 200, saved


# -----------------------------------user-group---------------------------
@feature(events.__FEATURE_ROUTING__, 'api_create_role', 'api_create_role')
@post('/api/user-groups')
async def api_create_user_group(name, title, description):
    user_group = {
        'name': name,
        'title': title,
        'description': description
    }
    saved = await objects.get_or_create(UserGroup, user_group)
    return 200, saved


@feature(events.__FEATURE_ROUTING__, 'api_create_role', 'api_create_role')
@post('/api/user-group-mappings')
async def api_create_user_group_mapping(user, group):
    user_group_mapping = {
        'user': user,
        'group': group
    }
    saved = await objects.get_or_create(UserGroup, user_group_mapping)
    return 200, saved


@feature(events.__FEATURE_ROUTING__, 'api_create_role', 'api_create_role')
@post('/api/user-group-role-mappings')
async def api_create_user_group_role_mapping(group, role):
    user_group_role_mapping = {
        'group': group,
        'role': role
    }
    saved = await objects.get_or_create(UserGroup, user_group_role_mapping)
    return 200, saved


# -----------------------------------user-group---------------------------
@feature(events.__FEATURE_ROUTING__, 'api_create_role', 'api_create_role')
@post('/api/permissions')
async def api_create_permission(name, title, description):
    user_group = {
        'name': name,
        'title': title,
        'description': description
    }
    saved = await objects.get_or_create(UserGroup, user_group)
    return 200, saved


@feature(events.__FEATURE_ROUTING__, 'api_create_role', 'api_create_role')
@post('/api/permission-role-mappings')
async def api_create_permission_role_mapping(permission, role):
    user_group = {
        'permission': permission,
        'role': role
    }
    saved = await objects.get_or_create(UserGroup, user_group)
    return 200, saved


# -----------------------------------user-group---------------------------
@feature(events.__FEATURE_ROUTING__, 'api_create_menu', 'api_create_menu')
@post('/api/menus')
async def api_create_menu(name, title, icon, parent, target):
    menu = {
        'name': name,
        'title': title,
        'icon': icon,
        'parent': parent,
        'target': target
    }
    saved = await objects.get_or_create(Menu, menu)
    return 200, saved


@feature(events.__FEATURE_ROUTING__, 'api_create_menu', 'api_create_menu')
@post('/api/permission-menus-mappings')
async def api_create_permission_menu_mapping(permission, menu):
    permission_menu_mapping = {
        'permission': permission,
        'menu': menu
    }
    saved = await objects.get_or_create(PermissionMenuMappings, permission_menu_mapping)
    return 200, saved


# -----------------------------------user-group---------------------------
@feature(events.__FEATURE_ROUTING__, 'api_create_menu', 'api_create_menu')
@post('/api/page-display')
async def api_create_page_display(name, title, description):
    page_display = {
        'name': name,
        'title': title,
        'description': description
    }
    saved = await objects.get_or_create(PageDisplay, page_display)
    return 200, saved


@feature(events.__FEATURE_ROUTING__, 'api_create_menu', 'api_create_menu')
@post('/api/permission-page-display-mappings')
async def api_create_permission_page_display(permission, page_display):
    page_display = {
        'permission': permission,
        'page_display': page_display
    }
    saved = await objects.get_or_create(PageDisplay, page_display)
    return 200, saved


# -----------------------------------user-group---------------------------
@feature(events.__FEATURE_ROUTING__, 'api_create_menu', 'api_create_menu')
@post('/api/file-entry')
async def api_create_file_entry(name, title, description):
    file_entry = {
        'name': name,
        'title': title,
        'description': description
    }
    saved = await objects.get_or_create(FileEntry, file_entry)
    return 200, saved


@feature(events.__FEATURE_ROUTING__, 'api_create_menu', 'api_create_menu')
@post('/api/permission-file-entry-mappings')
async def api_create_permission_file_entry(permission, entry_file):
    permission_file_entry = {
        'permission': permission,
        'entry_file': entry_file
    }
    saved = await objects.get_or_create(FileEntry, permission_file_entry)
    return 200, saved


# -----------------------------------user-group---------------------------
@feature(events.__FEATURE_ROUTING__, 'api_create_menu', 'api_create_menu')
@post('/api/operations')
async def api_create_operation(name, title, description):
    operation = {
        'name': name,
        'title': title,
        'description': description
    }
    saved = await objects.get_or_create(Operation, operation)
    return 200, saved


@feature(events.__FEATURE_ROUTING__, 'api_create_menu', 'api_create_menu')
@post('/api/permission-operation-mappings')
async def api_create_permission_operation(permission, operation):
    permission_operation = {
        'permission': permission,
        'operation': operation
    }
    saved = await objects.get_or_create(PermissionOperationMappings, permission_operation)
    return 200, saved
