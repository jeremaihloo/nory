"""
__auth__
"""
import inspect
import logging
import os
import importlib
import functools

import utils
import events


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
    def __init__(self, name, version, description, author, home_page):
        self.name = name
        self.version = version
        self.description = description
        self.author = author
        self.home_page = home_page


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
        abs_p = utils.get_ncms_path()
        apps = os.listdir(os.path.join(abs_p, 'apps'))

        apps = list(filter(lambda x: not x.startswith('_') and not x.endswith('.py'), apps))
        for item in apps:
            try:
                await self.load_app(item)
                logging.info('app {} loaded'.format(item))
            except Exception as e:
                logging.warning('app {} load error'.format(item))
                logging.warning(str(e))

        await self.loading_apps()

    async def load_app(self, item):
        abs_p = utils.get_ncms_path()
        app = importlib.import_module('apps.{}'.format(item))
        if not os.path.exists(os.path.join(abs_p, 'apps/{}/info.py'.format(item))):
            raise Exception('load app error , {}/info.py not found'.format(item))

        info = importlib.import_module('apps.{}.info'.format(item))
        info_desc = AppInfo(
            name=item,
            author=getattr(info, '__author__', 'None'),
            version=getattr(info, '__version__', 'None'),
            description=getattr(info, '__description__', 'None'),
            home_page=getattr(info, '__home_page__', 'None')
        )
        self.__apps__.append(info_desc)
        indexs = getattr(info, 'INDEXS', None)
        if indexs:
            for id in indexs:
                m = importlib.import_module('apps.{}.{}'.format(item, id))
                for attr in dir(m):
                    fn = getattr(m, attr, None)
                    if fn is not None and inspect.isfunction(fn):
                        event = getattr(fn, '__app_event__', None)
                        if event is not None:
                            if self.__app_fns__.get(event, None) is None:
                                self.__app_fns__[event] = []
                            self.__app_fns__[event].append(fn)
