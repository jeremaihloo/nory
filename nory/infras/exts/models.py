import importlib
import inspect
import logging

from nory.infras import constants
from nory.infras.exts import features
from nory.infras.exts.contexts import FeatureContext


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
    def __init__(self, env, info, app=None):
        self.env = env
        self.info = info
        self.app = app
        self.init_features()

    def init_features(self):
        self.features = {}
        for item in dir(features):
            if item.startswith('__FEATURE'):
                self.features[item] = []

    async def on_installing(self):
        fs = self.get_worked_features(features.__FEATURE_ON_APP_INSTALLING__)
        await self.do_features(fs)

    async def on_loading(self):
        fs = self.get_worked_features(features.__FEATURE_ON_APP_LOADING__)
        await self.do_features(fs)

    async def do_features(self, fs):
        for item in fs:
            await item(FeatureContext(self.env, self.app))

    async def on_uninstall(self):
        fs = self.get_worked_features(features.__FEATURE_ON_APP_UNINSTALLING__)
        await self.do_features(fs)

    async def on_enable_feature(self, fs):
        for f in fs:
            setattr(f, 'enabled', True)

    async def on_disable_feature(self, fs):
        for f in fs:
            setattr(f, 'enabled', False)

    def get_worked_features(self, event):
        app_features = [x for x in self.features[event]]
        enabled_features = [x for x in app_features if getattr(x, 'enabled', True)]
        for item in enabled_features:
            setattr(item, '__extension__', self)
        return enabled_features


class ExtensionLoadError(Exception):
    pass


class ExtensionLoader(object):
    def __init__(self, env, paths, logger=None):
        self.env = env
        self.paths = paths
        self.logger = logger or logging.getLogger('extension')

    async def load(self, info: ExtensionInfo, app=None) -> Extension:
        for item in self.paths:
            m = importlib.import_module('.extensions.{}'.format(info.name), item)
            if m is not None:
                self.logger.debug('import module {}'.format(m))
                return await self._load(m, info, app)
        # TODO: raize exception
        raise ExtensionLoadError()

    async def _load(self, m, info: ExtensionInfo, app=None):
        extension = Extension(self.env, info, app)
        for attr in dir(m):
            fn = getattr(m, attr, None)
            if fn is not None and inspect.isfunction(fn):
                event = getattr(fn, constants.FEATURE_TYPE, None)
                if event is not None:
                    if extension.features.get(event, None) is None:
                        extension.features[event] = []
                    self.logger.info('feature [{}] [{}] loaded'.format(event, fn))
                    extension.features[event].append(fn)
        return extension

    async def reload(self, info: ExtensionInfo, app=None) -> Extension:
        for item in self.paths:
            m = importlib.reload('.extensions.{}'.format(info.name), item)
            self._load(m, info, app)
