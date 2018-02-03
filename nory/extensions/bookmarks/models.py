from datetime import datetime
from uuid import uuid4

from peewee import UUIDField, ForeignKeyField, TextField, BooleanField, DateTimeField, IntegerField

from extensions.article.models import User, Tag
from extensions.rbacm.models import UserGroup
from infrastructures.dbs import BaseModel

VISIABLE_TO_PUBLIC = 'VISIABLE_TO_PUBLIC'


class Bookmark(BaseModel):
    id = UUIDField(primary_key=True, default=uuid4)
    user = ForeignKeyField(User, related_name='bookmarks')
    title = TextField()
    url = TextField()
    visiable_to = TextField(default=VISIABLE_TO_PUBLIC)
    enabled = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.now)


class BookmarkTagMappings(BaseModel):
    id = UUIDField(primary_key=True, default=uuid4)
    bookmark = ForeignKeyField(Bookmark)
    tag = ForeignKeyField(Tag)
    enabled = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.now)


class BookmarkGroupMappings(BaseModel):
    id = UUIDField(primary_key=True, default=uuid4)
    bookmark = ForeignKeyField(Bookmark)
    group = ForeignKeyField(UserGroup)
    enabled = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.now)


class BookmarkUserStar(BaseModel):
    id = UUIDField(primary_key=True, default=uuid4)
    bookmark = ForeignKeyField(Bookmark)
    user = ForeignKeyField(User)
    enabled = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.now)


class BookmarkVote(BaseModel):
    id = UUIDField(primary_key=True, default=uuid4)
    bookmark = ForeignKeyField(Bookmark)
    vote = IntegerField(choices=(-1, 1))
    user = ForeignKeyField(User)
    reason = TextField()
    enabled = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.now)
