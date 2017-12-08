
import json
import logging

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


def load_options():
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


load_options()


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
    debug = False
    db_user = 'root'
    db_password = 'root'
    db_database = 'ncms'
    secret = 'ncms'

if __name__ == '__main__':
    print(NcmsConfig.version)
