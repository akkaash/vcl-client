import click
import getpass
from vclapi import VCLApi

class Config(object):
    def __init__(self):
        self.url = None
        self.username = None
        self.password = None

pass_config = click.make_pass_decorator(Config, ensure=True)

@click.group()
@click.argument('url', type=click.STRING)
@click.argument('username')
@pass_config
def cli(config, url, username):
    config.url = url
    config.username = username
    config.password = getpass.getpass()


@cli.command()
@click.option('--string', help='string to send to VCL Site', default='Hello World!')
@pass_config
def test(config, string):
    api = VCLApi(config.url, config.username, config.password)
    response = api.test(string)
    print response

@cli.group()
@pass_config
def image(config):
    pass

@image.command()
@pass_config
def list(config):
    api = VCLApi(config.url, config.username, config.password)
    response = api.get_images()
    click.echo(response)


@cli.group()
@pass_config
def request(config):
    pass

@request.command()
@click.argument('image_id')
@click.argument('start')
@click.argument('length')
@pass_config
def add(config, image_id, start, length):
    api = VCLApi(config.url, config.username, config.password)
    response = api.add_request(image_id, start, length)
    click.echo(response)
