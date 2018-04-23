# -*- coding: utf-8 -*-


import argparse
import datetime
import os
import platform
import sys

from jsdaily.daily_up import main as update
from jsdaily.daily_un import main as uninstall
from jsdaily.daily_re import main as reinstall
from jsdaily.daily_ps import main as postinstall
from jsdaily.daily_dp import main as dependency
from jsdaily.daily_lg import main as logging


__all__ = ['main']


# change working directory
os.chdir(os.path.dirname(__file__))


# version string
__version__ = '1.0.3'


# today
today = datetime.datetime.today()


# error handling class
class UnsupoortedOS(RuntimeError):
    def __init__(self, message, *args, **kwargs):
        sys.tracebacklimit = 0
        super().__init__(message, *args, **kwargs)


def get_parser():
    parser = argparse.ArgumentParser(prog='jsupdate', description=(
                    'Package Day Care Manager'
                ), usage=(
                    'jsdaily [-h] command '
                ))
    parser.add_argument('-V', '--version', action='version', version=__version__)

    group = parser.add_argument_group(
                    'Commands',
                    'jsdaily provides a friendly CLI workflow for the '
                    'administrator of macOS to manupulate packages '
                )
    group.add_argument('command', choices=[
                            'update', 'up', 'upgrade',                  # jsupdate
                            'uninstall', 'remove', 'rm', 'r', 'un',     # jsuninstall
                            'reinstall', 're',                          # jsreinstall
                            'postinstall', 'post', 'ps',                # jspostinstall
                            'dependency', 'deps', 'dp'                  # jsdependency
                            'logging', 'log', 'lg'                      # jslogging
                        ], help=argparse.SUPPRESS)

    return parser


def main():
    if platform.system() != 'Darwin':
        raise UnsupoortedOS('jsdaily: script runs only on macOS')

    parser = get_parser()
    args = parser.parse_args(sys.argv[1:2])

    argv = sys.argv[2:]
    if args.command in ('update', 'up', 'upgrade'):
        update(argv)
    elif args.command in ('uninstall', 'remove', 'rm', 'r', 'un'):
        uninstall(argv)
    elif args.command in ('reinstall', 're'):
        reinstall(argv)
    elif args.command in ('postinstall', 'post', 'ps'):
        postinstall(argv)
    elif args.command in ('dependency', 'deps', 'dp'):
        dependency(argv)
    elif args.command in ('logging', 'log', 'lg'):
        logging(argv)
    else:
        parser.print_help()


if __name__ == '__main__':
    sys.exit(main())
