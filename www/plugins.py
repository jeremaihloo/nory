"""
__auth__
"""
import inspect
import logging
import os
import importlib

import functools

import utils
from coroweb import get


def plugin_fn(event, name, description):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)

        wrapper.__plugin_event__ = event
        wrapper.__plugin_fn_name__ = name
        wrapper.__plugin_fn_description__ = description

        return wrapper

    return decorator


class Plugin(object):
    __plugin__ = 'plugin'

    def __init__(self):
        self.features = []


@utils.singleton
class PluginManager(utils.DictClass):
    def __init__(self):
        self.plugins = []
        self.__auth__ = []
        self.__auth_false__ = []
        self.__routes__ = []

    def reload_plugins(self):
        self.plugins = []
        self.__auth__ = []
        self.__auth_false__ = []
        self.__routes__ = []

        self.load_plugins()

    def load_plugins(self):
        logging.info('loading plugins')
        abs_p = utils.get_ncms_path()
        plugin_modules = os.listdir(os.path.join(abs_p, 'installed_plugins'))
        plugin_modules = list(filter(lambda x: not x.startswith('_'), plugin_modules))
        for item in plugin_modules:
            p = importlib.import_module('installed_plugins.{}'.format(item[:-3]))
            self.plugins.append(p)

        self.category_plugins()

    # TODO: pythonic
    def category_plugins(self):
        for p in self.plugins:
            for attr in dir(p):
                fn = getattr(p, attr, None)
                if fn is not None and inspect.isfunction(fn):
                    event = getattr(fn, '__plugin_event__', None)
                    if event is not None:
                        if self.get(event, None) is None:
                            self[event] = []
                        self[event].append(fn)

    def get_plugin_infos(self):
        for p in self.plugins:
            info = {
                'author': getattr(p, '__author__', 'None'),
                'version': getattr(p, '__version__', 'None'),
                'description': getattr(p, '__description__', 'None'),
                'home_page': getattr(p, '__home_page__', 'None')
            }
            yield info

    def get_events(self):
        return (
            '__auth__',
            '__auth_false__',
            '__routes__'
        )

    def get_features(self):
        features = []
        for event in self.get_events():
            features.extend(self[event])
        return features
