import logging

logging.basicConfig(level=logging.DEBUG)
import norm
from configs import options
from migrations_core import do_local_migrations
import pytest


@pytest.mark.asyncio
async def test_do_local_migrations(event_loop):
    await norm.create_pool(event_loop, **configs.db)
    await do_local_migrations()
