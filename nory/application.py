#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import logging
import signal
import envtypes
import os
from infras.envs.models import Environment as NoryEnvironment, Configuration
from infras.exts.coros import AppManager
from infras.web.models import Jinja2Options, WebOptions
from infras.web.nweb import NoryWebService


class NoryHost(object):

    def __init__(self, name='nory', env: NoryEnvironment = None, logger: logging.Logger = None):
        self.name = name
        self.env = env if env is not None else NoryEnvironment(name=self.name)
        self.logger = logger

    def set_env_mode_from_sys_env(self):
        mode = os.environ.get('mode', envtypes.Development)
        self.env.mode = mode

    def add_config_from_file(self, filename):
        pass

    def start(self):
        logger = self.logger.getChild('nory')
        app_manager = AppManager()
        jinja2_options = self.env.configuration.option('jinja2', Jinja2Options)
        web_options = self.env.configuration.option('web', WebOptions)
        nory = NoryWebService(_logger=logger, _app_manager=app_manager, _jinja2_options=jinja2_options,
                              _web_options=web_options)
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(nory.init(self.loop))


def graceful(env: NoryEnvironment):
    n = Nory(env)

    def onSigInt(signo, frame):
        print('Shutdown...')
        n.shutdown()

    def onSigTerm(signo, frame):
        print('Shutdown...')
        n.shutdown()

    def onSigKill(signo, frame):
        print('Shutdown...')
        n.shutdown()

    signal.signal(signal.SIGINT, onSigInt)
    signal.signal(signal.SIGTERM, onSigTerm)

    return n
