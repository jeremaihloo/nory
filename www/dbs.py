
import peewee_async
from peewee import Model
from configs import NcmsConfig

database = peewee_async.MySQLDatabase(NcmsConfig.db_database, user=NcmsConfig.db_user, password=NcmsConfig.db_password)
objects = peewee_async.Manager(database)


class BaseModel(Model):
    class Meta:
        database = database

