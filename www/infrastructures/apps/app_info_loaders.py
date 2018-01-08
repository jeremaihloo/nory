import importlib
import logging

import os
import yaml

from infrastructures.apps.models import AppInfo


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
