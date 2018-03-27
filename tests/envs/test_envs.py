from nory.infras.envs import modes
from nory.infras.envs.configs import get_config_by_path_value, FileConfigLoader
from nory.infras.envs.configs import Configuration


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
    configuration = Configuration()
    configuration.add_file_by_name('appsettings.json')
    assert len(configuration.config_files) == 1
    assert configuration['load_from'] == 'json'
    assert configuration['mode'] == 'Default'


def test_builder_add_file_by_prefix():
    configuration = Configuration()
    configuration.add_file_by_prefix('appsettings')
    assert len(configuration.config_files) == 1
    configuration.add_file_by_prefix('appsettings', follow_mode=False)
    assert len(configuration.config_files) == 3
    assert configuration['load_from'] == 'json'
    assert configuration['mode'] == 'Development'


def test_builder_add_by_mode():
    configuration = Configuration()
    configuration.add_by_env_mode(modes.Development)
    assert configuration['load_by'] == 'mode'
    assert configuration['load_from'] == 'json'
    assert configuration['mode'] == 'option_overide'
    assert configuration.load_by == 'mode'
    assert configuration.mode == 'option_overide'


class AppSettings(Configuration):
    def __init__(self):
        self.url = 'option_test'


def test_option():
    configuration = Configuration()
    configuration.add_file_by_prefix('option')
    o = AppSettings()
    o = configuration.option('web', o)
    assert o['url'] == 'localhost'
    assert o.url == 'localhost'
