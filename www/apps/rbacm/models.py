from datetime import datetime
from uuid import uuid4
from app_cores import feature
from peewee import CharField, UUIDField, DateTimeField, ForeignKeyField, TextField
from apps.article.models import User
from dbs import BaseModel, database
import events


class Role(BaseModel):
    id = UUIDField(primary_key=True, default=uuid4)
    name = CharField()
    title = CharField()
    description = CharField(null=True)
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
    description = CharField(null=True)
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
    title = CharField()
    type = CharField()
    description = CharField(null=True)
    created_at = DateTimeField(default=datetime.now)


class PermissionRoleMappings(BaseModel):
    id = UUIDField(primary_key=True, default=uuid4)
    permission = ForeignKeyField(Permission)
    role = ForeignKeyField(Role)
    created_at = DateTimeField(default=datetime.now)


class Menu(BaseModel):
    id = UUIDField(primary_key=True, default=uuid4)
    name = CharField(unique=True)
    title = CharField()
    description = CharField(null=True)
    icon = CharField(null=True)
    parent = ForeignKeyField('self', related_name='children', null=True)
    href = CharField()
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
    description = TextField(null=True)
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
    description = TextField(null=True)
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
    description = TextField(null=True)
    url_pattern = CharField()
    created_at = DateTimeField(default=datetime.now)


class PermissionOperationMappings(BaseModel):
    id = UUIDField(primary_key=True, default=uuid4)
    permission = ForeignKeyField(Permission)
    operation = ForeignKeyField(Operation)
    created_at = DateTimeField(default=datetime.now)


rbacm_models = [
    Role,
    UserRoleMappings,
    UserGroup,
    UserGroupMappings,
    UserGroupRoleMappings,
    Permission,
    PermissionRoleMappings,
    Menu,
    PermissionMenuMappings,
    PageDisplay,
    PermissionPageDisplayMappings,
    FileEntry,
    PermissionFileMappings,
    Operation,
    PermissionOperationMappings
]


@feature(events.__FEATURE_ON_APP_INSTALLING__)
async def on_app_installing_init_db():
    global rbacm_models
    database.create_tables(rbacm_models)
