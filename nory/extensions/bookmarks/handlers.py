from playhouse.shortcuts import model_to_dict

from extensions.article.models import Tag
from extensions.bookmarks.models import Bookmark, BookmarkUserStar, BookmarkVote, BookmarkTagMappings
from extensions.pagination.coros import get_pagination
from infrastructures.apps import features
from infrastructures.apps.decorators import feature
from infrastructures.dbs import objects
from infrastructures.web.decorators import post, get


@feature(features.__FEATURE_ROUTING__, 'api_create_bookmarks', 'api_create_bookmarks')
@post('/api/bookmarks')
async def api_create_bookmarks(*, title, url, tags):
    bookmark, _ = objects.get_or_create(Bookmark,
                                        title=title,
                                        url=url)
    for tag in tags:
        tag, _ = objects.get_or_create(Tag, content=tag)
        m, _ = await objects.create_or_get(BookmarkTagMappings,
                                           tag=tag,
                                           bookmark=bookmark)
    return 200, model_to_dict(bookmark)


@feature(features.__FEATURE_ROUTING__, 'api_get_bookmarks', 'api_get_bookmarks')
@get('/api/bookmarks')
async def api_get_bookmarks(*, page=1):
    query = Bookmark.select()
    bookmarks = await get_pagination(query, page_index=page)
    return 200, bookmarks


@feature(features.__FEATURE_ROUTING__, 'api_get_bookmarks', 'api_get_bookmarks')
@get('/api/bookmarks/tag/{tag}')
async def api_get_bookmarks_by_tag(*, tag, page=1):
    query = (Bookmark.select(Bookmark)
        .join(BookmarkTagMappings)
        .join(Tag)
        .where(Tag.content == tag))
    bookmarks = await get_pagination(query, page_index=page)
    return 200, bookmarks


@feature(features.__FEATURE_ROUTING__, 'api_get_bookmarks', 'api_get_bookmarks')
@get('/api/bookmarks/{bookmark_id}')
async def api_get_bookmarks_by_id(*, bookmark_id):
    bookmark = await objects.get(Bookmark.select().select(id=bookmark_id))
    return 200, bookmark


@feature(features.__FEATURE_ROUTING__, 'api_star_bookmarks', 'api_star_bookmarks')
@post('/api/bookmarks/star/{bookmark_id}')
async def api_star_bookmarks(request, *, bookmark_id):
    bookmark, _ = await objects.create_or_get(BookmarkUserStar,
                                              bookmark=bookmark_id,
                                              user=request.__user__)
    return 200, bookmark


@feature(features.__FEATURE_ROUTING__, 'api_get_bookmarks', 'api_get_bookmarks')
@post('/api/bookmarks/vote/{bookmark_id}')
async def api_vote_bookmarks(request, *, bookmark_id, vote, reason):
    bookmark, _ = await objects.create_or_get(BookmarkVote,
                                              bookmark=bookmark_id,
                                              user=request.__user__,
                                              vote=vote,
                                              reason=reason)
    return 200, bookmark
