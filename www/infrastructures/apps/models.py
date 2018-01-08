from infrastructures import events


class AppInfo(object):
    def __init__(self, name, version, description, author, home_page, indexs, dependency, static, enabled):
        self.name = name
        self.version = version
        self.description = description
        self.author = author
        self.home_page = home_page
        self.indexs = indexs
        self.dependency = dependency
        self.static = static
        self.enabled = enabled


class App(object):
    def __init__(self):
        self.features = {}
        for item in dir(events):
            if item.startswith('__FEATURE'):
                self.features[item] = []
