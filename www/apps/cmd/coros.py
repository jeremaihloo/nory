import functools
import inspect

from infrastructures.web.coros import has_var_kw_arg, has_named_kw_args, get_named_kw_args, get_required_kw_args

__commands__ = []


def command(name=None, description=''):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)

        wrapper.name = name
        wrapper.description = description

        __commands__.append(wrapper)

        return wrapper

    return decorator


class CommandHandler(object):
    def __init__(self, fn):
        self._func = fn
        self._has_var_kw_arg = has_var_kw_arg(fn)
        self._has_named_kw_args = has_named_kw_args(fn)
        self._named_kw_args = get_named_kw_args(fn)
        self._required_kw_args = get_required_kw_args(fn)

    def __call__(self, *args, **kwargs):
        kw = {}
        func_arg_sns = inspect.signature(self._func).parameters.keys()

        for index, item in enumerate(func_arg_sns):
            if index < len(args):
                if (item not in self._named_kw_args) and (item not in self._required_kw_args):
                    kw[item] = args[index]

        for key, val in kwargs.items():
            kw[key] = val

        return self._func(**kw)


def parse_command_args(line):
    args = []
    kw = {}
    for item in line.split(' '):
        if item.startswith('--'):
            split_array = item.split('=')
            kw[split_array[0][2:]] = convert_data(split_array[1])
        else:
            args.append(item)
    return args, kw


async def run_command(line):
    global __commands__
    args, kw = parse_command_args(line)
    for item in __commands__:
        name = getattr(item, 'name')
        if name == args[0]:
            fn = CommandHandler(item)
            r = await fn(*args[1:], **kw)
            print('command [{}] ok ! {}'.format(line, r if r is not None else ''))
            return True
    print('command [{}] not found'.format(line))
    return False


def convert_data(val: str):
    if val == 'true':
        return True
    if val == 'false':
        return False
    if val.isdigit():
        return int(val)
    return val


@command(name='configs', description='get the configs')
async def get_configs(name, debug=True):
    print(name)
    print(debug)
    if debug:
        return '/etc/lujiejie.json'
