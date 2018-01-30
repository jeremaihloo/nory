import os

from infrastructures.apps import features
from infrastructures.apps.decorators import feature

__resources__ = {}


def add_resource_file(name, path, title='', description='', cdn_domain=None):
    file = {
        'name': name,
        'path': path,
        'title': title,
        'description': description,
        'cdn_domain': cdn_domain
    }
    __resources__[name] = file


@feature(features.__FEATURE_TEMPLATE_FILTER__, 'resource', 'resource')
def resource(name, use_cdn=True):
    global __resources__
    res = __resources__.get(name, '')
    return os.path.join(res['cdn_domain'], res['path']) if use_cdn else res['path']
