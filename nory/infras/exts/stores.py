from datetime import datetime

import os

from nory.infras.utils import singleton

import requests

EXT_PACKAGE_FILE_NAME = 'extensions.json'
EXT_LOCK_FILE_NAME = 'extensions.lock.json'


def ext_hash(name, version):
    return hash('{}{}'.format(name, version))


class ExtensionStoreClient(object):

    def __init__(self, domain):
        self.domain = domain

        self.api_search = '/api/search/{key}'
        self.api_info = '/api/info/{name}'
        self.api_download_url = '/api/down/{name}/{version}.zip'

        self.path_app_package = './app-packages/{name}/{version}.zip'

    async def search(self, key):
        url = self.api_search.format(key=key)
        res = requests.get(url).json()
        return res

    async def info(self, name):
        url = self.api_info.format(name=name)
        return requests.get(url).json()

    async def download(self, name, version=0):
        url = self.api_download_url.format(name=name, version=version)
        res = requests.get(url, stream=True)
        if res.status_code == 200:
            with open(self.path_app_package.format(name=name, version=version)) as f:
                for chunk in res:
                    f.write(chunk)
