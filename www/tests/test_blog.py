import pytest

import handlers
import norm
from configs import options
from migrations_core import do_local_migrations
from apps.core.models import User


@pytest.mark.asyncio
async def test_blog(event_loop):
    pass
