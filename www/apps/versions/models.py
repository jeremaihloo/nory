from datetime import datetime
from uuid import uuid4

from peewee import UUIDField, BooleanField, DateTimeField, IntegerField, TextField

from infrastructures.dbs import BaseModel


class Version(BaseModel):
    id = UUIDField(primary_key=True, default=uuid4)
    app = TextField()
    ncms_version = IntegerField(unique=True)
    app_version = IntegerField(unique=True)
    enabled = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.now)

