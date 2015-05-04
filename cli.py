import time
import urllib

import click
from vcl import response
import vcl


class Config(object):
    def __init__(self):
        self.url = None
        self.username = None
        self.password = None
        self.api = None


pass_config = click.make_pass_decorator(Config, ensure=True)


def make_config(config, url, username, password):
    config.url = str(url).strip()
    config.username = str(username).strip()
    config.password = str(password).strip()
    config.api = vcl.VCL(config.url, config.username, config.password)


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
@click.option('--count', type=click.INT, help='number of requests', default=1)
@click.argument('url')
@click.argument('username')
@click.password_option(help='password for VCL site')
@pass_config
def add(config, image_id, start, length, count, url, username, password):
    make_config(config, url, username, password)
    if start is None:
        start = "now"
    if length is None:
        length = 60
    if count is None:
        count = 1
    vcl_responses = config.api.add_request(image_id, start, length, count)
    for vcl_response in vcl_responses:
        if isinstance(vcl_response, response.VCLRequestResponse):
            click.echo("{0}: {1}".format(vcl_response.vcl_response.status,
                                         vcl_response.request_id))
        elif isinstance(vcl_response, response.VCLErrorResponse):
            click.echo("{0}: {1}".format(vcl_response.vcl_response.status,
                                         vcl_response.error_message))


@request.command()
@pass_config
@click.argument('url', nargs=1)
@click.argument('username', nargs=1)
@click.option('--request-id', multiple=True, type=click.INT, help="id of request to end")
@click.password_option(help='password for VCL site')
def end(config, url, username, request_id, password):
    make_config(config, url, username, password)
    for req_id in request_id:
        res = config.api.end_request(req_id)
        click.echo(res)


@request.command()
@pass_config
@click.argument('url')
@click.argument('username')
@click.password_option(help='password for VCL site')
def list(config, url, username, password):
    make_config(config, url, username, password)
    res = config.api.get_request_ids()
    for res in res:
        click.echo(res)


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


@request.command()
@pass_config
@click.option('--remote-ip', help='IP address of connecting user')
@click.argument('request-id')
@click.argument('url')
@click.argument('username')
@click.password_option(help='password for VCL site')
def connect(config, remote_ip, request_id, url, username, password):
    make_config(config, url, username, password)
    # check reservation status
    res = config.api.get_request_status(request_id)
    while res['status'] == 'loading':
        click.echo('request %d is loading' % int(request_id))
        click.echo('est. load time: %d' % int(res['time']))
        click.echo('will retry in %d' % int(res['time']))
        time.sleep(res['time'] * 60)
        res = config.api.get_request_status(request_id)
        click.echo(res)
    if remote_ip is None:
        remote_ip = urllib.urlopen('http://myip.dnsomatic.com/').read().strip()
        click.echo(remote_ip)
    res = config.api.get_request_connect_data(request_id, remote_ip)
    click.echo(res)
