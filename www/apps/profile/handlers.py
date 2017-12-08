from playhouse.shortcuts import model_to_dict

from app_cores import app_fn
import events
from apps.core.models import Article
from coroweb import get
from dbs import objects


@app_fn(events.__EVENT_ROUTING__, 'profile', 'profile')
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
