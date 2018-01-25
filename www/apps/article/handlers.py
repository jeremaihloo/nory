import re

from apps.pagination.coros import get_pagination
from infrastructures import events
from apps.article.utils import get_markdown_h1
from infrastructures.apps.decorators import feature
from apps.article.models import Tag, Article, User, ArticleTagMapping
from apps.auth_base.white import allow_anyone
from infrastructures.web.decorators import get, post
from infrastructures.dbs import objects
from infrastructures.utils import next_id, hash_pwd
from playhouse.shortcuts import model_to_dict
from infrastructures.errors import NcmsWebApiValueError, NcmsWebApiError


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


@feature(events.__FEATURE_ROUTING__, 'api_get_tags', 'api_get_tags')
@get('/api/tags')
async def api_get_tags(*, page=1):
    tags = await get_pagination(Tag.select(), page_index=page)
    return tags


@feature(events.__FEATURE_ROUTING__, 'api_post_tags', 'api_post_tags')
@post('/api/tags')
async def api_post_tags(*, content):
    o, _ = await objects.create_or_get(Tag, content=content)
    return 200, model_to_dict(o)


@feature(events.__FEATURE_ROUTING__, 'api_get_articles', 'api_get_articles')
@get('/api/articles')
async def api_get_articles(*, published=False, page=1):
    query = Article.select()
    if published:
        query = query.where(Article.published == True)

    articles = await get_pagination(query, page)

    return articles


@feature(events.__FEATURE_ROUTING__, 'api_post_articles', 'api_post_articles')
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


@feature(events.__FEATURE_ROUTING__, 'api_get_article_by_id', 'api_get_article_by_id')
@get('/api/articles/{id}')
async def api_get_article_by_id(*, id, published=False):
    article = await objects.get(Article.select().where(Article.id == id, Article.published == published))
    return model_to_dict(article)


@feature(events.__FEATURE_ROUTING__, 'api_publish_article', 'api_publish_article')
@post('/api/articles/{id}/publish')
async def api_publish_article(*, id):
    article = await objects.get(Article, id=id)
    article.published = True
    await objects.update(article)
    return model_to_dict(article)


@feature(events.__FEATURE_ROUTING__, 'api_un_publish_article', 'api_un_publish_article')
@post('/api/articles/{id}/un-publish')
async def api_un_publish_article(*, id):
    article = await objects.get(Article, id=id)
    article.published = False
    await objects.update(article)
    return model_to_dict(article)


@feature(events.__FEATURE_ROUTING__, 'api_un_publish_article', 'api_un_publish_article')
@post('/api/articles/{id}/enable')
async def api_enable_article(*, id):
    article = await objects.get(Article, id=id)
    article.enabled = True
    await objects.update(article)
    return model_to_dict(article)


@feature(events.__FEATURE_ROUTING__, 'api_un_publish_article', 'api_un_publish_article')
@post('/api/articles/{id}/disable')
async def api_disable_article(*, id):
    article = await objects.get(Article, id=id)
    article.enabled = False
    await objects.update(article)
    return model_to_dict(article)


@feature(events.__FEATURE_ROUTING__, 'api_get_article_by_id', 'api_get_article_by_id')
@post('/api/tags/{tag}/articles')
async def api_get_articles_by_tag(*, tag, page=1):
    query = (Article.select()
        .join(ArticleTagMapping)
        .join(Tag)
        .where(Tag.content == tag))
    articles = await get_pagination(query, page_index=page)
    return 200, articles


@allow_anyone
@feature(events.__FEATURE_ROUTING__, 'page_index', 'page_index')
@get('/')
async def page_index():
    articles = await api_get_articles(published=True, page=1)
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
    article = await api_get_article_by_id(id=id, published=True)
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
