import hashlib
import logging
import time

from apps.article.models import User
from infrastructures.configs.models import NcmsConfig
from infrastructures.dbs import objects

COOKIE_NAME = 'ncms_auth_cookie'
_COOKIE_KEY = NcmsConfig.secret


async def cookie2user(cookie_str):
    """Parse cookie and load user if cookie is valid."""

    if not cookie_str:
        return None
    try:
        L = cookie_str.split(':')
        if len(L) != 3:
            raise Exception('login timeout')
            return None
        uid, expires, sha1 = L
        if int(expires) < time.time():
            raise Exception('login timeout')
            return None
        user = await objects.get(User.select().where(User.id == uid))
        if user is None:
            return None
        s = '%s:%s:%s:%s' % (uid, user.password, expires, _COOKIE_KEY)
        if sha1 != hashlib.sha1(s.encode('utf-8')).hexdigest():
            logging.info('invalid sha1')
            return None
        user.password = '******'
        return user
    except Exception as e:
        logging.exception(e)
        return None


def user2cookie(user, max_age):
    """
    Generate cookie str by user.
    """
    # build cookie string by: id-expires-sha1
    expires = str(int(time.time() + max_age))
    s = '%s:%s:%s:%s' % (str(user.id), user.password, expires, _COOKIE_KEY)
    L = [str(user.id), expires, hashlib.sha1(s.encode('utf-8')).hexdigest()]
    return ':'.join(L)
