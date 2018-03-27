from nory.infras.envs.configs import Environment
from aiohttp import web


class FeatureContext(object):
    def __init__(self, env: Environment, app: web.Application = None, request: web.Request = None, **kwargs):
        self.env = env
        self.app = app
        self.request = request
        for key, val in kwargs.items():
            setattr(self, key, val)
