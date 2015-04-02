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

@cli.command()
@click.option('--list', is_flag=True, flag_value=True, help='list available images')
@click.argument('url')
@click.argument('username')
@click.password_option(help='password for VCL site')
@pass_config
def image(config, list, url, username, password):
    make_config(config, url, username, password)
    if list:
        response = config.api.get_images()
        click.echo(response)

@cli.command()
@click.option('--add', help='add request', is_flag=True, flag_value=True)
@click.option('--image-id', type=click.INT, help='image ID for request')
@click.option('--start', help='unix timestamp for request start time')
@click.option('--length', type=click.INT, help='length of request in 15 minute increments')
@click.option('--end', help='end request', is_flag=True, flag_value=True)
@click.option('--request-id', help='request ID', type=click.INT)
@click.option('--list', is_flag=True, flag_value=True)
@click.argument('url')
@click.argument('username')
@click.password_option(help='password for VCL site')
@pass_config
def request(config, add, image_id, start, length,\
        end, request_id, \
        list, \
        url, username, password):
    make_config(config, url, username, password)
    if add:
        if start is None:
            start = "now"
        if length is None:
            length = 15
        response = config.api.add_request(image_id, start, length)
        click.echo(response)
    elif end:
        response = config.api.end_request(request_id)
        click.echo(response)
    elif list:
        response = config.api.get_requestIds()
        click.echo(response)
