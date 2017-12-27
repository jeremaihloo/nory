from datetime import datetime
from uuid import uuid4
from app_cores import app_fn
from peewee import CharField, UUIDField, DateTimeField, ForeignKeyField
from apps.core.models import User
from configs import NcmsConfig
from dbs import BaseModel, database
import events


class Role(BaseModel):
    id = UUIDField(primary_key=True, default=uuid4)
    name = CharField()
    description = CharField()
    created_at = DateTimeField(default=datetime.now)


class Permission(BaseModel):
    id = UUIDField(primary_key=True, default=uuid4)
    name = CharField(unique=True)
    description = CharField()
    created_at = DateTimeField(default=datetime.now)


class RolePermissionMappings(BaseModel):
    id = UUIDField(primary_key=True, default=uuid4)
    permission = ForeignKeyField(Permission)
    role = ForeignKeyField(Role)
    created_at = DateTimeField(default=datetime.now)


class UserRoleMappings(BaseModel):
    id = UUIDField(primary_key=True, default=uuid4)
    user = ForeignKeyField(User)
    role = ForeignKeyField(Role)
    created_at = DateTimeField(default=datetime.now)


class Menu(BaseModel):
    id = UUIDField(primary_key=True, default=uuid4)
    name = CharField(unique=True)
    title = CharField()
    icon = CharField()
    parent = ForeignKeyField('self', related_name='children')
    target = CharField()
    created_at = DateTimeField(default=datetime.now)


class RoleMenuMappings(BaseModel):
    id = UUIDField(primary_key=True, default=uuid4)
    role = ForeignKeyField(Role)
    menu = ForeignKeyField(Menu)
    created_at = DateTimeField(default=datetime.now)


@app_fn(events.__EVENT_ON_APP_INSTALLING__)
async def on_app_installing_init_db():
    database.create_tables([
        Role,
        Permission,
        RolePermissionMappings,
        UserRoleMappings,
        Menu,
        RoleMenuMappings
    ])
