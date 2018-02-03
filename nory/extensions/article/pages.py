import re

from extensions.article.api import api_get_articles, api_get_tags, api_get_articles_by_tag, api_get_article_by_id
from extensions.pagination.coros import get_pagination
from infrastructures.apps import features
from extensions.article.utils import get_markdown_h1
from infrastructures.apps.decorators import feature
from extensions.article.models import Tag, Article, User, ArticleTagMapping
from extensions.auth_base.white import allow_anyone
from infrastructures.web.decorators import get, post
from infrastructures.dbs import objects
from infrastructures.utils import next_id, hash_pwd
from playhouse.shortcuts import model_to_dict
from infrastructures.errors import NcmsWebApiValueError, NcmsWebApiError


@allow_anyone
@feature(features.__FEATURE_ROUTING__, 'page_index', 'page_index')
@get('/')
async def page_index():
    articles = await api_get_articles(published=True, page=1)
    print(articles)
    return {
        'articles': articles,
        '__template__': 'article/templates/index.html'
    }


@allow_anyone
@feature(features.__FEATURE_ROUTING__, 'page_tags', 'page_tags')
@get('/tags')
async def page_tags():
    tags = await api_get_tags()
    return {
        '__template__': 'article/templates/tags.html',
        'tags': tags
    }


@allow_anyone
@feature(features.__FEATURE_ROUTING__, 'page_article_by_tag', 'page_article_by_tag')
@get('/tags/{tag}')
async def page_article_by_tag(*, tag):
    articles = await api_get_articles_by_tag(tag=tag)
    return {
        '__template__': 'article/templates/tag-item.html',
        'articles': articles
    }


@allow_anyone
@feature(features.__FEATURE_ROUTING__, 'page_id', 'page_id')
@get('/articles/{id}')
async def page_article(*, id):
    article = await api_get_article_by_id(id=id, published=True)
    return {
        'article': article,
        '__template__': 'article/templates/article.html'
    }


@allow_anyone
@feature(features.__FEATURE_ROUTING__, 'page_name', 'page_name')
@get('/page/{name}')
async def page_name(*, name):
    pass


@feature(features.__FEATURE_ROUTING__, 'manage_articles', 'manage_articles')
@get('/manage/articles')
async def manage_articles():
    return {
        '__template__': 'article/front-admin/dist/index.html'
    }
