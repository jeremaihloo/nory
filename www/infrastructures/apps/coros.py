"""
__auth__
"""
import inspect
import logging
import os
import importlib
from infrastructures import events, utils
from infrastructures.apps.app_info_loaders import PyInfoLoader, AppYamlInfoLoader
from infrastructures.apps.dependency import sort_app_info_by_dependency
from infrastructures.configs.models import NcmsConfig



class AppLoader(object):
    def load(self, name):
        pass

def load_app_info(name):
    m = {
        'info.py': PyInfoLoader(),
        'app.yaml': AppYamlInfoLoader()
    }
    abs_p = os.path.abspath('.')
    filter_path = lambda key: os.path.exists(os.path.join(abs_p, 'apps/{}/{}'.format(name, key)))
    keys = list(filter(filter_path, m.keys()))
    if keys is None or len(keys) == 0:
        raise FileNotFoundError('app info file not found {}'.format(name))
    elif len(keys) > 1:
        raise Exception('more than one app info file exists')

    loader = m.get(keys[0], None)
    if loader is not None:
        return loader.load(name)
    raise Exception('[load_app_info] loader not found for [{}]'.format(name))


@utils.singleton
class AppManager(utils.DictClass):
    def __init__(self, app):
        self.app = app
        self.__apps__ = []
        self.__features__ = {}

        self.init_fns()

    def init_fns(self):
        es = list(filter(lambda x: x.startswith('__EVENT'), dir(events)))
        for item in es:
            self.__features__[getattr(events, item)] = []

    async def reload_apps(self):
        self.__apps__ = []
        self.__features__ = {}

        self.init_fns()

        self.load_apps()

        self.loading_apps()

    async def install_apps(self):
        pass

    async def install_app(self, item):
        pass

    async def loading_app(self, item):
        await item(self.app)

    async def loading_apps(self):
        for item in self.__features__.get(events.__FEATURE_ON_APP_LOADING__, []):
            try:
                await self.loading_app(item)
                logging.info('[loading_apps] app item {} ok'.format(item))
            except Exception as e:
                logging.exception('[loading_apps] error [{}]  {}'.format(item, e))

    async def load_apps(self):
        logging.info('start loading apps')
        abs_p = os.path.abspath('.')
        apps = os.listdir(os.path.join(abs_p, 'apps'))

        apps = list(filter(lambda x: not x.startswith('_') and not x.startswith('.') and not x.endswith('.py'), apps))
        app_infos = []

        for item in apps:
            try:
                info = load_app_info(item)
                if info:
                    app_infos.append(info)
                    logging.info('[load_app_info] found loader for [{}]'.format(item))
            except Exception as e:
                logging.exception('load app info [{}] error', item, e)

        app_infos = sort_app_info_by_dependency(app_infos)

        logging.info('sorted app info dependency [{}]'.format([x.name for x in app_infos]))

        for item in app_infos:
            if item.name in NcmsConfig.pre_installed_apps and not utils.ncms_has_been_installed():
                item.enabled = True
            try:
                if item.enabled:
                    await self.load_app(item)
                    logging.info('[load_apps] app [{}] loaded'.format(item.name))
                else:
                    logging.info('[load_apps] app [{}] skiped [disabled]'.format(item.name))
            except Exception as e:
                logging.exception('[load_apps] app [{}] load error'.format(item.name))

        await self.loading_apps()

    async def load_app(self, app_info):
        self.__apps__.append(app_info)
        indexs = app_info.indexs
        if indexs:
            for id in indexs:
                m = importlib.import_module('apps.{}.{}'.format(app_info.name, id))
                for attr in dir(m):
                    fn = getattr(m, attr, None)
                    if fn is not None and inspect.isfunction(fn):
                        event = getattr(fn, '__app_event__', None)
                        if event is not None:
                            if self.__features__.get(event, None) is None:
                                self.__features__[event] = []
                            self.__features__[event].append(fn)

