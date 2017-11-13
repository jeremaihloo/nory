import pytest

import orm
from config import configs
from models import User, Content


@pytest.mark.asyncio
async def test_(event_loop):
    await orm.create_pool(event_loop, **configs.db)
    pass


def test_eq():
    m = orm.Model()
    print(m == 2)

@pytest.mark.asyncio
async def test_attr(event_loop):
    await orm.create_pool(event_loop, **configs.db)
    q = User.query().where(User.name == 10000)
    print(q)
    print(await q.one())

def test_fn():
    assert callable(Content)