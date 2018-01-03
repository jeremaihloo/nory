import events
from app_cores import feature


@feature(events.__FEATURE_TASK__, 'upload_to_qiniu', 'upload_to_qiniu')
def upload_to_qiniu():
    return True, 'ok'
