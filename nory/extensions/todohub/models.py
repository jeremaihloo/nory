from datetime import datetime
from uuid import uuid4

from peewee import UUIDField, DateTimeField

from infrastructures.dbs import BaseModel
from infrastructures.norms.coros import IntegerField, BooleanField, TextField


class TotoItemFormula(BaseModel):
    id = UUIDField(primary_key=True, default=uuid4)
    title = TextField()
    description = TextField()
    content = TextField()
    created_at = DateTimeField(default=datetime.now)


class TodoItem(BaseModel):
    id = UUIDField(primary_key=True, default=uuid4)
    title = TextField()
    description = TextField()
    type = IntegerField()
    created_at = DateTimeField(default=datetime.now)


class TodoItemVersion(BaseModel):
    id = UUIDField(primary_key=True, default=uuid4)
    title = TextField()
    description = TextField()
    created_at = DateTimeField(default=datetime.now)
