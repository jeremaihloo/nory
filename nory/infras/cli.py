import asyncio
import functools
import inspect

from nory.infras.utils import singleton, nameof, descriptionof
from nory.infras.web.req import has_var_kw_arg, has_named_kw_args, get_named_kw_args, get_required_kw_args

__commands__ = []

class CommandExistsError(Exception):
    pass

def find_cmd_fn(cmd):
    global __commands__
    for item in __commands__:
        if cmd == getattr(item, 'name'):
            return item
    return None

def command(name=None, description=''):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)

        wrapper.name = name
        wrapper.description = description
        if find_cmd_fn(name) is not None:
            raise CommandExistsError
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

    def help(self):
        template = """{name}    {desc}
          {options} """
        return template.format(name=nameof(self._func),
                               desc=descriptionof(self._func),
                               options='\n--'.join(self._named_kw_args))


class CommandDescriptor(object):

    def __init__(self, cmd, args, options, fn: CommandHandler):
        self.cmd = cmd
        self.args = args
        self.options = options
        self.fn = fn

    def to_cmd_line(self):
        pass


@command(name='help')
async def help(*args, **kwargs):
    print('\nUsage: \n')

    print('Avaiable Commands:\n')
    global __commands__
    for val in __commands__:
        handler = CommandHandler(val)
        print(handler.help())
    return True


def parse_command_descriptor(line) -> CommandDescriptor:
    args = []
    kw = {}
    for item in line.split(' '):
        if item.startswith('--'):
            split_array = item.split('=')
            if len(split_array) == 2:
                kw[split_array[0][2:]] = convert_cmd_options(split_array[1])
            else:
                kw[split_array[0][2:]] = True
        else:
            args.append(item)
    cmd = 'help' if len(args) == 0 else args[0]

    def find_cmd_fn(cmd):
        global __commands__
        for item in __commands__:
            if cmd == getattr(item, 'name'):
                return item
        return None

    fn = find_cmd_fn(cmd)

    return CommandDescriptor(cmd, [] if len(args) == 0 else args[1:], kw, fn)


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

    def register(self, cmd):
        global __commands__
        __commands__.append(cmd)

    async def run_command(self, line):
        global __commands__
        descriptor = parse_command_descriptor(line)

        def find_item(n=None):
            for item in __commands__:
                name = getattr(item, 'name')
                if name is None:
                    name = getattr(item, '__name__')
                if name == n:
                    return item
            return None

        item = find_item(descriptor.cmd)
        if item is None:
            item = find_item('help')

        fn = CommandHandler(item)
        r = await fn(*descriptor.args, **descriptor.options)
        if isinstance(r, str):
            print(r)
        return True


@command(name='environments', description='get the environments')
async def get_configs(name, debug=True):
    print(name)
    print(debug)
    if debug:
        return '/etc/lujiejie.json'


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(CommandHost().run_command('environments lujiejie --debug=False'))
