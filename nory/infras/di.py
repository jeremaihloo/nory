class DI(object):
    def __init__(self):
        self._container = {
            'singleton': {}
        }

    def find_by_names(self, names):
        r = {}
        for name in names:
            r[name] = self.find_singleton_by_name(name)
        return r

    def find_singleton_by_name(self, name):
        return self._container['singleton'].get(name, None)

    def assign_singleton(self, name, obj):
        self._container['singleton'][name] = obj


di = DI()
