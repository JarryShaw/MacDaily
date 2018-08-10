# -*- coding: utf-8 -*-


import os
import subprocess


# version string
__version__ = '1.5.0'


# root path
ROOT = os.path.dirname(os.path.abspath(__file__))


def get_parser():
    parser = argparse.ArgumentParser(prog='bundle', description=(
                    'Automatic Package Bundling Manager'
                ), usage=(
                    'macdaily bundle [-hV] [-v]'
                ))
    parser.add_argument('-V', '--version', action='version', version=__version__)
    parser.add_argument('command', choices=['load', 'dump'], help=argparse.SUPPRESS)


def main(argv, config, *, logdate, logtime, today):
    parser = get_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return

    if command in ('load'):
        subprocess.run(['bash', os.path.join(ROOT, 'libbundle/load.sh')])
    elif command in ('dump'):
        subprocess.run(['bash', os.path.join(ROOT, 'libbundle/dump.sh')])
    else:
        parser.print_help()
