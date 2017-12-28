import events
from app_cores import app_fn


@app_fn(events.__EVENT_AUTHING__, '', '')
def auth_rbacm_provider(app, request):
    return True, 'auth ok'
