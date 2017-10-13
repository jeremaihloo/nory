import asyncio
import time

import orm
from models import next_id
from orm import Model, execute, IntegerField, TextField, StringField, FloatField
import importlib
import os


class Migration(Model):
    __table__ = 'migrations'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    version = IntegerField()
    name = StringField(ddl='nvarchar(50)')
    created_at = FloatField(default=time.time)


class MigrationBuilder(object):
    def __init__(self, version, name):
        self.version = version
        self.name = name
        self.lines = []

    def add_tables(self, models):
        sqls = [self.build_create_table_sql(x) for x in models]
        self.lines.append({
            'action': 'add_tables',
            'sqls': ';'.join(sqls)
        })
        return self

    def drop_tables(self, models, safe=True):
        sqls = [self.build_drop_table_sql(x) for x in models]
        self.lines.append({
            'action': 'drop_tables',
            'sqls': ';\n'.join(sqls)
        })
        return self

    def alter_tables(self, models):
        pass

    @asyncio.coroutine
    def do(self):
        sql = []
        for line in self.lines:
            sql.append(line['sqls'])
        yield from execute(';\n'.join(sql))

    def build_create_table_sql(self, model: Model):
        sqls = []
        for key, val in model.__mappings__.items():
            ddl = val.ddl if hasattr(val, 'ddl') else val.column_type
            field_sql = "{name} {ddl}".format(name=key, ddl=ddl)
            sqls.append(field_sql)
        return 'create table ' + model.__table__ + ' \n(\n\t' + ',\n\t'.join(sqls) + '\n)'

    def build_drop_table_sql(self, model: Model, safe=True):
        new_table = '{table}_bk_{version}'.format(table=model.__table__, version=self.version)
        bk_sql = ''' 
                create
                table
                {new_table}(select *
                from {old_table});
            '''.format(new_table=new_table, old_table=model.__table__)
        drop_sql = 'drop table {table};'.format(table=model.__table__)
        return ';\n'.join([bk_sql, drop_sql])


class MigrationError(Exception):
    def __init__(self, message):
        super(MigrationError, self).__init__(message)
        self.message = message


@asyncio.coroutine
def db_migrations():
    r = yield from orm.select('show tables', None)
    tables = map(lambda x: x['Tables_in_ncms'], r)
    if 'migrations' not in tables:
        mbuilder = MigrationBuilder(0, 'migrations')
        migration_table_sql = mbuilder.build_create_table_sql(Migration)
        yield from orm.execute(migration_table_sql)

    db_migrations_file_names = os.listdir('do_migrations')
    file_names = list(filter(lambda x:x.startswith('migration'), db_migrations_file_names))
    file_names = list(map(lambda x:x[:-3], file_names))

    builders = []
    for file_name in file_names:
        migration = importlib.import_module('do_migrations.{}'.format(file_name))
        builders.append(migration.create_builder())

    for item in builders:
        fr = yield from Migration.findAll(where='name = ?', args=(item.name,))
        if fr is not None and len(list(fr)) > 0:
            raise MigrationError(message='migration may be excuted ! name: {}'.format(item.name))
        yield from item.do()