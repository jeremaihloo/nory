import app_cores
from app_cores import app_fn

__author__ = 'jeremaihloo'

__version__ = '0.0.1'

__description__ = 'provide jwt auth'

__home_page__ = 'https://github.com/jeremaihloo/ncms-rbacm'

__permissions__ = [
    'DB'
]

__user_agreement__ = """

"""

import time
from models import next_id
from orm import Model, StringField, FloatField
from coroweb import post


class Role(Model):
    __table__ = 'roles'

    name = StringField(primary_key=True, ddl='varchar(50)')
    title = StringField(ddl='varchar(50)')
    description = StringField(ddl='varchar(50)')
    created_at = FloatField(default=time.time)


class Permission(Model):
    __table__ = 'permissions'

    name = StringField(primary_key=True, ddl='varchar(50)')
    created_at = FloatField(default=time.time)


class RolePemissionMappings(Model):
    __table__ = 'role_pemission_mappings'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    permission = StringField(ddl='varchar(50)')
    role = StringField(ddl='varchar(50)')
    created_at = FloatField(default=time.time)


class UserRoleMappings(Model):
    __table__ = 'user_role_mappings'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    user_id = StringField(ddl='varchar(50)')
    role = StringField(ddl='varchar(50)')
    created_at = FloatField(default=time.time)


class Menu(Model):
    __table__ = 'menus'

    name = StringField(primary_key=True, ddl='varchar(50)')
    title = StringField(ddl='varchar(50)')
    icon = StringField(ddl='varchar(50)')
    parent = StringField(ddl='varchar(50)')
    target = StringField(ddl='varchar(50)')
    created_at = FloatField(default=time.time)


class UserMenuMappings(Model):
    __table__ = 'user_menu_mappings'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    user_id = StringField(ddl='varchar(50)')
    menu = StringField(ddl='varchar(50)')
    created_at = FloatField(default=time.time)


@app_fn(app_cores.__EVENT_ROUTING__, 'get_plugins', 'get plugin infos')
@post('/api/roles')
async def api_create_role(name, title, desc):
    role = Role()
    role.name = name
    role.title = title
    role.description = desc
    await role.save()
    return {

    }


@app_fn(app_cores.__EVENT_ROUTING__, 'get_plugins', 'get plugin infos')
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


@app_fn(app_cores.__EVENT_ROUTING__, 'get_plugins', 'get plugin infos')
@post('/api/user-role-mappings')
async def api_create_user_role_mapping(user_id, role):
    mapping = UserRoleMappings()
    mapping.user_id = user_id
    mapping.role = role
    await mapping.save()
    return {

    }


@app_fn(app_cores.__EVENT_ROUTING__, 'get_plugins', 'get plugin infos')
@post('/api/user-menu-mappings')
async def api_create_user_role_mapping(user_id, menu):
    mapping = UserMenuMappings()
    mapping.user_id = user_id
    mapping.menu = menu
    await mapping.save()
    return {

    }


async def on_install():
    pass


async def on_uninstall():
    pass
