# -*- coding: utf-8 -*-


import argparse
import jsupdate
import jsuninstall
import jsreinstall
import jspostinstall
import jsdependency
import jslogging
import platform
import re
import sys


# version string
__version__ = '0.9.3'


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
                            'dependency', 'deps',                       # jsdependency
                            'logging', 'log',                           # jslogging
                        ], help=argparse.SUPPRESS)

    return parser


def main():
    if platform.system() != 'Darwin':
        raise UnsupoortedOS('update: script runs only on macOS')

    parser = get_parser()
    args = parser.parse_args([sys.argv[1]])

    argv = sys.argv[2:]
    if args.command in ('update', 'up', 'upgrade'):
        jsupdate.main(argv)
    elif args.command in ('uninstall', 'remove', 'rm', 'r', 'un'):
        jsuninstall.main(argv)
    elif args.command in ('reinstall', 're'):
        jsreinstall.main(argv)
    elif args.command in ('postinstall', 'post', 'ps'):
        jspostinstall.main(argv)
    elif args.command in ('dependency', 'deps'):
        jsdependency.main(argv)
    elif args.command in ('logging', 'log'):
        jslogging.main(argv)
    else:
        parser.print_help()


if __name__ == '__main__':
    sys.exit(main())
