from datetime import datetime

from infrastructures.utils import singleton

import requests


def app_hash(name, version):
    return hash('{}{}'.format(name, version))


class UpdateItem(object):
    def __init__(self, old_version, new_version, at):
        self.old_version = old_version
        self.new_version = new_version
        self.at = at


class AppInfoLockItem(object):
    def __init__(self, name, version):
        self.name = name
        self.version = version
        self.hash = app_hash(name, version)
        self.created_at = datetime.now()
        self.last_updated_at = datetime.now()
        self.update_records = []


class LockFileInfo(object):

    def __init__(self):
        self.apps = []
        self.created_at = datetime.now()
        self.last_updated_at = datetime.now()

    @property
    def total(self):
        return len(self.apps)


@singleton
class AppStoreClient(object):

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


def app_exist(app_name):
    pass


class Installer(object):

    def __init__(self):
        self.store = AppStoreClient()

    async def install_app(self, name):
        """install a app by app name"""
        if not app_exist(name):
            self.store.download(name)

    async def lock(self):
        """Create lockfile extensions.lock"""
        pass

    async def uninstall_app(self, name):
        """Uninstall app by name"""
        pass

    async def install_all_pre_installed_app(self):
        """Install all pre installed app when ncms first started"""
        pass

    async def update(self, apps):
        """Update extensions"""
        pass



