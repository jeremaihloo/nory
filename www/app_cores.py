"""
__auth__
"""
import inspect
import logging
import os
import importlib
import functools
import yaml
import utils
import events
from configs import NcmsConfig
from dependency import sort_app_dependency


def feature(event, name='', title='', description=''):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)

        wrapper.__app_event__ = event
        wrapper.__app_fn_name__ = name
        wrapper.__app_fn_title__ = title
        wrapper.__app_fn_description__ = description

        return wrapper

    return decorator


class AppInfo(object):
    def __init__(self, name, version, description, author, home_page, indexs, dependency, static, enabled):
        self.name = name
        self.version = version
        self.description = description
        self.author = author
        self.home_page = home_page
        self.indexs = indexs
        self.dependency = dependency
        self.static = static
        self.enabled = enabled


class AppLoader(object):
    def load(self, name):
        pass


class AppInfoLoader(object):
    def load(self, name):
        pass


class PyInfoLoader(AppInfoLoader):
    """info.py"""

    def load(self, name):
        info_m = importlib.import_module('apps.{}.info'.format(name))
        app_info = AppInfo(
            name=name,
            author=getattr(info_m, '__author__', 'None'),
            version=getattr(info_m, '__version__', 'None'),
            description=getattr(info_m, '__description__', 'None'),
            home_page=getattr(info_m, '__home_page__', 'None'),
            indexs=getattr(info_m, 'INDEXS', []),
            dependency=getattr(info_m, 'dependency', []),
            static=getattr(info_m, 'static', {}),
            enabled=getattr(info_m, 'enabled', False)
        )
        return app_info


class AppYamlInfoLoader(AppInfoLoader):
    """app.yaml"""

    def load(self, name):
        abs_p = os.path.abspath('.')
        path = os.path.join(abs_p, 'apps/{}/{}'.format(name, 'app.yaml'))
        app_info = yaml.load(open(path))
        logging.debug('app_info from yaml:{}'.format(app_info))
        app_info = AppInfo(
            name=name,
            author=app_info.get('author', ''),
            version=app_info.get('version', ''),
            description=app_info.get('description', ''),
            home_page=app_info.get('home_page'),
            indexs=app_info.get('indexs', []),
            dependency=app_info.get('dependency', []),
            static=app_info.get('static', {}),
            enabled=app_info.get('enabled', False)
        )
        return app_info


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


def sort_app_info_by_dependency(app_infos):
    maps = []
    for item in app_infos:
        for dep in item.dependency:
            maps.append((item, dep))
    logging.info('dependency mappings:{}'.format(maps))
    sorted_deps = sort_app_dependency(maps)

    def get_info_by_name(name):
        for item in app_infos:
            if name == item.name:
                return item
        return None

    not_need_to_sorted = list(filter(lambda x: x.name not in sorted_deps, app_infos))
    sorted_app_info = [get_info_by_name(x) for x in sorted_deps]
    not_need_to_sorted.extend(sorted_app_info)
    return [x for x in not_need_to_sorted if x is not None]


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
