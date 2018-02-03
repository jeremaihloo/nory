async def do_app_migrations(migrations):
    if not isinstance(migrations, list):
        migrations = [migrations]

    for item in migrations:
        await item()


app_migration_prefix = 'migration_'


def get_migrations_from_module(module):
    names = dir(module)
    names = [x for x in names if x.startswith(app_migration_prefix)]
    sorted(names)
    for name in names:
        fn = getattr(module, name, None)
        if fn is None:
            continue
        yield fn
