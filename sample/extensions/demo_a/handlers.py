import logging
from uuid import uuid4

from nory.infras.envs.configs import Configuration, Environment
from nory.infras.exts import features
from nory.infras.exts.contexts import FeatureContext
from nory.infras.exts.decorators import feature
from nory.infras.exts.managers import ExtensionManager
from nory.infras.web.decorators import get
from nory.infras.web.module_features import UseModule
from aiorm import Model, IntegerField, CharField, DbContext, DbSet, UUIDField


class DbConfig(Configuration):
    host = 'localhost'
    user = 'root'
    password = 'root'
    database = 'ncms'
    port = '3309'
    charset = 'utf8mb4'


class MainConfig(Configuration):
    default = 'msyql'
    mysql = DbConfig()


class DataBaseModule(UseModule):
    def initialize(self, app, _logger: logging.Logger, _ext_manager: ExtensionManager, env: Environment):
        config = DbConfig()
        env.configuration.option('db', config)


class Demo(Model):
    id = UUIDField(primary_key=True, default=uuid4)
    name = CharField()


class SampleDbContext(DbContext):
    demos = DbSet(Demo)


@feature(features.__FEATURE_ROUTING__, 'demo-a', 'demo-a')
@get('/')
async def get_demo(db: SampleDbContext):
    demo = Demo(name='jeremaihloo')
    await db.demos.add(demo)
    res = await db.fetch_all(db.demos.select_query())
    return res


@feature(features.__FEATURE_ON_APP_INSTALLING__, 'demo-install', 'demo-install')
async def create_data(context: FeatureContext):
    config = MainConfig()
    context.env.configuration.option('db', config)
    db = SampleDbContext(context.app.loop, **config)
    context.app.db['demo_a'] = db

    await db.begin()
    try:
        await db.drop_tables([Demo])
        await db.create_tables([Demo])
    except:
        pass
    await db.save_changes()
