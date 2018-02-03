import asyncio
import pytest

from infrastructures.dbs import objects


@pytest.mark.asyncio
async def test_1():
    await objects


@pytest.mark.asyncio
async def test_2():
    await asyncio.sleep(2)