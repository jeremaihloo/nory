from infrastructures import events
from infrastructures.apps.coros import feature


@feature(events.__FEATURE_TASK__, 'upload_to_qiniu', 'upload_to_qiniu')
def upload_to_qiniu():
    return True, 'ok'
