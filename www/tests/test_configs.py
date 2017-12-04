import inspect
import json
import logging

__configs__ = dict()

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
            m = json.load(open('configs/{}.json'.format(item)))
            __configs__ = merge(__configs__, m)
            logging.info('configs/{}.json loaded'.format(item))
        except FileNotFoundError as e:
            logging.warning('configs/{}.json not found')


load_options()

print('fasfas')
print(__configs__)

class ConfigMeta(type):

    def __getattribute__(self, item):
        val = super(ConfigMeta, self).__getattribute__(item)
        if isinstance(val, ConfigBase):
            raise Exception('just suport simple struct')
        print(__configs__)
        return __configs__[item] if __configs__.get(item, None) else val


class ConfigBase(object, metaclass=ConfigMeta):
    pass


class ConfigDemo(ConfigBase):
    name = "hahaha"


def test_main():
    logging.basicConfig(level=logging.DEBUG)
    logging.debug(ConfigDemo.name)
