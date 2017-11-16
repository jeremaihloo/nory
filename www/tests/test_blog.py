import pytest

import handlers
import orm
from config import configs
from migrations_core import do_local_migrations


@pytest.mark.asyncio
async def test_blog(event_loop):
    await orm.create_pool(event_loop, **configs.db)

    await do_local_migrations()

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

    field = await handlers.api_create_content_field(name='name', title='Name', field_type='String')
    assert field is not None
    field = await handlers.api_create_content_field(name='tag', title='Tag', field_type='String')
    assert field is not None
    field = await handlers.api_create_content_field(name='content', title='Content', field_type='Text')
    assert field is not None
    field = await handlers.api_create_content_field(name='created_at', title='Created At', field_type='CreatedAt')
    assert field is not None

    model = await handlers.api_create_content_model(name='article', title='Article',
                                                           fields=('name', 'tag', 'content', 'created_at'))
    assert model is not None

    data = await handlers.api_create_content(model_name='article', data={
        'name': 'hello world',
        'content': 'this is hello world article content !',
        'created_at': '2017-08-09 12:20:40'
    })
    assert data is not None

    contents = await handlers.api_get_contents(model_name='article')
    assert contents is not None