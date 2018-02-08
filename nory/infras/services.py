import asyncio

from infras.di import IService


class LocalServiceMixin(object):

    async def initialize(self, loop=None):
        pass


class LocalService(IService, LocalServiceMixin):

    def start(self):
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.initialize(self.loop))


class IRemoteService(IService):
    pass


class WebService(LocalService):
    pass


class RpcService(IRemoteService):
    pass


class WebsocketService(IRemoteService):
    pass
