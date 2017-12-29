from datetime import datetime
from uuid import uuid4
from app_cores import app_fn
from peewee import CharField, UUIDField, DateTimeField, ForeignKeyField, TextField
from apps.core.models import User
from configs import NcmsConfig
from dbs import BaseModel, database
import events


class Role(BaseModel):
    id = UUIDField(primary_key=True, default=uuid4)
    name = CharField()
    description = CharField()
    created_at = DateTimeField(default=datetime.now)


class UserRoleMappings(BaseModel):
    id = UUIDField(primary_key=True, default=uuid4)
    user = ForeignKeyField(User)
    role = ForeignKeyField(Role)
    created_at = DateTimeField(default=datetime.now)


class UserGroup(BaseModel):
    id = UUIDField(primary_key=True, default=uuid4)
    name = CharField(unique=True)
    title = CharField()
    created_at = DateTimeField(default=datetime.now)


class UserGroupMappings(BaseModel):
    id = UUIDField(primary_key=True, default=uuid4)
    user = ForeignKeyField(User)
    group = ForeignKeyField(UserGroup)
    created_at = DateTimeField(default=datetime.now)


class UserGroupRoleMappings(BaseModel):
    id = UUIDField(primary_key=True, default=uuid4)
    group = ForeignKeyField(UserGroup)
    role = ForeignKeyField(Role)
    created_at = DateTimeField(default=datetime.now)


class Permission(BaseModel):
    id = UUIDField(primary_key=True, default=uuid4)
    name = CharField(unique=True)
    type = CharField()
    description = CharField()
    created_at = DateTimeField(default=datetime.now)


class RolePermissionMappings(BaseModel):
    id = UUIDField(primary_key=True, default=uuid4)
    permission = ForeignKeyField(Permission)
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


class PermissionMenuMappings(BaseModel):
    id = UUIDField(primary_key=True, default=uuid4)
    permission = ForeignKeyField(Permission)
    menu = ForeignKeyField(Menu)
    created_at = DateTimeField(default=datetime.now)


class PageDisplay(BaseModel):
    id = UUIDField(primary_key=True, default=uuid4)
    name = CharField(unique=True)
    title = CharField()
    description = TextField()
    created_at = DateTimeField(default=datetime.now)


class PermissionPageDisplayMappings(BaseModel):
    id = UUIDField(primary_key=True, default=uuid4)
    permission = ForeignKeyField(Permission)
    display = ForeignKeyField(PageDisplay)
    created_at = DateTimeField(default=datetime.now)


class FileEntry(BaseModel):
    id = UUIDField(primary_key=True, default=uuid4)
    name = CharField(unique=True)
    title = CharField()
    description = TextField()
    created_at = DateTimeField(default=datetime.now)


class PermissionFileMappings(BaseModel):
    id = UUIDField(primary_key=True, default=uuid4)
    permission = ForeignKeyField(Permission)
    file = ForeignKeyField(FileEntry)
    created_at = DateTimeField(default=datetime.now)


class Operation(BaseModel):
    id = UUIDField(primary_key=True, default=uuid4)
    name = CharField(unique=True)
    title = CharField()
    description = TextField()
    created_at = DateTimeField(default=datetime.now)


class PermissionOperationMappings(BaseModel):
    id = UUIDField(primary_key=True, default=uuid4)
    permission = ForeignKeyField(Permission)
    operation = ForeignKeyField(Operation)
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
