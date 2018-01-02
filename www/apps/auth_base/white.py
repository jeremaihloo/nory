import logging

import functools

__urls__ = []


def allow_anyone(func):
    global __urls__

    current_path = getattr(func, '__route__', '/')
    __urls__.append(current_path)
    logging.info('[allow_anyone] {}'.format(current_path))

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper
