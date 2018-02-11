from nory.infras.envs import modes
from nory.infras.envs.config_loaders import get_config_by_path_value, FileConfigLoader, ConfigurationBuilder
from nory.infras.envs.models import Environment, Configuration


def test_config_base():
    config = Configuration()
    config.mode = 'test'
    assert config['mode'] == 'test'


def test_get_config_by_path_value():
    config = get_config_by_path_value('db.mysql.host', '127.0.0.1')
    assert config['db']['mysql']['host'] == '127.0.0.1'


def test_json_file_loader():
    loader = FileConfigLoader('appsettings.json')
    config = loader.load()
    assert config['load_from'] == 'json'
    assert config['mode'] == 'Default'


def test_yml_file_loader():
    loader = FileConfigLoader('appsettings.Production.yml')
    config = loader.load()
    assert config['load_from'] == 'yml'
    assert config['mode'] == 'Production'


def test_builder_add_file_by_name():
    builder = ConfigurationBuilder(Environment(modes.Development))
    builder.add_file_by_name('appsettings.json')
    config = builder.build()
    assert config['load_from'] == 'json'
    assert config['mode'] == 'Default'


def test_builder_add_file_by_prefix():
    builder = ConfigurationBuilder(Environment(modes.Development))
    builder.add_file_by_prefix('appsettings')
    config = builder.build()
    assert config['load_from'] == 'json'
    assert config['mode'] == 'Development'


def test_builder_add_by_mode():
    builder = ConfigurationBuilder(Environment(modes.Development))
    builder.add_by_env_mode(modes.Development)
    config = builder.build()

    assert config['load_by'] == 'mode'
    assert config['load_from'] == 'json'
    assert config['mode'] == 'option_overide'
    assert config.load_by == 'mode'
    assert config.mode == 'option_overide'


class AppSettings(Configuration):
    def __init__(self):
        self.url = 'option_test'


def test_option():
    builder = ConfigurationBuilder(Environment(modes.Development))
    builder.add_file_by_prefix('option')
    config = builder.build()
    o = AppSettings()
    config.option('web', o)
    assert o['url'] == 'localhost'
    assert o.url == 'localhost'
