import click


@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug=False):
    pass


@cli.command()
def version():
    """ Version of Nory"""
    from ..version import version
    click.echo(version)


if __name__ == '__main__':
    cli()
