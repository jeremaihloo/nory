import hmac
import time
import uuid


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


def json_default(dt_fmt='%Y-%m-%d %H:%M:%S', date_fmt='%Y-%m-%d',
                 decimal_fmt=str):
    def _default(obj):
        if isinstance(obj, datetime):
            return obj.strftime(dt_fmt)
        elif isinstance(obj, date):
            return obj.strftime(date_fmt)
        elif isinstance(obj, Decimal):
            return decimal_fmt(obj)
        elif isinstance(obj, UUID):
            return str(obj)
        else:
            raise TypeError('%r is not JSON serializable' % obj)

    return _default


def json_dumps(obj, dt_fmt='%Y-%m-%d %H:%M:%S', date_fmt='%Y-%m-%d',
               decimal_fmt=str, ensure_ascii=True):
    return json.dumps(obj, ensure_ascii=ensure_ascii,
                      default=json_default(dt_fmt, date_fmt, decimal_fmt))
