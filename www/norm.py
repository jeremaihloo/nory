#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime, date, time
from functools import wraps

__author__ = 'Michael Liao'

import logging

import aiomysql


class _aio_callable_context_manager(object):
    __slots__ = ()

    def __call__(self, fn):
        @wraps(fn)
        async def inner(*args, **kwargs):
            async with self:
                return fn(*args, **kwargs)

        return inner


class _aio_db_context_manager(_aio_callable_context_manager):

    def __init__(self, conn):
        self.conn = conn
        self.cursor = None

    async def __aenter__(self):
        await self.conn.__aenter__()
        await self.conn._conn.begin()
        self.cursor = await self.conn._conn.cursor(aiomysql.DictCursor)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.cursor.close()
        await self.conn._conn.commit()
        await self.conn.__aexit__(exc_type, exc_val, exc_tb)


class DataBase(object):
    pass


class MySqlDbOperator(_aio_db_context_manager):
    def __init__(self, conn):
        super(MySqlDbOperator, self).__init__(conn)

    async def execute(self, sql, args=None):
        await self.cursor.execute(sql.replace('?', '%s'), args)
        affected = self.cursor.rowcount
        await self.cursor.close()
        return affected

    async def select(self, sql, args=None):
        await self.cursor.execute(sql.replace('?', '%s'), args or ())
        rs = await self.cursor.fetchall()
        return rs


class MySQLDataBase(object):
    def __init__(self, **kw):
        self.__pool = None

    async def _connect(self, loop, **kw):
        self.__pool = await aiomysql.create_pool(
            host=kw.get('host', 'localhost'),
            port=kw.get('port', 3306),
            user=kw['user'],
            password=kw['password'],
            db=kw['db'],
            charset=kw.get('charset', 'utf8'),
            # autocommit=kw.get('autocommit', True),
            maxsize=kw.get('maxsize', 10),
            minsize=kw.get('minsize', 1),
            loop=loop
        )

    async def connect(self, loop, **kw):
        await self._connect(loop, **kw)

    async def atomic(self) -> MySqlDbOperator:
        return MySqlDbOperator(self.__pool.acquire())


database = MySQLDataBase()


def create_args_string(num):
    L = []
    for n in range(num):
        L.append('?')
    return ', '.join(L)


class Field(object):
    def __init__(self, name, column_type, primary_key, default, unique):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default
        self.unique = unique

    def __str__(self):
        return '<%s, %s:%s>' % (self.__class__.__name__, self.column_type, self.name)


class StringField(Field):
    def __init__(self, name=None, primary_key=False, default=None, ddl='varchar(100)', unique=False):
        super().__init__(name, ddl, primary_key, default, unique)


class BooleanField(Field):
    def __init__(self, name=None, default=False):
        super().__init__(name, 'boolean', False, default)


class IntegerField(Field):
    def __init__(self, name=None, primary_key=False, default=0):
        super().__init__(name, 'bigint', primary_key, default, False)


class FloatField(Field):
    def __init__(self, name=None, primary_key=False, default=0.0, unique=False):
        super().__init__(name, 'real', primary_key, default, unique)


class TextField(Field):
    def __init__(self, name=None, default=None):
        super().__init__(name, 'text', False, default, False)


class RelationField(Field):
    def __init__(self, model):
        self.model = model


class OneField(RelationField):
    def __init__(self, model):
        super(OneField, self).__init__(model)


class ManyField(RelationField):
    def __init__(self, model):
        super(ManyField, self).__init__(model)


class ForeignField(RelationField):
    def __init__(self, model):
        super(ForeignField, self).__init__(model)


