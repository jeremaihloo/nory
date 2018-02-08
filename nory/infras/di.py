from infras.utils import nameof, scopeof

SINGLETON = 'SINGLETON'
SCOPED = 'SCOPED'


class IService(object):
    pass


class ServiceProvider(object):
    __mappings__ = {}

    def __init__(self, mappings):
        self.__mappings__ = mappings

    def get_services(self, key):
        if not isinstance(key, str):
            key = nameof(key)
        return self.__mappings__.get(key)


class DiItem(object):
    def __init__(self, name, type, service):
        self.name = name
        self.type = type
        self.service = service


class Container(object):
    __mappings__ = {}

    def set(self, service, key=None, type=None):
        name = nameof(service) if key is None else key
        type = scopeof(service) if type is None else type

        if type == SINGLETON and callable(service):
            service = service()

        item = DiItem(name, type, service)
        if self.__mappings__.get(name) is None:
            self.__mappings__[name] = []
        self.__mappings__[name].append(item)

    def get(self, key):
        pass

    def add_single(self, item):
        self.set(item, type=SINGLETON)

    def add_scoped(self, interface, item):
        self.set(item, nameof(interface), type=SCOPED)

    def build(self) -> ServiceProvider:
        mappings = {}
        for key, cs in self.__mappings__.items():
            if len(cs) == 1:
                item = cs[0]
                if item.type == SINGLETON:
                    mappings[key] = item.service
            else:
                def items():
                    for item in cs:
                        if callable(item.service):
                            item = item.service()
                            yield item
                        else:
                            pass

                iss = items()
                mappings[key] = list(iss)
        return ServiceProvider(mappings)


class DemoSingletonService(IService):
    user_name = 'lujiejie'


class IDemoScopedServiceBase(IService):
    pass


class DemoScopedServiceA(IDemoScopedServiceBase):
    user_name = 'lidazhao'


class DemoScopedServiceB(IDemoScopedServiceBase):
    user_name = 'dadada'


if __name__ == '__main__':
    container = Container()
    container.add_single(DemoSingletonService)
    container.add_scoped(IDemoScopedServiceBase, DemoScopedServiceA)
    container.add_scoped(IDemoScopedServiceBase, DemoScopedServiceB)
    provider = container.build()
    se = provider.get_services(DemoSingletonService)
    assert se.user_name == DemoSingletonService.user_name

    ss = provider.get_services(IDemoScopedServiceBase)
    assert len(ss) == 2
    assert ss[0] != ss[1]
