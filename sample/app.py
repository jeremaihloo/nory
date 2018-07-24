import os
from nory.infras.web.middlewares import logger_factory, auth_factory, data_factory, response_factory
from nory.infras.web.nweb import WebBuilder

import sys
sys.path.append(os.path.abspath(os.curdir))

if __name__ == '__main__':
    root_path = os.path.dirname(__file__)

    web_builder = WebBuilder('sample', root_path)
    web_builder.env.configuration.add_file_by_prefix('appsettings', follow_mode=False)
    web_builder.use_middlewares([logger_factory, auth_factory, data_factory, response_factory])
    web_builder.use_ext_manager(['extensions'])

    web_builder.build().start()
