import logging
import time
import abc
import norm
import utils
from apps.core.models import next_id
from norm import Model, IntegerField, StringField, FloatField
import importlib
import os


class MigrationRecord(Model):
    __table__ = 'migrations'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    version = IntegerField()
    name = StringField(ddl='nvarchar(50)')
    created_at = FloatField(default=time.time)


class Migration(object, metaclass=abc.ABCMeta):
    def __init__(self, version, name):
        self.version = version
        self.name = name
        self.lines = []

        self.builder = MigrationBuilder(version, name)

    @abc.abstractclassmethod
    async def do(self):
        pass

    @abc.abstractclassmethod
    async def undo(self):
        pass

    def __str__(self):
        return str(self.builder)


class MigrationBuilder(object):
    def __init__(self, version, name):
        self.version = version
        self.name = name
        self.lines = []

    def add_tables(self, models, force=False):
        if force:
            self.drop_tables(models, safe=False)
        sqls = [self.build_create_table_sql(x) for x in models]
        self.lines.append({
            'action': 'add_tables',
            'sqls': ';\n'.join(sqls)
        })
        return self

    def drop_tables(self, models, safe=True):
        sqls = [self.build_drop_table_sql(x, safe=safe) for x in models]
        self.lines.append({
            'action': 'drop_tables',
            'sqls': ';\n'.join(sqls)
        })
        return self

    def alter_tables(self, models):
        pass

    def __str__(self):
        sql = []
        for line in self.lines:
            sql.append(line['sqls'])
        return ';\n'.join(sql)

    def build_create_table_sql(self, model: Model):
        sqls = []
        for key, val in model.__mappings__.items():
            ddl = val.ddl if hasattr(val, 'ddl') else val.column_type
            field_sql = "{name} {ddl}".format(name=key, ddl=ddl)
            sqls.append(field_sql)
        return 'create table ' + model.__table__ + ' \n(\n\t' + ',\n\t'.join(sqls) + '\n)'

    def build_drop_table_sql(self, model: Model, safe=True):
        new_table = '{table}_bk_{version}'.format(table=model.__table__, version=self.version)
        bk_sql = """CREATE TABLE {new_table}(SELECT *FROM {old_table})""".format(new_table=new_table,
                                                                                 old_table=model.__table__)
        drop_sql = 'DROP TABLE IF EXISTS {table}'.format(table=model.__table__)
        return ';\n'.join([bk_sql, drop_sql]) if safe else drop_sql


class MigrationError(Exception):
    def __init__(self, message):
        super(MigrationError, self).__init__(message)
        self.message = message


async def do_local_migrations(db):
    logging.info('start do local migrations')
    r = await db.select('show tables', None)
    tables = map(lambda x: x['Tables_in_ncms'], r)
    if 'migrations' not in tables:
        mbuilder = MigrationBuilder(0, 'migrations')
        migration_table_sql = mbuilder.build_create_table_sql(MigrationRecord)
        await db.execute(migration_table_sql)
    abs_p = utils.get_ncms_path()
    db_migrations_file_names = os.listdir(os.path.join(abs_p, 'migrations'))
    file_names = list(filter(lambda x: x.startswith('migration'), db_migrations_file_names))
    file_names = list(map(lambda x: x[:-3], file_names))

    ms = []
    for file_name in file_names:
        migration = importlib.import_module('migrations.{}'.format(file_name))
        classes_names = list(filter(lambda x: x.startswith('Migration') and (not x == 'Migration'), dir(migration)))
        classes = list(map(lambda key: getattr(migration, key), classes_names))

        ms.extend(classes)

    ms = [x() for x in ms if issubclass(x, Migration)]

    logging.info('collected {} migrations'.format(len(ms)))

    # sort
    sorted(ms, key=lambda x: x.version)

    await do_migrations(ms, db)


async def do_migrations(migrations, db):
    for item in migrations:
        logging.info('do migration version: {} name: {}'.format(item.version, item.name))
        try:
            fr = await db.select(norm.Query().select(MigrationRecord).where(MigrationRecord.name == item.name).all())
            if fr is not None and len(list(fr)) > 0:
                raise MigrationError(message='migration may be excuted ! name: {}'.format(item.name))
            item.do()
            await db.execute(str(item))
        except Exception as e:
            logging.error('migration error : {}'.format((str(e))))


async def undo_migrations(migrations, db):
    for item in migrations:
        try:
            fr = await db.select(norm.Query().select(MigrationRecord).where(MigrationRecord.name == item.name).all())
            if fr is not None and len(list(fr)) > 0:
                raise MigrationError(message='migration may be excuted ! name: {}'.format(item.name))
            item.undo()
            await db.execute(str(item))
        except Exception as e:
            logging.error('migration error : {}'.format((str(e))))
