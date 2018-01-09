import peewee_async
from peewee import Model
from infrastructures.configs.models import DbConfig

database = peewee_async.MySQLDatabase(DbConfig.db_database, host=DbConfig.db_host, user=DbConfig.db_user,
                                      password=DbConfig.db_password, charset='utf8mb4')
objects = peewee_async.Manager(database)


class BaseModel(Model):
    class Meta:
        database = database
