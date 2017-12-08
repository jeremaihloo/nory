import re
import events
from app_cores import app_fn
from apps.core.apis import APIValueError, APIError, Page
from apps.core.models import Tag, Article, User
from coroweb import get, post
from dbs import objects
from utils import next_id, hash_pwd


@app_fn(events.__EVENT_ROUTING__, 'api_post_login', 'api_post_login')
@post('/api/login')
async def api_post_login(*, name, password):
    user = User.select().where(User.name == name, User.password == password)
    if user.exists():
        user = user.get()
        return user
    else:
        return 404


@app_fn(events.__EVENT_ROUTING__, 'api_get_users', 'api_get_users')
@get('/api/users')
async def api_get_users(*, page='1'):
    page_index = get_page_index(page)
    num = await User.findNumber('count(id)')
    p = Page(num, page_index)
    if num == 0:
        return dict(page=p, users=())
    users = await User.findAll(orderBy='created_at desc', limit=(p.offset, p.limit))
    for u in users:
        u.passwd = '******'
    return dict(page=p, users=users)


_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')


@app_fn(events.__EVENT_ROUTING__, 'api_register_user', 'api_register_user')
@post('/api/users')
async def api_register_user(*, email, name, passwd):
    if not name or not name.strip():
        raise APIValueError('name')
    if not email or not _RE_EMAIL.match(email):
        raise APIValueError('email')
    if not passwd:
        raise APIValueError('passwd')
    users = await objects.get(User.select().where(User.email))
    if len(users) > 0:
        raise APIError('register:failed', 'email', 'Email is already in use.')
    uid = next_id()

    await objects.create(User, id=uid, name=name.strip(), email=email, passwd=hash_pwd(passwd))

    return 200


@app_fn(events.__EVENT_ROUTING__, 'api_login', 'api_login')
@post('/api/login')
async def api_login(*, name, passwd):
    user = await objects.get(User.select().where(User.name == name, User.password == passwd))
    return 200 if user else 404


@app_fn(events.__EVENT_ROUTING__, 'api_get_tags', 'api_get_tags')
@get('/api/tags')
async def api_get_tags():
    tags = await objects.execute(Tag.select())
    return tags


@app_fn(events.__EVENT_ROUTING__, 'api_post_tags', 'api_post_tags')
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
