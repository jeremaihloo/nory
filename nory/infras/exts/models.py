import importlib
import inspect

from infras import constants
from infras.exts import features


class ExtensionInfo(object):
    def __init__(self, name, version, description, author, home_page, indexs, dependency, static, enabled, locale):
        self.name = name
        self.version = version
        self.description = description
        self.author = author
        self.home_page = home_page
        self.indexs = indexs
        self.dependency = dependency
        self.static = static
        self.enabled = enabled
        self.locale = locale


class Extension(object):
    def __init__(self, info, ncms_application):
        self.info = info
        self.ncms_application = ncms_application
        self.init_features()

    def init_features(self):
        self.features = {}
        for item in dir(features):
            if item.startswith('__FEATURE'):
                self.features[item] = []

    async def load(self):
        m = importlib.import_module('extensions.{}.__init__'.format(self.info.name))
        await self._load(m)

    async def _load(self, m):
        for attr in dir(m):
            fn = getattr(m, attr, None)
            if fn is not None and inspect.isfunction(fn):
                event = getattr(fn, constants.FEATURE_TYPE, None)
                if event is not None:
                    if self.features.get(event, None) is None:
                        self.features[event] = []
                    self.features[event].append(fn)

    async def reload(self):
        self.init_features()
        m = importlib.reload('extensions.{}.__init__'.format(self.info.name))
        self._load(m)

    async def on_installing(self):
        fs = self.get_worked_features(features.__FEATURE_ON_APP_INSTALLING__)
        await self.do_features(fs)

    async def on_loading(self):
        fs = self.get_worked_features(features.__FEATURE_ON_APP_LOADING__)
        await self.do_features(fs)

    async def do_features(self, fs):
        for item in fs:
            await item(self.ncms_application)

    async def on_uninstall(self):
        fs = self.get_worked_features(features.__FEATURE_ON_APP_UNINSTALLING__)
        await self.do_features()

    async def on_enable_feature(self, fs):
        for f in fs:
            setattr(f, 'enabled', True)

    async def on_disable_feature(self, fs):
        for f in fs:
            setattr(f, 'enabled', False)

    def get_worked_features(self, event):
        app_features = [x for x in self.features[event]]
        enabled_features = [x for x in app_features if getattr(x, 'enabled', True)]
        return enabled_features
