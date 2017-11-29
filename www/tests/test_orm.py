import pytest

import aiorm
from configs import options
from apps.core.models import User

pytestmark = pytest.mark.asyncio


@pytestmark
async def test_new_orm(event_loop):
    database = aiorm.MySQLDataBase()
    await database.connect(event_loop, **options.db.to_dict())

    async with await database.atomic() as db:
        await db.execute('select * from tests')


@pytestmark
async def test_query(event_loop):
    database = aiorm.MySQLDataBase()
    await database.connect(event_loop, **options.db.to_dict())

    async with await database.atomic() as db:
        print((User.name == 'jeremaihloo'))
        print((User.created_at > '2017-03-19'))
        a = (User.name == 'jeremaihloo') & (User.created_at > '2017-03-19')
        print(a)
        r = aiorm.Query().select(User).where((User.name == 'jeremaihloo') & (User.created_at > '2017-03-19')).all()
        print(r)
        await db.execute(r)