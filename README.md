# VCL Client

A command line client, written in Python, for VCL using [click](http://click.pocoo.org).

__Please Note__: The project is still a work in progress and not near a release. Use Caution.

## Install

1. Clone this repository.
2. Create a new virtualenv. More information [here]()
3. `python setup.py install`

## Usage
```console
$ vcl --help
Usage: vcl [OPTIONS] COMMAND [ARGS]...

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  image
  request
  test
```

1. Adding new requests (reservations) to VCL

    ```console
    $ vcl request add --help
    Usage: vcl request add [OPTIONS] URL USERNAME

    Options:
      --image-id INTEGER  image ID for request
      --start TEXT        unix timestamp for request start time
      --length INTEGER    length of request in 15 minute increments
      --count INTEGER     number of requests
      --password TEXT     password for VCL site
      --help              Show this message and exit.
    ```

    Example: Add request for image 1234 for 2 hours.
    ```console
    $ vcl request add --image-id 1234 --length 120 "https://vcl.example.com/index.php?mode=xmlrpccall" "user@affiliation"
    ```
2. Ending requests in VCL

    ```console
    $ vcl request end --help
    Usage: vcl request end [OPTIONS] URL USERNAME

    Options:
      --request-id INTEGER  id of request to end
      --password TEXT       password for VCL site
      --help                Show this message and exit.
    ```
    Example:

    End a request of 98765
    ```console
    $ vcl request end --request-id 98765 "https://vcl.example.com/index.php?mode=xmlrpccall" "user@affiliation"
    ```

    Ending multiple requests
    ```console
    $ vcl request end --request-id 98765 --request-id 12345 "https://vcl.example.com/index.php?mode=xmlrpccall" "user@affiliation"
    ```

### Thank You
I would like to thank Josh Thompson for providing some seed code for VCLServerProxy and VCLTransport.
