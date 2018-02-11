from nory.infras.envs.models import Configuration


class Jinja2Options(Configuration):
    def __init__(self):
        self.autoescape = True
        self.block_start_string = '{%'
        self.block_end_string = '%}'
        self.variable_start_string = '{{'
        self.variable_end_string = '}}'
        self.auto_reload = True


class WebOptions(Configuration):
    def __init__(self):
        self.host = '0.0.0.0'
        self.port = 9000
