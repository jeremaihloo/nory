import events
from app_cores import app_fn
from apps.rbacm.models import Role, Menu, UserMenuMappings, UserRoleMappings
from coroweb import post


@app_fn(events.__EVENT_ROUTING__, 'api_create_role', 'api_create_role')
@post('/api/roles')
async def api_create_role(name, title, desc, menus):
    role = Role()
    role.name = name
    role.title = title
    role.description = desc
    await role.save()


@app_fn(events.__EVENT_ROUTING__, 'api_create_menu', 'api_create_menu')
@post('/api/menus')
async def api_create_menu(name, title, icon, parent, target):
    menu = Menu()
    menu.name = name
    menu.title = title
    menu.icon = icon
    menu.parent = parent
    menu.target = target
    await menu.save()
    return {

    }


@app_fn(events.__EVENT_ROUTING__, 'api_create_user_role_mapping', 'api_create_user_role_mapping')
@post('/api/user-role-mappings')
async def api_create_user_role_mapping(user_id, role):
    mapping = UserRoleMappings()
    mapping.user_id = user_id
    mapping.role = role
    await mapping.save()
    return {

    }


@app_fn(events.__EVENT_ROUTING__, 'api_create_user_role_mapping', 'api_create_user_role_mapping')
@post('/api/user-menu-mappings')
async def api_create_user_role_mapping(user_id, menu):
    mapping = UserMenuMappings()
    mapping.user_id = user_id
    mapping.menu = menu
    await mapping.save()
    return {

    }
