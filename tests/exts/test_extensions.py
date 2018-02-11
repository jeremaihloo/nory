import pytest

from nory.infras.exts import features
from nory.infras.exts.models import ExtensionLoader
from nory.infras.exts.info_loaders import load_extension_info
from nory.infras.exts.dependency import sort_extension_dependency
from nory.infras.exts.managers import ExtensionManager


@pytest.mark.asyncio
async def test_load_info():
    info_a = load_extension_info('demo-a')
    assert info_a.name == 'demo-a'


def test_info_sort():
    info_b = load_extension_info('demo-b')
    info_a = load_extension_info('demo-a')

    r = sort_extension_dependency([info_a, info_b])
    assert isinstance(r, list)
    assert r[0].name == 'demo-b'
    assert r[1].name == 'demo-a'


@pytest.mark.asyncio
async def test_extension_loader():
    info = load_extension_info('demo-a')
    loader = ExtensionLoader(paths=[__package__])
    extension = await loader.load(info)
    assert len(extension.features[features.__FEATURE_ROUTING__]) == 1
    assert len(extension.get_worked_features(features.__FEATURE_ROUTING__)) == 1

@pytest.mark.asyncio
async def test_load_extension_manager():
    manager = ExtensionManager()
    await manager.load_extensions()
    assert len(manager.extensions) == 2
    assert len(manager.get_worked_features(features.__FEATURE_ROUTING__)) == 2
