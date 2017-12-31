import app_cores
from app_cores import feature, AppManager
from coroweb import get


@feature(app_cores.__EVENT_ROUTING__, 'get_plugins', 'get plugin infos')
@get('/api/plugins')
async def api_get_plugins():
    manager = AppManager()
    infos = list(manager.get_plugin_infos())
    return {
        'infos': infos
    }


@feature(app_cores.__EVENT_ROUTING__, 'get_plugin_features', 'get plugin feautures')
@get('/api/plugins/features')
async def api_get_features():
    manager = AppManager()
    return {
        'features': manager.get_features()
    }


@feature(app_cores.__EVENT_ROUTING__, 'reload_plugins', 'reload plugins')
@get('/api/plugins/reload')
async def api_get_features():
    manager = AppManager()
    manager.reload_apps()
    return {
        'ok': True
    }
