import json
import logging
import os
import sys

__configs__ = None

__config_names = ['development', 'production']


def merge(defaults, override):
    r = {}
    for k, v in defaults.items():
        if k in override:
            if isinstance(v, dict):
                r[k] = merge(v, override[k])
            else:
                r[k] = override[k]
        else:
            r[k] = v
    return r


def load_options_from_config_file():
    global __configs__
    for item in __config_names:
        try:
            m = json.load(open('runnings/config.{}.json'.format(item)))
            if __configs__ is not None:
                __configs__ = merge(__configs__, m)
            else:
                __configs__ = m
            logging.info('runnings/config.{}.json loaded'.format(item))
        except FileNotFoundError as e:
            logging.warning('runnings/config.{}.json not found'.format(item))


def load_config_from_command_line():
    pairs = {}
    for i in range(len(sys.argv)):
        item = sys.argv[i]
        if item.startswith('--'):
            if item.find('=') <= -1:
                pairs[item[2:]] = True
            else:
                item_arr = item.split('=')
                key = item_arr[0][2:]
                val = item_arr[1]
                if isinstance(val, str) and val in ['False', 'True']:
                    val = True if val == 'True' else False
                pairs[key] = val
        else:
            pass
    logging.info('options from command line : {}'.format(pairs))
    global __configs__
    if __configs__ is not None:
        __configs__ = merge(__configs__, pairs)
    else:
        __configs__ = pairs


load_options_from_config_file()

load_config_from_command_line()


class ConfigMeta(type):

    def __getattribute__(self, item):
        val = super(ConfigMeta, self).__getattribute__(item)
        if isinstance(val, ConfigBase):
            raise Exception('just suport simple struct')
        val = __configs__[item] if __configs__.get(item, None) else val
        return val


class ConfigBase(object, metaclass=ConfigMeta):
    pass


class NcmsConfig(ConfigBase):
    version = 1
    debug = True

    db_user = 'root'
    db_password = 'root'
    db_database = 'ncms'

    secret = 'ncms'

    pre_installed_apps = ['core', 'admin', 'app_manager', 'app_store_client', 'auth_cookie', 'rbacm']


if __name__ == '__main__':
    print(NcmsConfig.version)
