import functools


def feature(event, name='', title='', description=''):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)

        wrapper.__app_event__ = event
        wrapper.__app_fn_name__ = name
        wrapper.__app_fn_title__ = title
        wrapper.__app_fn_description__ = description

        return wrapper

    return decorator
