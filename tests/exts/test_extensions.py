import os
import pytest

from nory.infras.exts import features
from nory.infras.exts.models import ExtensionLoader
from nory.infras.exts.info_loaders import ExtensionInfoLoader
from nory.infras.exts.dependency import sort_extension_dependency
from nory.infras.exts.managers import ExtensionManager
from nory.infras.envs.configs import Environment

loader = ExtensionLoader(None, paths=[os.path.abspath('../extensions')])
info_loader = ExtensionInfoLoader(None, loader)


def test_load_info():
    info_a = info_loader.load('demo-a')
    assert info_a.name == 'demo-a'


def test_info_sort():
    info_b = info_loader.load('demo-b')
    info_a = info_loader.load('demo-a')

    r = sort_extension_dependency([info_a, info_b])
    assert isinstance(r, list)
    assert r[0].name == 'demo-b'
    assert r[1].name == 'demo-a'


def test_extension_loader():
    info = info_loader.load('demo_b')
    loader = ExtensionLoader(None, paths=['../extensions'])
    extension = loader.load(info)
    assert len(extension.features[features.__FEATURE_ROUTING__]) == 1
    assert len(extension.get_worked_features(features.__FEATURE_ROUTING__)) == 1
    print('....')


@pytest.mark.asyncio
async def test_load_extension_manager():
    env = Environment('test', os.path.dirname(__file__))
    loader = ExtensionLoader(env, paths=['../extensions'])
    manager = ExtensionManager(env, loader)
    await manager.load_extensions()
    assert len(manager.extensions.keys()) == 2
    for key, val in manager.extensions.items():
        assert key in ('demo-a', 'demo-b')
        assert len(val.get_worked_features(features.__FEATURE_ROUTING__)) == 1
    assert len(manager.get_worked_features(features.__FEATURE_ROUTING__)) == 2
