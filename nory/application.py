#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import logging
import signal
from nory.infras.envs.models import Environment as NoryEnvironment
from nory.infras.exts.managers import ExtensionManager
from nory.infras.exts.models import ExtensionLoader
from nory.infras.web.models import Jinja2Options, WebOptions
from nory.infras.web.nweb import NoryWebService


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

        jinja2_options = Jinja2Options()
        self.env.configuration.option('jinja2', jinja2_options)

        web_options = WebOptions()
        web_options = self.env.configuration.option('web', web_options)

        nory = NoryWebService(_logger=logger, _ext_manager=extension_manager, _jinja2_options=jinja2_options,
                              _web_options=web_options)
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(nory.init(self.loop))
        self.loop.run_forever()
