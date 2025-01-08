"""CLI interface for version ranges."""

import argparse
import logging
import sys
from typing import Union

import versioalueet.api as api
import versioalueet.env as env
from versioalueet import APP_ALIAS, APP_NAME, DEBUG, VERSION, log


def parse_request(argv: list[str]) -> Union[int, argparse.Namespace]:
    """Parse the command line arguments received."""
    parser = argparse.ArgumentParser(
        prog=APP_ALIAS, description=APP_NAME, formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '-q',
        '--quiet',
        dest='quiet',
        default=False,
        action='store_true',
        help='work as quiet as possible (default: False)',
    )
    parser.add_argument(
        '-v',
        '--verbose',
        dest='verbose',
        default=False,
        action='store_true',
        help='work logging more information along the way (default: False)',
    )
    parser.add_argument(
        '-d',
        '--debug',
        dest='debug',
        default=False,
        action='store_true',
        help='provide debug level information (default: False)',
    )
    parser.add_argument(
        '-R',
        '--report-environment',
        dest='report',
        default=False,
        action='store_true',
        help='report the runtime environment in JSON format (default: False)',
    )
    parser.add_argument(
        '-V',
        '--version-of-lib',
        dest='package_version',
        default=False,
        action='store_true',
        help='show the library / package version and exit (default: False)',
    )
    parser.add_argument(
        '-r',
        '--version-ranges',
        dest='version_ranges',
        default='',
        type=str,
        help="version ranges as valid vers string (default: '')",
    )
    parser.add_argument(
        dest='versions',
        nargs='*',
        default='',
        type=str,
        help="version(s) to test against version ranges for inclusion (default: '')",
    )
    if not argv:
        parser.print_help()
        return 0

    options = parser.parse_args(argv)

    if options.package_version:
        print(VERSION)
        return 0

    if options.report:
        print(env.report(options, format='json'))
        return 0

    if options.verbose and options.quiet:
        parser.error('you cannot be quiet and verbose at the same time')

    if DEBUG:
        options.debug = True  # pragma: no cover
    if options.debug and options.quiet:
        parser.error('you cannot be quiet and debug at the same time')

    return options


def main(argv: Union[list[str], None] = None) -> int:
    """Delegate processing to functional module.

    Examples:

    >>> main(['-qr', 'vers:pypi/  42||'])
    vers:pypi/42
    0
    """
    argv = sys.argv[1:] if argv is None else argv
    options = parse_request(argv)
    if isinstance(options, int):
        return 0
    if options.quiet:
        log.setLevel(logging.CRITICAL)
    elif options.debug:
        log.setLevel(logging.DEBUG)

    return api.main(options)
