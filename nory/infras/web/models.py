from infras.envs.models import Configuration


class Jinja2Options(Configuration):
    autoescape = True
    block_start_string = '{%'
    block_end_string = '%}'
    variable_start_string = '{{'
    variable_end_string = '}}'
    auto_reload = True


class WebOptions(Configuration):
    host = '0.0.0.0'
    port = 9000