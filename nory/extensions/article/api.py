import re

from playhouse.shortcuts import model_to_dict

from extensions.article.models import User, Article, ArticleTagMapping, Tag
from extensions.article.utils import get_markdown_h1
from extensions.pagination.coros import get_pagination
from infrastructures.apps import features
from infrastructures.apps.decorators import feature
from infrastructures.dbs import objects
from infrastructures.errors import NcmsWebApiValueError, NcmsWebApiError
from infrastructures.utils import hash_pwd, next_id
from infrastructures.web.decorators import post, get


@feature(features.__FEATURE_ROUTING__, 'api_get_users', 'api_get_users')
@get('/api/users')
async def api_get_users(*, page=1):
    users = await objects.execute(User.select().paginate(page))
    return [model_to_dict(x, exclude=[User.password, User.articles], backrefs=True) for x in users]


_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')


@feature(features.__FEATURE_ROUTING__, 'api_register_user', 'api_register_user')
@post('/api/users')
async def api_register_user(*, email, name, passwd):
    if not name or not name.strip():
        raise NcmsWebApiValueError('name')
    if not email or not _RE_EMAIL.match(email):
        raise NcmsWebApiValueError('email')
    if not passwd:
        raise NcmsWebApiValueError('passwd')
    users = await objects.get(User.select().where(User.email))
    if len(users) > 0:
        raise NcmsWebApiError('register:failed', 'email', 'Email is already in use.')
    uid = next_id()

    await objects.create(User, id=uid, name=name.strip(), email=email, passwd=hash_pwd(passwd))

    return 200


@feature(features.__FEATURE_ROUTING__, 'api_get_tags', 'api_get_tags')
@get('/api/tags')
async def api_get_tags(*, page=1):
    tags = await get_pagination(Tag.select(), page_index=page)
    return tags


@feature(features.__FEATURE_ROUTING__, 'api_post_tags', 'api_post_tags')
@post('/api/tags')
async def api_post_tags(*, content):
    o, _ = await objects.create_or_get(Tag, content=content)
    return 200, model_to_dict(o)


@feature(features.__FEATURE_ROUTING__, 'api_get_articles', 'api_get_articles')
@get('/api/articles')
async def api_get_articles(*, published=False, page=1):
    query = Article.select()
    if published:
        query = query.where(Article.published == True)

    articles = await get_pagination(query, page)

    return articles


@feature(features.__FEATURE_ROUTING__, 'api_post_articles', 'api_post_articles')
@post('/api/articles')
async def api_post_articles(request, *, content, id=None):
    if id is None:
        o, _ = await objects.get_or_create(Article, content=content, title=get_markdown_h1(content),
                                           user=request.__user__)
    else:
        o = await objects.get(Article, id=id)
        o.content = content
        o.title = get_markdown_h1(content)
        await objects.update(o)
    return 200, model_to_dict(o)


@feature(features.__FEATURE_ROUTING__, 'api_get_article_by_id', 'api_get_article_by_id')
@get('/api/articles/{id}')
async def api_get_article_by_id(*, id, published=False):
    article = await objects.get(Article.select().where(Article.id == id, Article.published == published))
    return model_to_dict(article)


@feature(features.__FEATURE_ROUTING__, 'api_publish_article', 'api_publish_article')
@post('/api/articles/{id}/publish')
async def api_publish_article(*, id):
    article = await objects.get(Article, id=id)
    article.published = True
    await objects.update(article)
    return model_to_dict(article)


@feature(features.__FEATURE_ROUTING__, 'api_un_publish_article', 'api_un_publish_article')
@post('/api/articles/{id}/un-publish')
async def api_un_publish_article(*, id):
    article = await objects.get(Article, id=id)
    article.published = False
    await objects.update(article)
    return model_to_dict(article)


@feature(features.__FEATURE_ROUTING__, 'api_un_publish_article', 'api_un_publish_article')
@post('/api/articles/{id}/enable')
async def api_enable_article(*, id):
    article = await objects.get(Article, id=id)
    article.enabled = True
    await objects.update(article)
    return model_to_dict(article)


@feature(features.__FEATURE_ROUTING__, 'api_un_publish_article', 'api_un_publish_article')
@post('/api/articles/{id}/disable')
async def api_disable_article(*, id):
    article = await objects.get(Article, id=id)
    article.enabled = False
    await objects.update(article)
    return model_to_dict(article)


@feature(features.__FEATURE_ROUTING__, 'api_get_article_by_id', 'api_get_article_by_id')
@post('/api/tags/{tag}/articles')
async def api_get_articles_by_tag(*, tag, page=1):
    query = (Article.select()
        .join(ArticleTagMapping)
        .join(Tag)
        .where(Tag.content == tag))
    articles = await get_pagination(query, page_index=page)
    return 200, articles
