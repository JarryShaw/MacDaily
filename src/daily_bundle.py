# -*- coding: utf-8 -*-


import argparse
import getpass
import os
import subprocess


# version string
__version__ = '2018.08.29'


# root path
ROOT = os.path.dirname(os.path.abspath(__file__))


# user name
USER = getpass.getuser()


def get_parser():
    parser = argparse.ArgumentParser(prog='bundle', description=(
                    'Automatic Package Bundling Manager'
                ), usage=(
                    'macdaily bundle [-hV] [-v]'
                ))
    parser.add_argument('-V', '--version', action='version', version=__version__)
    parser.add_argument('command', choices=['load', 'dump'], help=(
                            'dump or load a Macfile to keep track to all packages'
                        ))
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help=(
                            'run in verbose mode, with detailed output information'
                        ))

    return parser


def main(argv, config, *, logdate, logtime, today):
    parser = get_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return

    if args.command in ('load'):
        subprocess.run(['sudo', '--user', USER, '--set-home', 'bash', os.path.join(ROOT, 'libbundle/load.sh')])
    elif args.command in ('dump'):
        subprocess.run(['sudo', '--user', USER, '--set-home', 'bash', os.path.join(ROOT, 'libbundle/dump.sh'), str(args.verbose).lower()])
    else:
        parser.print_help()
