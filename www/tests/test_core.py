import unittest

import pytest

import handlers
import aiorm
from configs import options
from migrations_core import do_local_migrations


@pytest.mark.asyncio
async def reinit_dbs():
    await do_local_migrations()




