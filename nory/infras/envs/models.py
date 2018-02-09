

class Configuration(dict):
    __mappings__ = {}

    def option(self, key, cls):
        values = self.__mappings__.get(key, dict())
        o = cls(**values)
        return o

    def __setattr__(self, key, value):
        self[key] = value

    def __getattr__(self, item):
        return self[item]


class Environment(object):
    name = 'nory'
    mode = 'Development'
    configuration = Configuration()

    def __init__(self, name='nory', mode='Development', **kwargs):
        self.name = name
        self.mode = mode
        for key, val in kwargs.items():
            self.configuration[key] = val
