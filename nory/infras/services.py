from nory.infras.envs.models import Environment


class Nory(object):

    def __init__(self, env: Environment):
        self.env = env

    def on_startup(self):
        raise NotImplementedError()

    def on_cleanup(self):
        raise NotImplementedError()
