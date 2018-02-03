import functools
import inspect

from infrastructures.utils import singleton
from infrastructures.web.coros import has_var_kw_arg, has_named_kw_args, get_named_kw_args, get_required_kw_args


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


class CommandDescriptor(object):

    def __init__(self, cmd, args, options, fn):
        self.cmd = cmd
        self.args = args
        self.options = options
        self.fn = fn

    def to_cmd_line(self):
        pass


def parse_command_descriptor(line):
    args = []
    kw = {}
    for item in line.split(' '):
        if item.startswith('--'):
            split_array = item.split('=')
            kw[split_array[0][2:]] = convert_cmd_options(split_array[1])
        else:
            args.append(item)
    return CommandDescriptor(args[0], args[1:], kw, None)


def convert_cmd_options(val: str):
    if val in ('true', 'True', 1, '1'):
        return True
    if val in ('false', 'False', 0, '0'):
        return False
    if val.isdigit():
        return int(val)
    return val

@singleton
class CommandHost(object):
    commands = []

    async def register(self, cmd):
        self.commands.append(cmd)

    async def run_command(self, line):
        descriptor = parse_command_descriptor(line)
        for item in self.commands:
            name = getattr(item, 'name')
            if name == descriptor.cmd:
                fn = CommandHandler(item)
                r = await fn(*descriptor.args, **descriptor.options)
                print('command [{}] ok ! {}'.format(line, r if r is not None else ''))
                return True
        print('command [{}] not found'.format(line))
        return False


@command(name='configs', description='get the configs')
async def get_configs(name, debug=True):
    print(name)
    print(debug)
    if debug:
        return '/etc/lujiejie.json'
