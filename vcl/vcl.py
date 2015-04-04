import click
import getpass
from vclapi import VCLApi

class Config(object):
    def __init__(self):
        self.url = None
        self.username = None
        self.password = None
        self.api = None

pass_config = click.make_pass_decorator(Config, ensure=True)

def make_config(config, url, username, password):
    config.url = url
    config.username = username
    config.password = password
    config.api = VCLApi(config.url, config.username, config.password)

@click.group()
@click.version_option()
@pass_config
def cli(config):
    pass

@cli.command()
@click.option('--string', help='string to send to VCL Site', default='Hello World!')
@click.argument('url')
@click.argument('username')
@click.password_option(help='password for VCL site')
@pass_config
def test(config, string, url, username, password):
    make_config(config, url, username, password)
    response = config.api.test(string)
    click.echo(response)

@cli.group()
@pass_config
def image(config):
    pass

@image.command()
@pass_config
@click.argument('url')
@click.argument('username')
@click.password_option(help='password for VCL site')
def list(config, url, username, password):
    make_config(config, url, username, password)
    response = config.api.get_images()
    click.echo(response)


@cli.group()
@pass_config
def request(config):
    pass

@request.command()
@click.option('--image-id', type=click.INT, help='image ID for request')
@click.option('--start', help='unix timestamp for request start time')
@click.option('--length', type=click.INT, help='length of request in 15 minute increments')
@click.argument('url')
@click.argument('username')
@click.password_option(help='password for VCL site')
@pass_config
def add(config, image_id, start, length, url, username, password):
    make_config(config, url, username, password)
    if start is None:
        start = "now"
    if length is None:
        length = 15
    response = config.api.add_request(image_id, start, length)
    click.echo(response)

@request.command()
@pass_config
@click.option('--request-id', help='request ID', type=click.INT)
@click.argument('url')
@click.argument('username')
@click.password_option(help='password for VCL site')
def end(config, request_id):
    make_config(config, url, username, password)
    response = config.api.end_request(request_id)
    click.echo(response)

@request.command()
@pass_config
@click.argument('url')
@click.argument('username')
@click.password_option(help='password for VCL site')
def list(config, url, username, password):
    make_config(config, url, username, password)
    response = config.api.get_requestIds()
    click.echo(response)

@request.command()
@pass_config
@click.argument('request-id')
@click.argument('url')
@click.argument('username')
@click.password_option(help='password for VCL site')
def status(config, request_id, url, username, password):
    make_config(config, url, username, password)
    response = config.api.get_request_status(request_id)
    click.echo(response)
