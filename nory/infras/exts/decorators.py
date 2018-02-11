import functools

from nory.infras import constants


def feature(feature_type, name='', title='', description=''):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)

        setattr(wrapper, constants.FEATURE_TYPE, feature_type)
        setattr(wrapper, constants.FEATURE_NAME, name)
        setattr(wrapper, constants.FEATURE_TITLE, title)
        setattr(wrapper, constants.FEATURE_DESCRIPTION, description)

        return wrapper

    return decorator
