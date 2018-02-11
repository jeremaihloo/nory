import json
import sys
import os

import yaml

from infras.envs import modes
from infras.envs.models import Configuration, Environment


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


class FileConfigLoader(ConfigLoader):
    __config_file_loaders__ = {
        '.json': json_file_config_load_handler,
        '.yaml': yaml_file_config_load_handler,
        '.yml': yaml_file_config_load_handler
    }

    def __init__(self, filename: str, loaders: dict = None):
        self.filename = filename

        if loaders is not None:
            self.__config_file_loaders__.update(loaders)

    def load(self):
        ext = '.{}'.format(self.filename.split('.')[-1])
        handler = self.__config_file_loaders__[ext]
        self.configs = handler(self.filename)
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


def get_config_by_path_value(path, value, mapping: dict = None):
    if isinstance(path, str):
        path = path.split('.')

    if mapping is None:
        mapping = dict()

    if len(path) > 1:
        m = dict()

        get_config_by_path_value(path[1:], value, m)

        mapping[path[0]] = m
    else:
        mapping[path[0]] = value
    return mapping


def get_config_mode_by_filename(filename):
    parts = filename.split('.')
    for item in parts:
        if item in dir(modes):
            return item
    return modes.Default


class ConfigurationBuilder(object):
    def __init__(self, env: Environment):
        self.env = env
        self.loader_entities = []

    def add_file_by_prefix(self, filename_prefix: str):
        paths = os.path.split(filename_prefix)
        d, filename = os.path.join('./' if paths[0] == '' else paths[0]), paths[-1]
        files = os.listdir(d)
        config_files = [x for x in files if x.startswith(filename_prefix)]
        config_files = [x for x in config_files if get_config_mode_by_filename(x) == self.env.mode]

        for item in config_files:
            self.add_file_by_name(os.path.join(d, item))
        return self

    def add_file_by_name(self, filename):
        loader = FileConfigLoader(filename)
        self.env.configuration.update(loader.load())
        self.loader_entities.append(loader)
        return self

    def add_by_env_mode(self, mode=None, dir_path='.'):
        if mode is None:
            mode = self.env.mode

        files = os.listdir(dir_path)
        files = [x for x in files if os.path.splitext(x)[1] in FileConfigLoader.__config_file_loaders__.keys()]
        files = [x for x in files if get_config_mode_by_filename(x) == mode]

        for item in files:
            self.add_file_by_name(os.path.join(dir_path, item))
        return self

    def set(self, path, value):
        m = get_config_by_path_value(path, value)
        self.env.configuration.update(m)
        return self

    def build(self) -> Configuration:
        return self.env.configuration
