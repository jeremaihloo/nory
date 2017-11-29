import unittest

import pytest

import handlers
import orm
from configs import configs
from migrations_core import do_local_migrations


@pytest.mark.asyncio
async def reinit_dbs():
    await do_local_migrations()


@pytest.mark.asyncio
async def test_create_content_type(event_loop):
    await orm.create_pool(event_loop, **configs.db)
    await reinit_dbs()

    content_type = await handlers.api_create_content_type(name='Integer', title='Integer')
    assert content_type is not None
    content_type = await handlers.api_create_content_type(name='String', title='String')
    assert content_type is not None
    content_type = await handlers.api_create_content_type(name='CreatedAt', title='Created At')
    assert content_type is not None
    content_type = await handlers.api_create_content_type(name='UpdateAt', title='UpdateAt')
    assert content_type is not None
    content_type = await handlers.api_create_content_type(name='NextId', title='Next id')
    assert content_type is not None
    content_type = await handlers.api_create_content_type(name='Text', title='Text')
    assert content_type is not None


@pytest.mark.asyncio
async def test_create_field(event_loop):
    await orm.create_pool(event_loop, **configs.db)
    field = await handlers.api_create_content_field(name='name', title='Name', field_type='String')
    assert field is not None
    await orm.create_pool(event_loop, **configs.db)
    field = await handlers.api_create_content_field(name='content', title='Content', field_type='Text')
    assert field is not None
    await orm.create_pool(event_loop, **configs.db)
    field = await handlers.api_create_content_field(name='created_at', title='Created At', field_type='CreatedAt')
    assert field is not None


@pytest.mark.asyncio
async def test_create_model(event_loop):
    await orm.create_pool(event_loop, **configs.db)
    content_type = await handlers.api_create_content_model(name='article', title='Article',
                                                           fields=('name', 'content', 'created_at'))
    assert content_type is not None
    print(content_type)


@pytest.mark.asyncio
async def test_create_content(event_loop):
    await orm.create_pool(event_loop, **configs.db)
    content_type = await handlers.api_create_content(model_name='article', data={
        'name': 'hello world',
        'content': 'this is hello world article content !',
        'created_at': '2017-08-09 12:20:40'
    })
    assert content_type is not None


@pytest.mark.asyncio
async def test_get_contents(event_loop):
    await orm.create_pool(event_loop, **configs.db)
    contents = await handlers.api_get_contents(model_name='article')
    assert contents is not None
    print(contents)



