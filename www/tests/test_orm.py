import pytest

import orm
from configs import options
from models import User, Content

pytestmark = pytest.mark.asyncio

@pytest.mark.asyncio
async def test_(event_loop):
    await orm.create_pool(event_loop, **options.db)
    pass


def test_eq():
    m = orm.Model()
    print(m == 2)


@pytest.mark.asyncio
async def test_attr(event_loop):
    await orm.create_pool(event_loop, **options.db)
    q = User.query().where(User.name == 10000)
    print(q)
    print(await q.one())


def test_fn():
    assert callable(Content)


@pytestmark
async def test_new_orm(event_loop):
    database = orm.MySQLDataBase()
    await database.connect(event_loop, **options.db.to_dict())

    async with await database.atomic() as db:
        await db.execute('select * from tests')


@pytestmark
async def test_query(event_loop):
    database = orm.MySQLDataBase()
    await database.connect(event_loop, **options.db.to_dict())

    async with await database.atomic() as db:
        print((User.name == 'jeremaihloo'))
        print((User.created_at > '2017-03-19'))
        a = (User.name == 'jeremaihloo') & (User.created_at > '2017-03-19')
        print(a)
        r = orm.Query().select(User).where((User.name == 'jeremaihloo') & (User.created_at > '2017-03-19')).all()
        print(r)
        await db.execute(r)