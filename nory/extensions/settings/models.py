from datetime import datetime
from uuid import uuid4

from peewee import CharField, UUIDField, DateTimeField, TextField

from infrastructures.dbs import BaseModel, objects


class Setting(BaseModel):
    id = UUIDField(primary_key=True, default=uuid4)
    name = CharField()
    title = CharField()
    description = TextField()
    group = CharField()
    value = CharField()
    created_at = DateTimeField(default=datetime.now)


async def set(name, title, description, value, group):
    o, _ = await objects.create_or_get(Setting,
                                       name=name,
                                       title=title,
                                       description=description,
                                       value=value,
                                       group=group)
    return o


async def get(name, group):
    o = await objects.get(Setting, name=name, group=group)
    return o
