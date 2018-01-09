
__configs__ = {}

__config_names = ['development', 'production']


class ConfigMeta(type):

    def __getattribute__(self, item):
        val = super(ConfigMeta, self).__getattribute__(item)
        if isinstance(val, ConfigBase):
            raise Exception('just suport simple struct')
        val = __configs__[item] if __configs__.get(item, None) else val
        return val


class ConfigBase(object, metaclass=ConfigMeta):
    pass


class NcmsConfig(ConfigBase):
    version = 1
    debug = True
    secret = 'ncms'
    pre_installed_apps = ['article', 'admin', 'app_manager', 'app_store_client', 'auth_cookie', 'rbacm']
    log_level = 'INFO'
    colored_log = True


class DbConfig(ConfigBase):
    db_host = 'localhost'
    db_user = 'root'
    db_password = 'root'
    db_database = 'ncms'
    db_port = '3306'
    db_charset = 'utf8mb4'