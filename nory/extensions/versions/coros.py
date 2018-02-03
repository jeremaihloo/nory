from extensions.versions.models import Version
from infrastructures.dbs import objects

def get_app_last_version(app_name):
    version = objects.get(Version.select().where(Version.app == app_name).order_by(Version.app_version))
    return version

