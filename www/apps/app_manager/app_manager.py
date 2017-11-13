import app_cores
from app_cores import app_fn, AppManager
from coroweb import get


@app_fn(app_cores.__EVENT_ROUTING__, 'get_plugins', 'get plugin infos')
@get('/api/plugins')
async def api_get_plugins():
    manager = AppManager()
    infos = list(manager.get_plugin_infos())
    return {
        'infos': infos
    }


@app_fn(app_cores.__EVENT_ROUTING__, 'get_plugin_features', 'get plugin feautures')
@get('/api/plugins/features')
async def api_get_features():
    manager = AppManager()
    return {
        'features': manager.get_features()
    }


@app_fn(app_cores.__EVENT_ROUTING__, 'reload_plugins', 'reload plugins')
@get('/api/plugins/reload')
async def api_get_features():
    manager = AppManager()
    manager.reload_apps()
    return {
        'ok': True
    }
