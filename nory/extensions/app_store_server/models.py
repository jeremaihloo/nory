from datetime import datetime
from uuid import uuid4

from peewee import UUIDField, ForeignKeyField, BooleanField, DateTimeField, TextField, CharField

from extensions.article.models import User
from infrastructures.dbs import BaseModel


class AppIndexItem(BaseModel):
    id = UUIDField(primary_key=True, default=uuid4)
    user = ForeignKeyField(User, related_name='app_index_items')
    name = CharField()
    description = TextField()
    info = TextField()
    published = BooleanField(default=False)
    enabled = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.now)
