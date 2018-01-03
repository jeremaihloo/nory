import click
import importlib


@click.group(name='gen')
@click.option('--api_paths', default='apps/admin/handlers:apps/core/handler', help='Path to api handlers')
def generate():
    pass


@generate.command()
def generate_apis():
    pass


@generate.command()
def generate_mutation_types():
    pass


@generate.command()
def generate_actions():
    pass
