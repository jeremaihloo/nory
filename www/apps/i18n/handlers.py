import json

from apps.auth_base.white import allow_anyone
from infrastructures import events
from infrastructures.apps.decorators import feature
from infrastructures.apps.models import AppInfo
from infrastructures.utils import singleton
from infrastructures.web.decorators import get


class I18NParser(object):
    @staticmethod
    def parse(self, file_name):
        pass


class I18NJsonParser(I18NParser):
    @staticmethod
    def parse(self, file_name):
        m = json.load(open(file_name))
        return m


@singleton
class I18N(object):
    def __init__(self):
        self.mapping = {}

    def load_from_app(self, app_info: AppInfo):
        for key, val in app_info.locale.items():
            lang = self.mapping.get(key, None)
            if lang is None:
                self.mapping[key] = {}
            m = I18NJsonParser.parse(val)
            for k, v in m.items():
                if self.mapping[key].get(k, None) is None:
                    self.mapping[key][k] = v


@allow_anyone
@feature(events.__FEATURE_ROUTING__, 'api_i18n_json', 'api_i18n_json')
@get('/api/i18n.json')
def api_i18n_json():
    return 200, I18N.mapping
