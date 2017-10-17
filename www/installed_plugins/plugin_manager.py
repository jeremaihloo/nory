__author__ = 'jeremaihloo'

__version__ = '0.0.1'

__description__ = 'plugin manager'

__home_page__ = 'https://github.com/jeremaihloo/ncms-plugin-manager'

from plugins import plugin_fn, PluginManager
from coroweb import get


@plugin_fn('__routes__', 'get_plugins', 'get plugin infos')
@get('/api/plugins')
async def api_get_plugins():
    manager = PluginManager()
    infos = list(manager.get_plugin_infos())
    return {
        'infos': infos
    }


@plugin_fn('__routes__', 'get_plugin_features', 'get plugin feautures')
@get('/api/plugins/features')
async def api_get_features():
    manager = PluginManager()
    return {
        'features': manager.get_features()
    }


@plugin_fn('__routes__', 'reload_plugins', 'reload plugins')
@get('/api/plugins/reload')
async def api_get_features():
    manager = PluginManager()
    manager.reload_plugins()
    return {
        'ok': True
    }