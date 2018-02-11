import logging

from nory.application import NoryHost
from nory.infras.envs import modes
from nory.infras.envs.config_loaders import ConfigurationBuilder
from nory.infras.envs.models import Environment
from nory.infras.web.nweb import NoryWebService


class NcmsWebService(NoryWebService):
    name = '__main__'


if __name__ == '__main__':
    env = Environment(mode=modes.Development)
    env.configuration = ConfigurationBuilder(env).add_file_by_prefix('appsettings').build()

    host = NoryHost(name='nory', env=env, logger=logging.getLogger(__name__))
    host.start()
