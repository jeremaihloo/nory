from infrastructures.norms.coros import execute
import logging

_logger = logging.getLogger('norms')


async def show_tables():
    pass


async def create_tables(tables, safe=True):
    def get_create_table_sql():
        for item in tables:
            args = []
            for f_name, f in getattr(item, '__mappings__').items():
                args.append(str(f))
            sql = 'CREATE TABLE {} ({})'.format(getattr(item, '__table__'), ',\n\t'.join(args))
            yield sql

    sqls = list(get_create_table_sql())
    try:
        await execute('\n'.join(sqls))
    except Exception as e:
        _logger.exception(e)
        if not safe:
            raise Exception('Create Table Error')


async def drop_tables(tables, safe=True):
    def get_drop_table_sql():
        for item in tables:
            sql = 'DROP TABLE {}'.format(getattr(item, '__table__'))
            yield sql

    sqls = list(get_drop_table_sql())
    try:
        await execute('\n'.join(sqls))
    except Exception as e:
        _logger.exception(e)
        if not safe:
            raise Exception('Create Table Error')


async def add_table_column(table, column_name, column_type, column_default):
    pass
