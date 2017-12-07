import events
from app_cores import app_fn
from apps.core.models import Tag, Article
from coroweb import get, post
from dbs import objects


@app_fn(events.__EVENT_ROUTING__, 'tags', ')')
@get('/api/tags')
async def api_get_tags():
    tags = await objects.execute(Tag.select())
    return tags


@app_fn(events.__EVENT_ROUTING__, 'tags', ')')
@post('/api/tags')
async def api_post_tags(*, content):
    return 200


@app_fn(events.__EVENT_ROUTING__, 'blog', ')')
@get('/api/articles')
async def api_get_blogs():
    async with await database.atomic() as db:
        tags = await db.select(Query().select(Tag).all())
    return tags


@app_fn(events.__EVENT_ROUTING__, 'blog', ')')
@post('/api/articles')
async def api_get_articles(*, content):
    return 200


@app_fn(events.__EVENT_ROUTING__, 'page_index', 'page_index')
@get('/')
async def page_index():
    return {
        '__template__': 'core/templates/layout.html'
    }


@app_fn(events.__EVENT_ROUTING__, 'tags', 'tags')
@get('/tags')
async def page_tags():
    tags = await api_get_tags()
    return {
        '__template__': 'core/templates/tags.html',
        'tags': tags
    }


@app_fn(events.__EVENT_ROUTING__, 'page_tags', 'page_tags')
@get('/tags/{name}')
async def page_tag_item(*, name):
    articles = await api_get_contents(model_name='article')
    print(articles)
    return {
        '__template__': 'core/templates/tag-item.html',
        'articles': articles
    }


@app_fn(events.__EVENT_ROUTING__, 'page_content', 'page_content')
@get('/content/{content_slug}')
async def page_content():
    pass


@app_fn(events.__EVENT_ROUTING__, 'page_id', 'page_id')
@get('/content/id-{id}')
async def page_id(*, id):
    pass


@app_fn(events.__EVENT_ROUTING__, 'page_name', 'page_name')
@get('/page/{name}')
async def page_name(*, name):
    pass
