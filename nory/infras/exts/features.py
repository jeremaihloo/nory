import functools
import logging

__FEATURE_ROUTING__ = '__FEATURE_ROUTING__'
__FEATURE_AUTHING__ = '__FEATURE_AUTHING__'
__FEATURE_AUTH_FALSE__ = '__FEATURE_AUTH_FALSE__'
__FEATURE_BEFORE_REQUEST__ = '__FEATURE_BEFORE_REQUEST__'
__FEATURE_ADD_ROUTE__ = '__FEATURE_ADD_ROUTE__'
__FEATURE_TEMPLATE_FILTER__ = '__FEATURE_TEMPLATE_FILTER__'
__FEATURE_ON_APP_LOADING__ = '__FEATURE_ON_APP_LOADING__'
__FEATURE_ON_APP_INSTALLING__ = '__FEATURE_ON_APP_INSTALLING__'
__FEATURE_ON_APP_UNINSTALLING__ = '__FEATURE_ON_APP_UNINSTALLING__'
__FEATURE_WORKER__ = '__FEATURE_WORKER__'
__FEATURE_MENU_PROVIDER__ = '__FEATURE_MENU_PROVIDER__'
__FEATURE_TASK__ = '__FEATURE_TASK__'
__FEATURE_RESPONSE__ = '__FEATURE_RESPONSE__'
__FEATURE_ON_HANDLER_ARGS_INJECT__ = '__FEATURE_ON_HANDLER_ARGS_INJECT__'

__events_bus__ = {}


def subscribe(name):
    global __events_bus__

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            fns = __events_bus__.get(name, [])
            if len(fns) == 0:
                fns.append(func)
                __events_bus__[name] = fns
            else:
                __events_bus__[name].append(func)
            func(*args, **kwargs)

        return wrapper

    return decorator


async def publish(name, app, *args, **kwargs):
    global __events_bus__
    logging.info('[event] [publish] [{}]'.format(name))
    for item in __events_bus__.get(name, []):
        try:
            await item(app, *args, **kwargs)
            logging.error('[event] [publish] [{}] => [{}] [ok]'.format(name, item))
        except Exception as e:
            logging.error('[event] [publish] [{}] => [{}] [error]'.format(name, item))
    return True
