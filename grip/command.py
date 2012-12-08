"""\
grip.command
~~~~~~~~~~~~

Implements the command-line interface for Grip.


Usage:
  grip [options] [<path>] [<address>]
  grip -h | --help
  grip --version

Where:
  <path> is the path to the working directory of a content repository
  <address> is what to listen on, of the form <host>[:<port>], or just <port>
"""

import os
import sys
from path_and_address import resolve, split_address
from docopt import docopt
from .server import serve
from . import __version__


usage = '\n\n\n'.join(__doc__.split('\n\n\n')[1:])


def main(initial_args=None):
    """The entry point of the application."""
    if initial_args is None:
        initial_args = sys.argv[1:]
    version = 'Grip ' + __version__

    # Parse options
    args = docopt(usage, argv=initial_args, version=version)

    # Parse arguments
    path, address = resolve(args['<path>'], args['<address>'])
    host, port = split_address(address)
    directory, filename = _split(path)

    # Validate address
    if address and not host and not port:
        print 'Error: Invalid address', repr(address)

    # Run server
    try:
        serve(directory, filename, host, port)
    except ValueError, ex:
        print 'Error:', ex
        return 1

    return 0


def _split(path):
    """Returns (directory, filename) from the specified path."""
    if path is None:
        return None, None

    if path.endswith('.'):
        path += os.path.sep

    directory, filename = os.path.split(path)
    if filename == '':
        filename = None

    return directory, filename
