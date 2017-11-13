"""
__auth__
"""
import inspect
import logging
import os
import importlib

import functools

import utils

__EVENT_ROUTING__ = '__routing__'
__EVENT_AUTHING__ = '__authing__'
__EVENT_AUTH_FLASE__ = '__auth_false__'
__EVENT_REQUEST__ = '__request__'
__EVENT_ADD_ROUTE__ = '__add_route__'


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
        if not self.__app_fns__.get(__EVENT_ADD_ROUTE__, None):
            self.__app_fns__[__EVENT_ADD_ROUTE__] = []
        if not self.__app_fns__.get(__EVENT_AUTHING__, None):
            self.__app_fns__[__EVENT_AUTHING__] = []
        if not self.__app_fns__.get(__EVENT_AUTH_FLASE__, None):
            self.__app_fns__[__EVENT_AUTH_FLASE__] = []
        if not self.__app_fns__.get(__EVENT_ROUTING__, None):
            self.__app_fns__[__EVENT_ROUTING__] = []
        if not self.__app_fns__.get(__EVENT_REQUEST__, None):
            self.__app_fns__[__EVENT_REQUEST__] = []

    def reload_apps(self):
        self.__apps__ = []
        self.__app_fns__ = {}

        self.init_fns()

        self.load_apps()

    def load_apps(self):
        logging.info('loading plugins')
        abs_p = utils.get_ncms_path()
        apps = os.listdir(os.path.join(abs_p, 'apps'))

        apps = list(filter(lambda x: not x.startswith('_') and not x.endswith('.py'), apps))
        for item in apps:
            try:
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
                                event = getattr(fn, '__plugin_event__', None)
                                if event is not None:
                                    if self.get(event, None) is None:
                                        self.__app_fns__[event] = []
                                    self.__app_fns__[event].append(fn)
            except Exception as e:
                logging.warning(str(e))
