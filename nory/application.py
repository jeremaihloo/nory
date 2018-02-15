#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
from nory.infras.envs.models import Environment as NoryEnvironment
from nory.infras.exts.managers import ExtensionManager
from nory.infras.exts.models import ExtensionLoader
from nory.infras.web.models import WebOptions
from nory.infras.web.nweb import WebBuilder
from nory.infras.web.middlewares import logger_factory, auth_factory, data_factory, response_factory


class NoryHost(object):

    def __init__(self, ext_load_paths, name='nory', env: NoryEnvironment = None, logger: logging.Logger = None):
        self.name = name
        self.env = env if env is not None else NoryEnvironment(name=self.name)
        self.logger = logger
        self.ext_load_paths = ext_load_paths

    def start(self):
        logger = self.logger.getChild('nory')

        ext_loader = ExtensionLoader(paths=self.ext_load_paths, logger=logger.getChild('extension_loader'))

        extension_manager = ExtensionManager(ext_loader, logger=logger.getChild('extension_manager'))

        web_options = WebOptions()
        web_options = self.env.configuration.option('web', web_options)

        web_builder = WebBuilder(env=self.env, logger=logger, ext_manager=extension_manager, web_options=web_options)
        web_builder.use_middlewares([logger_factory, auth_factory, data_factory, response_factory])
        nory = web_builder.build()
        nory.on_startup()
