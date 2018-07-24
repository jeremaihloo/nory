import logging

import os
import yaml

from nory.infras.exts.models import ExtensionInfo


class ExtensionInfoLoader(object):
    """app.yaml"""

    def __init__(self, env, ext_loader):
        self.env = env
        self.ext_loader = ext_loader

    def load(self, name) -> ExtensionInfo:

        path = None

        for p in self.ext_loader.paths:
            path_dir = os.path.join(p, name)
            if os.path.exists(path_dir):
                path = path_dir
        if not path:
            raise FileNotFoundError('{}'.format(name))

        path = os.path.join(path, 'app.yaml')
        app_info = yaml.load(open(path))
        logging.debug('app_info from yaml:{}'.format(app_info))
        app_info = ExtensionInfo(
            name=name,
            author=app_info.get('author', ''),
            version=app_info.get('version', ''),
            description=app_info.get('description', ''),
            home_page=app_info.get('home_page'),
            indexs=app_info.get('indexs', []),
            dependency=app_info.get('dependency', []),
            static=app_info.get('static', {}),
            enabled=app_info.get('enabled', False),
            locale=app_info.get('locale', {}),
            load_path=path_dir
        )
        return app_info
