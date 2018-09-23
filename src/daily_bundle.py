# -*- coding: utf-8 -*-

import argparse
import datetime
import os
import subprocess
import sys

from macdaily.daily_config import parse
from macdaily.daily_utility import beholder

# version string
__version__ = '2018.09.23'

# root path
ROOT = os.path.dirname(os.path.abspath(__file__))


def get_parser():
    parser = argparse.ArgumentParser(prog='bundle',
                                     description='Automatic Package Bundling Manager',
                                     usage='macdaily bundle [-hV] [-v]')
    parser.add_argument('-V', '--version', action='version', version=__version__)
    parser.add_argument('command', choices=['load', 'dump'],
                        help='dump or load a Macfile to keep track to all packages')
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help='run in verbose mode, with detailed output information')
    return parser


def bundle(argv, config, logdate, logtime, today):
    parser = get_parser()
    args = parser.parse_args(argv)

    bash_timeout = config['Environment'].getint('bash-timeout', fallback=1000) * 4
    if args.command in ('load'):
        subprocess.run(['bash', os.path.join(ROOT, 'libbundle/load.sh')],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=bash_timeout)
    elif args.command in ('dump'):
        subprocess.run(['bash', os.path.join(ROOT, 'libbundle/dump.sh'), str(args.verbose).lower()],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=bash_timeout)
    else:
        parser.print_help()
        exit(1)


@beholder
def main():
    config = parse()
    argv = sys.argv[1:]
    today = datetime.datetime.today()
    logdate = datetime.date.strftime(today, r'%y%m%d')
    logtime = datetime.date.strftime(today, r'%H%M%S')
    bundle(argv, config, logdate, logtime, today)


if __name__ == '__main__':
    sys.tracebacklimit = 0
    sys.exit(main())
