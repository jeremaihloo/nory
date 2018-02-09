import json
import logging
import sys
import os

import yaml
from infras.envs.models import Configuration


class ConfigLoader(object):
    def __init__(self):
        self.configs = {}
        self.config_hash = None

    def load(self):
        return self.configs


def json_file_config_load_handler(path):
    return json.load(open(path))


def yaml_file_config_load_handler(path):
    return yaml.load(open(path))


__config_file_loaders__ = {
    '.json': json_file_config_load_handler,
    '.yaml': yaml_file_config_load_handler,
    '.yml': yaml_file_config_load_handler
}


class FileConfigLoader(ConfigLoader):

    def load(self):
        files = os.listdir('./runnings/environments')
        sorted(files)
        for item in files:
            ext = os.path.splitext(item)[1]
            try:
                handler = __config_file_loaders__.get(ext, None)
                if handler is None:
                    logging.warning('[file_config_loader] [{}] file load handler not found !'.format(ext))
                    continue
                m = handler(item)
                self.configs.update(m)
            except FileNotFoundError as e:
                pass
        return self.configs


class CommandLineConfigLoader(ConfigLoader):
    def load(self):

        for i in range(len(sys.argv)):
            item = sys.argv[i]
            if item.startswith('--'):
                if item.find('=') <= -1:
                    self.configs[item[2:]] = True
                else:
                    item_arr = item.split('=')
                    key = item_arr[0][2:]
                    val = item_arr[1]
                    if isinstance(val, str) and val in ['False', 'True']:
                        val = True if val == 'True' else False
                    self.configs[key] = val
            else:
                pass
        return self.configs


__configs_loaders = [
    FileConfigLoader,
    CommandLineConfigLoader
]


class ConfigurationBuilder(object):

    def build(self) -> Configuration:
        global __configs_loaders
        __configs__ = dict()
        for loader in __configs_loaders:
            cfs = loader().load()
            __configs__.update(cfs)
        return Configuration(**__configs__)
