import unittest
import pytest

import norm
from apps.core.models import User, UserProfile
from configs import options

pytestmark = pytest.mark.asyncio


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)


@pytestmark
async def test_insert(event_loop):
    database = norm.MySQLDataBase()
    await database.connect(event_loop, **options.db.to_dict())

    async with await database.atomic() as db:
        user = User()
        user.name = 'lujiejie'
        user.passwd = '******'
        await db.create(user)
        user_profile = UserProfile()
        user_profile.user_id = user.id
        user_profile.nick_name = 'jiejie'
        await db.create(user_profile)


@pytestmark
async def test_query(event_loop):
    database = norm.MySQLDataBase()
    await database.connect(event_loop, **options.db.to_dict())

    async with await database.atomic() as db:
        users = await db.select(norm.Query().select(User).all())
        print(users)
        assert users is not None and len(users) > 0

@pytestmark
async def test_query(event_loop):
    database = norm.MySQLDataBase()
    await database.connect(event_loop, **options.db.to_dict())

    async with await database.atomic() as db:
        users = await db.select(norm.Query().select(User).all())
        print(users)
        assert users is not None and len(users) > 0
        user = users[0]
        user.name = 'lujiejie----111'
        await db.update(user)