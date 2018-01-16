from apps.versions.models import Version
from infrastructures.apps.models import AppInfo
from infrastructures.dbs import objects


def get_app_last_version(app_name):
    version = objects.get(Version.select().where(Version.app == app_name).order_by(Version.app_version))
    return version


def get_app_db_migration_func_name(app_info: AppInfo):
    return '{app_name}_db_migration_{old_version}_to_{new_version}'.format(
        app_name=app_info.name,
        old_version=get_app_last_version(app_name=app_info.name),
        new_version=app_info.version
    )
