
from plugins import PluginManager


def test_load_plugins():
    manager = PluginManager()
    manager.load_plugins()
    print(manager)