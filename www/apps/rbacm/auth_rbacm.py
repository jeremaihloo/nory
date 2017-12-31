import events
from app_cores import feature


@feature(events.__FEATURE_AUTHING__, '', '')
async def auth_rbacm_provider(app, request):
    return True, 'auth ok'
