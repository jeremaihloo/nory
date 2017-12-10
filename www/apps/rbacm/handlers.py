import events
from app_cores import app_fn
from apps.rbacm.models import Role, Menu, UserMenuMappings, UserRoleMappings
from coroweb import post


@app_fn(events.__EVENT_ROUTING__, 'get_plugins', 'get plugin infos')
@post('/api/roles')
async def api_create_role(name, title, desc):
    role = Role()
    role.name = name
    role.title = title
    role.description = desc
    await role.save()
    return {

    }


@app_fn(events.__EVENT_ROUTING__, 'get_plugins', 'get plugin infos')
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


@app_fn(events.__EVENT_ROUTING__, 'get_plugins', 'get plugin infos')
@post('/api/user-role-mappings')
async def api_create_user_role_mapping(user_id, role):
    mapping = UserRoleMappings()
    mapping.user_id = user_id
    mapping.role = role
    await mapping.save()
    return {

    }


@app_fn(events.__EVENT_ROUTING__, 'get_plugins', 'get plugin infos')
@post('/api/user-menu-mappings')
async def api_create_user_role_mapping(user_id, menu):
    mapping = UserMenuMappings()
    mapping.user_id = user_id
    mapping.menu = menu
    await mapping.save()
    return {

    }
