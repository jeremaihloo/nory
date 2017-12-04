import asyncio

import peewee_async
from peewee import Model
from configs import options

print(options.db.to_dict())
database = peewee_async.MySQLDatabase('ncms', user=options.db.user, password=options.db.password)
objects = peewee_async.Manager(database)


class BaseModel(Model):
    class Meta:
        database = database
