"""
__auth__
"""
import inspect
import os
import importlib

import functools


def plugin_fn(event, name, description):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)

        wrapper.__plugin_event__ = event
        wrapper.__plugin_name__ = name
        wrapper.__plugin_description__ = description

        return wrapper

    return decorator


class Plugin(object):
    __plugin__ = 'plugin'

    def __init__(self):
        self.features = []


class PluginManager(dict):
    def __init__(self):
        self.plugins = []
        self.__auth__ = []

    def load_plugins(self):
        abs_p = os.path.abspath('.')
        abs_p = abs_p[:abs_p.find('tests')]
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
