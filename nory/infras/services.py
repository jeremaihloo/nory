from infras.di import IService


class LocalService(IService):
    pass


class IRemoteService(IService):
    pass


class WebService(IRemoteService):
    pass


class RpcService(IRemoteService):
    pass


class WebsocketService(IRemoteService):
    pass
