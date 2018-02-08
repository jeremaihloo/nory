#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import signal
import envtypes
from infras.di import Startup, IService
import os
from infras.envs.models import Environment as NoryEnvironment


class NoryHost(object):

    def __init__(self, name='nory', env: NoryEnvironment = None, startup: Startup = None):
        self.name = name
        self.env = env if env is not None else NoryEnvironment(name=self.name)
        self.startup = startup

    def set_env_mode_from_sys_env(self):
        mode = os.environ.get('mode', envtypes.Development)
        self.env.mode = mode

    def add_config_from_file(self, filename):
        pass

    def use_startup(self, startup: Startup):
        self.startup = startup if not callable(startup) else startup()
        self.startup.configure()

    def build(self) -> IService:
        entry = self.startup.entry_service()
        return entry


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
