from infrastructures.apps import features


class AppInfo(object):
    def __init__(self, name, version, description, author, home_page, indexs, dependency, static, enabled, locale):
        self.name = name
        self.version = version
        self.description = description
        self.author = author
        self.home_page = home_page
        self.indexs = indexs
        self.dependency = dependency
        self.static = static
        self.enabled = enabled
        self.locale = locale

class App(object):
    def __init__(self, info):
        self.info = info
        self.features = {}
        for item in dir(features):
            if item.startswith('__FEATURE'):
                self.features[item] = []

    def on_installing(self):
        pass

    def on_loading(self):
        pass

    def on_uninstall(self):
        pass

    def on_enable_feature(self):
        pass

    def on_disable_feature(self):
        pass
