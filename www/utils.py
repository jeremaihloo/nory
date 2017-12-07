import hmac
import os
import time
import uuid


def get_ncms_path():
    cwd = os.getcwd()
    cwd = os.path.abspath(cwd)
    cwd = cwd[:cwd.find('ncms/www') + 8]
    return cwd


class DictClass(dict):
    def __getattr__(self, item):
        if self.get(item, None) is None:
            raise KeyError('{} key not exist !'.format(item))
        return self[item]

    def __setattr__(self, key, value):
        self[key] = value


def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton


def hash_pwd(password):
    hash = hmac.new('ncms'.encode('utf-8'))
    hash.update(password.encode('utf-8'))
    return hash.hexdigest()


def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)
