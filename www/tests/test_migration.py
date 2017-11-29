import logging

logging.basicConfig(level=logging.DEBUG)
import orm
from configs import configs
from migrations_core import do_local_migrations
import pytest


@pytest.mark.asyncio
async def test_do_local_migrations(event_loop):
    await orm.create_pool(event_loop, **configs.db)
    await do_local_migrations()
