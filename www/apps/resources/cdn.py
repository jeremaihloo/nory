from infrastructures.apps import features
from infrastructures.apps.decorators import feature


@feature(features.__FEATURE_TASK__, 'upload_to_qiniu', 'upload_to_qiniu')
async def upload_to_qiniu():
    return True, 'ok'


async def sync_resources():
    pass