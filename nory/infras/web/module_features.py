import logging
import os
from jinja2 import FileSystemLoader

from nory.infras import constants
from nory.infras.envs.configs import Environment
from nory.infras.exts import features
from nory.infras.exts.managers import ExtensionManager
from nory.infras.web.models import Jinja2Options
from jinja2 import Environment as Jinja2Enviroment

class UseModule(object):
    def initialize(self, app, _logger: logging.Logger, _ext_manager: ExtensionManager, env: Environment):
        raise NotImplementedError()


class JinJa2(UseModule):
    def initialize(self, app, _logger: logging.Logger, _ext_manager: ExtensionManager, env: Environment):
        kw = Jinja2Options()
        env.configuration.option('jinjia2', kw)
        _logger.info('[init jinja2] ...')
        options = dict(
            autoescape=kw.get('autoescape', True),
            block_start_string=kw.get('block_start_string', '{%'),
            block_end_string=kw.get('block_end_string', '%}'),
            variable_start_string=kw.get('variable_start_string', '{{'),
            variable_end_string=kw.get('variable_end_string', '}}'),
            auto_reload=kw.get('auto_reload', True)
        )
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'extensions')
        _logger.info('[init_jinja2] set jinja2 template path: %s' % path)

        env = Jinja2Enviroment(loader=FileSystemLoader(path), **options)
        filters = _ext_manager.get_worked_features(features.__FEATURE_TEMPLATE_FILTER__)
        if filters is not None:
            for f in filters:
                env.filters[getattr(f, constants.FEATURE_NAME)] = f
        app['__templating__'] = env


class Statics(UseModule):
    def initialize(self, app, _logger: logging.Logger, _ext_manager: ExtensionManager, env: Environment):

        for item in _ext_manager.extensions.values():
            if not item.info.enabled:
                continue

            for k in item.info.static.keys():
                path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'extensions', item.info.name,
                                    item.info.static[k])
                try:
                    self.add_static(app, os.path.join(item.info.name, k), path, _logger)
                except Exception as e:
                    _logger.warning('[add_statics] add app [{}] static error'.format(item.info.name))

    def add_static(self, app, app_name, path, _logger):
        # path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
        if not os.path.exists(path):
            raise Exception('add static error dir not exists : {}'.format(path))
        app.router.add_static('/extensions/' + app_name, path)
        _logger.info('add static %s => %s' % ('/extensions/' + app_name, path))
