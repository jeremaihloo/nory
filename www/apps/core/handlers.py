from app_cores import app_fn, __EVENT_ROUTING__
from coroweb import get
from www.handlers import *


@app_fn(__EVENT_ROUTING__, 'page_index', 'page_index')
@get('/')
async def page_index():
    return {
        '__template__': 'core/templates/index.html'
    }


@app_fn(__EVENT_ROUTING__, 'tags', 'tags')
@get('/tags')
async def page_tags():
    tags = await api_get_contents(model_name='tag')
    print(tags)
    return {
        '__template__': 'core/templates/tags.html',
        'tags': tags
    }


@app_fn(__EVENT_ROUTING__, 'page_tags', 'page_tags')
@get('/tags/{name}')
async def page_tag_item(*, name):
    articles = await api_get_contents(model_name='article')
    print(articles)
    return {
        '__template__': 'core/templates/tag-item.html',
        'articles': articles
    }


@app_fn(__EVENT_ROUTING__, 'page_content', 'page_content')
@get('/content/{content_slug}')
async def page_content():
    pass


@app_fn(__EVENT_ROUTING__, 'page_id', 'page_id')
@get('/content/id-{id}')
async def page_id(*, id):
    pass


@app_fn(__EVENT_ROUTING__, 'page_name', 'page_name')
@get('/page/{name}')
async def page_name(*, name):
    pass
