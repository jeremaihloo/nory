import unittest

import pytest

import handlers
import orm
from config import configs

@pytest.mark.asyncio
async def test_create_content_type(event_loop):
    await orm.create_pool(event_loop, **configs.db)
    content_type = await handlers.api_create_content_type(name='name', title='Name')
    assert content_type is not None
    print(content_type)

@pytest.mark.asyncio
async def test_create_field(event_loop):
    await orm.create_pool(event_loop, **configs.db)
    content_type = await handlers.api_create_content_field(name='name', title='Name')
    assert content_type is not None
    print(content_type)

@pytest.mark.asyncio
async def test_create_model(event_loop):
    await orm.create_pool(event_loop, **configs.db)
    content_type = await handlers.api_create_content_type(name='name', title='Name')
    assert content_type is not None
    print(content_type)

@pytest.mark.asyncio
async def test_create_content(event_loop):
    await orm.create_pool(event_loop, **configs.db)
    content_type = await handlers.api_create_content_type(name='name', title='Name')
    assert content_type is not None
    print(content_type)