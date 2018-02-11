#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import signal

__author__ = 'Michael Liao'

import os, sys, time, subprocess

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from nory.infras.cli import CommandHost, command


def log(s):
    print('[Monitor] %s' % s)


class MyFileSystemEventHander(FileSystemEventHandler):
    def __init__(self, fn):
        super(MyFileSystemEventHander, self).__init__()
        self.restart = fn

    def on_any_event(self, event):
        if event.src_path.endswith('.py'):
            log('Python source file changed: %s' % event.src_path)
            self.restart()


class Hotting(object):
    def __init__(self, version=1, tasks=None):
        self.version = version
        self.tasks = [] if tasks is None else tasks

    @classmethod
    def parse(cls, filename='.hottings'):
        if not os.path.exists(filename):
            raise FileExistsError(filename)
        h = cls()
        return h

    async def start(self):
        for t in self.tasks:
            await t.start()
            
    def start_and_watch(self):
        self.start()
        self.watch()

    def watch(self):
        observer = Observer()
        for t in self.tasks:
            observer.schedule(MyFileSystemEventHander(t.restart), t.src, recursive=True)
            log('Watching directory %s...' % t.src)

        observer.start()

        try:
            while True:
                time.sleep(0.5)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()


class HottingTask(object):
    def __init__(self, cmd=None, src=None, reload=True):
        self.cmd = cmd
        self.src = src
        self.reload = reload

    async def start(self):
        self.process = subprocess.Popen(self.cmd, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)

    def stop(self):
        self.process.send_signal(signal.SIGTERM)

    def kill(self):
        self.process.kill()

    def restart(self):
        self.kill()
        self.start()


@command(name='start')
async def start_hotting(filename='.hottings'):
    h = Hotting.parse(filename)
    await h.start()


if __name__ == '__main__':
    host = CommandHost()
    host.register(start_hotting)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        host.run_command(' '.join(sys.argv[1:])))