
from plugins import PluginManager


def test_load_plugins():
    manager = PluginManager()
    manager.load_plugins()
    print(manager)
    print(list(manager.get_plugin_infos()))