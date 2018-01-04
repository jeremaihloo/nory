import re
import events
from apps.article.utils import get_markdown_h1
from app_cores import feature
from apps.article.models import Tag, Article, User, ArticleTagMapping
from apps.auth_base.white import allow_anyone
from coroweb import get, post
from dbs import objects
from utils import next_id, hash_pwd
from playhouse.shortcuts import model_to_dict


@feature(events.__FEATURE_ROUTING__, 'api_get_users', 'api_get_users')
@get('/api/users')
async def api_get_users(*, page=1):
    users = await objects.execute(User.select().paginate(page))
    return [model_to_dict(x, exclude=[User.password, User.articles], backrefs=True) for x in users]


_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')


@feature(events.__FEATURE_ROUTING__, 'api_register_user', 'api_register_user')
@post('/api/users')
async def api_register_user(*, email, name, passwd):
    if not name or not name.strip():
        raise NcmsWebApiError('name')
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


@feature(events.__FEATURE_ROUTING__, 'api_get_tags', 'api_get_tags')
@get('/api/tags')
async def api_get_tags():
    tags = await objects.execute(Tag.select())
    return tags


@feature(events.__FEATURE_ROUTING__, 'api_post_tags', 'api_post_tags')
@post('/api/tags')
async def api_post_tags(*, content):
    return 200


@feature(events.__FEATURE_ROUTING__, 'api_get_articles', 'api_get_articles')
@get('/api/articles')
async def api_get_articles(*, page=1):
    articles = await objects.execute(Article.select().paginate(page))
    return [model_to_dict(x, recurse=False) for x in articles]


@feature(events.__FEATURE_ROUTING__, 'api_post_articles', 'api_post_articles')
@post('/api/articles')
async def api_post_articles(request, *, content, id=None):
    if id is None:
        o, _ = await objects.get_or_create(Article, content=content, title=get_markdown_h1(content), user=request.__user__)
    else:
        o = await objects.get(Article, id=id)
        o.content = content
        await objects.update(o)
    return 200, model_to_dict(o)


@feature(events.__FEATURE_ROUTING__, 'api_get_article_by_id', 'api_get_article_by_id')
@post('/api/articles/{id}')
async def api_get_article_by_id(*, id):
    article = await objects.get(Article.select().where(Article.id == id))
    return model_to_dict(article)


@feature(events.__FEATURE_ROUTING__, 'api_get_article_by_id', 'api_get_article_by_id')
@post('/api/tags/{tag}/articles')
async def api_get_articles_by_tag(*, tag):
    articles = await objects.execute((Article.select()
        .join(ArticleTagMapping)
        .join(Tag)
        .where(Tag.content == tag)))
    return [model_to_dict(x) for x in articles]


@allow_anyone
@feature(events.__FEATURE_ROUTING__, 'page_index', 'page_index')
@get('/')
async def page_index():
    articles = await api_get_articles(page=1)
    return {
        'articles': articles,
        '__template__': 'article/templates/index.html'
    }


@allow_anyone
@feature(events.__FEATURE_ROUTING__, 'page_tags', 'page_tags')
@get('/tags')
async def page_tags():
    tags = await api_get_tags()
    return {
        '__template__': 'article/templates/tags.html',
        'tags': tags
    }


@allow_anyone
@feature(events.__FEATURE_ROUTING__, 'page_article_by_tag', 'page_article_by_tag')
@get('/tags/{tag}')
async def page_article_by_tag(*, tag):
    articles = await api_get_articles_by_tag(tag=tag)
    return {
        '__template__': 'article/templates/tag-item.html',
        'articles': articles
    }


@allow_anyone
@feature(events.__FEATURE_ROUTING__, 'page_id', 'page_id')
@get('/articles/{id}')
async def page_article(*, id):
    article = await api_get_article_by_id(id=id)
    return {
        'article': article,
        '__template__': 'article/templates/article.html'
    }


@allow_anyone
@feature(events.__FEATURE_ROUTING__, 'page_name', 'page_name')
@get('/page/{name}')
async def page_name(*, name):
    pass


@feature(events.__FEATURE_ROUTING__, 'manage_articles', 'manage_articles')
@get('/manage/articles')
async def manage_articles():
    return {
        '__template__': 'article/front-admin/dist/index.html'
    }
