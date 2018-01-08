from infrastructures import events
from infrastructures.apps.decorators import feature


@feature(events.__FEATURE_AUTHING__, 'auth_rbacm_provider', 'auth_rbacm_provider')
async def auth_rbacm_provider(app, request):
    return False, 'auth ok'