class ModelMetaclass(type):
    def __getattr__(self, item):
        return QueryImpl(left='{}.{}'.format(getattr(self, '__table__'), item))

    def __new__(cls, name, bases, attrs):
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)
        tableName = attrs.get('__table__', None) or name
        logging.info('found model: %s (table: %s)' % (name, tableName))
        mappings = dict()
        fields = []
        primaryKey = None
        for k, v in attrs.items():
            if isinstance(v, Field):
                logging.info('--> found mapping: %s ==> %s' % (k, v))
                mappings[k] = v
                if v.primary_key:
                    # 找到主键:
                    if primaryKey:
                        raise StandardError('Duplicate primary key for field: %s' % k)
                    primaryKey = k
                else:
                    fields.append(k)

        if not primaryKey:
            raise StandardError('Primary key not found.')
        for k in mappings.keys():
            attrs.pop(k)
        escaped_fields = list(map(lambda f: '`%s`' % f, fields))
        attrs['__mappings__'] = mappings  # 保存属性和列的映射关系
        attrs['__table__'] = tableName
        attrs['__primary_key__'] = primaryKey  # 主键属性名
        attrs['__fields__'] = fields  # 除主键外的属性名
        attrs['__select__'] = 'select `%s`, %s from `%s`' % (primaryKey, ', '.join(escaped_fields), tableName)
        attrs['__insert__'] = 'insert into `%s` (%s, `%s`) values (%s)' % (
            tableName, ', '.join(escaped_fields), primaryKey, create_args_string(len(escaped_fields) + 1))
        attrs['__update__'] = 'update `%s` set %s where `%s`=?' % (
            tableName, ', '.join(map(lambda f: '`%s`=?' % (mappings.get(f).name or f), fields)), primaryKey)
        attrs['__delete__'] = 'delete from `%s` where `%s`=?' % (tableName, primaryKey)
        return type.__new__(cls, name, bases, attrs)


class Model(dict, metaclass=ModelMetaclass):
    def __init__(self, **kw):
        super(Model, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    def getValue(self, key):
        return getattr(self, key, None)

    def getValueOrDefault(self, key):
        value = getattr(self, key, None)
        if value is None:
            field = self.__mappings__[key]
            if field.default is not None:
                value = field.default() if callable(field.default) else field.default
                logging.debug('using default value for %s: %s' % (key, str(value)))
                setattr(self, key, value)
        return value


def pre_other(o):
    if isinstance(o, QueryImpl):
        return o
    elif isinstance(o, str) or isinstance(o, datetime) or isinstance(o, date) or isinstance(o, time):
        return "'{}'".format(o)


class QueryImpl(object):
    def __init__(self, left=None, op=None, right=None):
        self.left = left
        self.op = op
        self.right = right

    def __str__(self):
        strs = []
        if isinstance(self.left, QueryImpl):
            strs.append('(')

        if self.left:
            strs.append(str(self.left))
        if self.op:
            strs.append(self.op)
        if self.right:
            strs.append(str(self.right))

        if isinstance(self.left, QueryImpl):
            strs.append(')')

        return ' '.join(strs)

    def __eq__(self, other):
        return QueryImpl(self, '=', pre_other(other))

    def __le__(self, other):
        return QueryImpl(self, '<=', pre_other(other))

    def __ge__(self, other):
        return QueryImpl(self, '>=', pre_other(other))

    def __lt__(self, other):
        return QueryImpl(self, '<', pre_other(other))

    def __gt__(self, other):
        return QueryImpl(self, '>', pre_other(other))

    def __and__(self, other):
        return QueryImpl(left=self, op='and', right=pre_other(other))

    def __or__(self, other):
        return QueryImpl(left=self, op='or', right=pre_other(other))


class SelectQuery(object):
    def __init__(self, model):
        self.model = model

    def __str__(self):
        return "SELECT * FROM {}".format(getattr(self.model, '__table__'))


class OrderByImpl(object):
    pass


class Query(object):
    def __init__(self, db_op=None, model=None):
        self.db_op = db_op
        self.query_method = None
        self._where = None
        self._orderby = []
        self._limit = 0
        self._offset = 0
        self.model = model

    def select(self, model):
        self.model = model
        self.query_method = SelectQuery(model)
        return self

    def where(self, query_impl):
        print(query_impl)
        self._where = self._where and query_impl if self._where else query_impl
        return self

    def order_by_asc(self, model_field):
        self._orderby.append('{} asc'.format(pre_other(model_field)))

    def order_by_desc(self, model_field):
        self._orderby.append('{} desc'.format(pre_other(model_field)))

    def _str_select(self):
        return '{select} WHERE {where} ORDER BY {orderby} LIMIT {limit} OFFSET {offset}'.format(
            select=self.query_method,
            where=self._where,
            orderby='{}.created_at desc'.format(getattr(self.model, '__table__')) if len(self._orderby) == 0 else ' and '.join(self._orderby),
            limit=self._limit,
            offset=self._offset)

    def __str__(self):
        if isinstance(self.query_method, SelectQuery):
            return self._str_select()

    def one(self):
        pass

    def all(self):
        return self.__str__()

    def execute(self):
        pass

        # db.query().select(User).where(User.name == 'jeremaihloo').one()
        # db.query().select(User).where(User.name == 'jeremaihloo').all()
