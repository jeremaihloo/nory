import asyncio
import pytest


@pytest.mark.asyncio
async def test_1():
    await asyncio.sleep(2)


@pytest.mark.asyncio
async def test_2():
    await asyncio.sleep(2)