import app_cores
from app_cores import app_fn
import time

from migrations_core import Migration, do_migrations, undo_migrations
from apps.core.models import next_id
from norm import Model, StringField, FloatField
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


class MigrationsRbacm(Migration):
    def __init__(self):
        self.version = 2
        self.name = 'rbacm'
        self.models = [Role, Permission, RolePemissionMappings, UserRoleMappings, Menu, UserMenuMappings]

        super(MigrationsRbacm, self).__init__(version=self.version, name=self.name)

    def do(self):
        self.builder.add_tables(self.models)

    def undo(self):
        self.builder.drop_tables(self.models)


async def on_install():
    await do_migrations([MigrationsRbacm()])


async def on_uninstall():
    await undo_migrations([MigrationsRbacm()])
