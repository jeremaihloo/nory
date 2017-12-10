from datetime import datetime
from uuid import uuid4

import events
from app_cores import app_fn
from peewee import CharField, UUIDField, DateTimeField, ForeignKeyField
from apps.core.models import User
from coroweb import post
from dbs import BaseModel


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


class UserMenuMappings(BaseModel):
    id = UUIDField(primary_key=True, default=uuid4)
    user = ForeignKeyField(User)
    menu = ForeignKeyField(Menu)
    created_at = DateTimeField(default=datetime.now)
