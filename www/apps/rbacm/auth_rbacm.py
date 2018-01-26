from infrastructures.apps import features
from infrastructures.apps.decorators import feature


@feature(features.__FEATURE_AUTHING__, 'auth_rbacm_provider', 'auth_rbacm_provider')
async def auth_rbacm_provider(app, request):
    return False, 'auth ok'
