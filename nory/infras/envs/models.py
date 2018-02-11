from . import modes


class Configuration(dict):
    def __init__(self, names=(), values=(), **kw):
        super(Configuration, self).__init__(**kw)
        for k, v in zip(names, values):
            self[k] = v

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    def option(self, key, obj):
        values = self.get(key, dict())

        obj.update(values)
        return obj


class Environment(object):
    name = 'nory'
    mode = modes.Default
    configuration = Configuration()

    def __init__(self, name='nory', mode='Development', **kwargs):
        self.name = name
        self.mode = mode
        for key, val in kwargs.items():
            self.configuration[key] = val
