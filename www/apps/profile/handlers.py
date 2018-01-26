from playhouse.shortcuts import model_to_dict

from infrastructures.apps.coros import feature
from infrastructures.apps import features
from apps.article.models import Article
from infrastructures.web.coros import get
from infrastructures.dbs import objects


@feature(features.__FEATURE_ROUTING__, 'profile', 'profile')
@get('/profile')
async def page_profile():
    try:
        profile = await objects.get(Article.select().where(Article.title == 'profile'))
        profile = model_to_dict(profile)
    except:
        profile = None
    return {
        'profile': profile,
        '__template__': 'profile/templates/profile.html'
    }
