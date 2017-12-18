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
from dependency import sort_dependency


def app_fn(event, name, description):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)

        wrapper.__app_event__ = event
        wrapper.__app_fn_name__ = name
        wrapper.__app_fn_description__ = description

        return wrapper

    return decorator


class AppInfo(object):
    def __init__(self, name, version, description, author, home_page, indexs, dependency):
        self.name = name
        self.version = version
        self.description = description
        self.author = author
        self.home_page = home_page
        self.indexs = indexs
        self.dependency = dependency


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
            dependency=getattr(info_m, 'dependency', [])
        )
        return app_info


class AppYamlInfoLoader(AppInfoLoader):
    """app.yaml"""

    def load(self, name):
        abs_p = utils.ncms_www_path()
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
            dependency=app_info.get('dependency', [])
        )
        return app_info


def load_app_info(name):
    m = {
        'info.py': PyInfoLoader(),
        'app.yaml': AppYamlInfoLoader()
    }
    abs_p = utils.ncms_www_path()
    filter_path = lambda key: os.path.exists(os.path.join(abs_p, 'apps/{}/{}'.format(name, key)))
    keys = list(filter(filter_path, m.keys()))
    if keys is None or len(keys) == 0:
        raise FileNotFoundError('app info file not found {}'.format(name))
    elif len(keys) > 1:
        raise Exception('more than one app info file exists')

    loader = m.get(keys[0], None)
    if loader is not None:
        logging.info('found loader for [{}]'.format(name))
        return loader.load(name)
    logging.warning('loader not found for [{}]'.format(name))
    raise Exception('loader not found for [{}]'.format(name))


def sort_app_info_by_dependency(app_infos):
    maps = []
    for item in app_infos:
        for dep in item.dependency:
            maps.append((item, dep))
    logging.info('dependency mappings:{}'.format(maps))
    sorted_deps = sort_dependency(maps)

    def get_info_by_name(name):
        for item in app_infos:
            if name == item.name:
                return item
        return None

    not_need_to_sorted = list(filter(lambda x: x.name not in sorted_deps, app_infos))
    logging.info('not need to sorted {}'.format(not_need_to_sorted))
    sorted_app_info = [get_info_by_name(x) for x in sorted_deps]
    logging.info('sorted app infos {}'.format(sorted_app_info))
    not_need_to_sorted.extend(sorted_app_info)
    logging.info('merged:{}'.format(not_need_to_sorted))
    return not_need_to_sorted


@utils.singleton
class AppManager(utils.DictClass):
    def __init__(self):
        self.__apps__ = []
        self.__app_fns__ = {}

        self.init_fns()

    def init_fns(self):
        es = list(filter(lambda x: x.startswith('__EVENT'), dir(events)))
        for item in es:
            self.__app_fns__[getattr(events, item)] = []

    async def reload_apps(self):
        self.__apps__ = []
        self.__app_fns__ = {}

        self.init_fns()

        self.load_apps()

        self.loading_apps()

    async def install_apps(self):
        pass

    async def install_app(self, item):
        pass

    async def loading_app(self, item):
        await item()

    async def loading_apps(self):
        for item in self.__app_fns__[events.__EVENT_ON_APP_LOADING__]:
            try:
                await self.loading_app(item)
                logging.info('on loading app item {} ok'.format(item))
            except Exception as e:
                logging.warning('on loading_apps error {}'.format(e))

    async def load_apps(self):
        logging.info('loading plugins')
        abs_p = utils.ncms_www_path()
        apps = os.listdir(os.path.join(abs_p, 'apps'))

        apps = list(filter(lambda x: not x.startswith('_') and not x.endswith('.py'), apps))
        app_infos = []

        for item in apps:
            try:
                info = load_app_info(item)
                if info:
                    app_infos.append(info)
            except Exception as e:
                logging.warning('load app info [{}] error :{}'.format(item, e))
        app_infos = sort_app_info_by_dependency(app_infos)
        logging.info('sorted app info dependency {}'.format([x.name for x in app_infos]))
        for item in app_infos:
            try:
                await self.load_app(item)
                logging.info('app {} loaded'.format(item.name))
            except Exception as e:
                logging.warning('app {} load error'.format(item.name))
                logging.warning(str(e))

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
                            if self.__app_fns__.get(event, None) is None:
                                self.__app_fns__[event] = []
                            self.__app_fns__[event].append(fn)
