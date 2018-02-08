import pytest

from infras.extensions.coros import AppManager

@pytest.mark.asyncio
async def test_load_plugins():
    manager = AppManager()
    await manager.load_apps()
    assert manager.__apps__ is not None and len(manager.__apps__) > 0
    assert manager.__features__ is not None
    print(list(manager.__apps__))
    print(manager.__features__)