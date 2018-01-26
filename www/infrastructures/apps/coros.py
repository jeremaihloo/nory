"""
__auth__
"""
import inspect
import logging
import os
import importlib
from infrastructures import utils, constants
from infrastructures.apps import features
from infrastructures.apps.app_info_loaders import load_app_info
from infrastructures.apps.dependency import sort_app_info_by_dependency
from infrastructures.apps.models import App
from infrastructures.configs.models import NcmsConfig


class AppLoader(object):
    async def load(self, app_info):
        app = App(app_info)

        for id in app_info.indexs:
            m = importlib.import_module('apps.{}.{}'.format(app_info.name, id))
            for attr in dir(m):
                fn = getattr(m, attr, None)
                if fn is not None and inspect.isfunction(fn):
                    event = getattr(fn, constants.FEATURE_TYPE, None)
                    if event is not None:
                        if app.features.get(event, None) is None:
                            app.features[event] = []
                        app.features[event].append(fn)
        return app


def get_apps_paths():
    abs_p = os.path.abspath('.')
    apps = os.listdir(os.path.join(abs_p, 'apps'))

    apps = list(filter(lambda x: not x.startswith('_') and not x.startswith('.') and not x.endswith('.py'), apps))
    return apps


@utils.singleton
class AppManager(object):
    def __init__(self, ncms_application):
        self.ncms_application = ncms_application
        self.apps = {}

    async def reload_apps(self):

        await self.load_apps()

    async def do_app_loading(self):
        loadings = self.get_worked_features(features.__FEATURE_ON_APP_LOADING__)
        for item in loadings:
            await item(self.ncms_application)

    async def load_apps(self):
        logging.info('start loading apps')
        app_names = get_apps_paths()

        app_infos = await self.load_app_infos(app_names)
        apps = await self.load_app_entries(app_infos)

        await self.do_app_loading()
        return apps

    async def load_app_infos(self, app_names):
        app_infos = []
        for item in app_names:
            try:
                info = load_app_info(item)
                if info:
                    app_infos.append(info)
                    logging.debug('[load_app_info] found loader for [{}]'.format(item))
            except Exception as e:
                logging.exception('[load_app_infos] load app info [{}] error', item, e)

        app_infos = sort_app_info_by_dependency(app_infos)

        logging.info('[load_app_infos] sorted app info dependency [{}]'.format([x.name for x in app_infos]))
        return app_infos

    async def load_app_entries(self, app_infos):
        app_loader = AppLoader()
        for item in app_infos:
            if item.name in NcmsConfig.pre_installed_apps and not utils.ncms_has_been_installed():
                item.enabled = True
            try:
                if item.enabled:
                    app = await app_loader.load(item)
                    self.apps[item.name] = app
                    logging.info('[load_apps] app [{}] loaded'.format(item.name))
                else:
                    logging.info('[load_apps] app [{}] skiped [disabled]'.format(item.name))
            except Exception as e:
                logging.exception('[load_apps] app [{}] load error'.format(item.name))

    def get_worked_features(self, event):
        enabled_apps = [x for x in self.apps.values() if x.info.enabled]
        features = []
        for item in enabled_apps:
            app_features = [x for x in item.features[event]]
            enabled_features = [x for x in app_features if getattr(x, 'enabled', True)]
            features.extend(enabled_features)
        logging.debug('[get_worked_features] {}'.format(features))
        return features
