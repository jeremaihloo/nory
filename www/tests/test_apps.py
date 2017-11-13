
from app_cores import AppManager


def test_load_plugins():
    manager = AppManager()
    manager.load_apps()
    assert manager.__apps__ is not None and len(manager.__apps__) > 0
    assert manager.__app_fns__ is not None
    print(list(manager.__apps__))
    print(manager.__app_fns__)