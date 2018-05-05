# -*- coding: utf-8 -*-


import argparse
import datetime
import os
import pathlib
import platform
import re
import sys

from jsdaily.daily_rc import *
from jsdaily.daily_ng import beholder
from jsdaily.daily_up import main as update
from jsdaily.daily_un import main as uninstall
from jsdaily.daily_re import main as reinstall
from jsdaily.daily_ps import main as postinstall
from jsdaily.daily_dp import main as dependency
from jsdaily.daily_lg import main as logging
from jsdaily.daily_mv import main as archive


__all__ = ['main']


# change working directory
os.chdir(os.path.dirname(__file__))


# version string
__version__ = '1.1.1'


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
                    'administrator of macOS to manipulate packages '
                )
    group.add_argument('command', choices=[
                            'update', 'up', 'U', 'upgrade',                 # jsupdate
                            'uninstall', 'remove', 'rm', 'r', 'un',         # jsuninstall
                            'reinstall', 're', 'R',                         # jsreinstall
                            'postinstall', 'post', 'ps', 'p',               # jspostinstall
                            'dependency', 'deps', 'dep', 'dp', 'de', 'd',   # jsdependency
                            'logging', 'log', 'lg', 'l',                    # jslogging
                            'launch',                                       # launch
                            'config', 'cfg',                                # config
                            'archive', 'gz', 'tar',                         # archive
                        ], help=argparse.SUPPRESS)

    return parser


@beholder
def main():
    if platform.system() != 'Darwin':
        raise UnsupoortedOS('jsdaily: script runs only on macOS')

    cfgdct = parse()
    parser = get_parser()
    args = parser.parse_args(sys.argv[1:2])
    logdate = datetime.date.strftime(today, '%y%m%d')
    logtime = datetime.date.strftime(today, '%H%M%S')

    argv = sys.argv[2:]
    if args.command in ('update', 'up', 'U', 'upgrade'):
        update(argv, cfgdct, logdate=logdate, logtime=logtime, today=today)
    elif args.command in ('uninstall', 'remove', 'rm', 'r', 'un'):
        uninstall(argv, cfgdct, logdate=logdate, logtime=logtime, today=today)
    elif args.command in ('reinstall', 're', 'R'):
        reinstall(argv, cfgdct, logdate=logdate, logtime=logtime, today=today)
    elif args.command in ('postinstall', 'post', 'ps', 'p'):
        postinstall(argv, cfgdct, logdate=logdate, logtime=logtime, today=today)
    elif args.command in ('dependency', 'deps', 'dep', 'dp', 'de', 'd'):
        dependency(argv, cfgdct, logdate=logdate, logtime=logtime, today=today)
    elif args.command in ('logging', 'log', 'lg', 'l'):
        logging(argv, cfgdct, logdate=logdate, logtime=logtime, today=today)
    elif args.command in ('launch'):
        launch(cfgdct)
    elif args.command in ('config', 'cfg'):
        config()
    elif args.command in ('archive', 'gz', 'tar'):
        archive(cfgdct, logdate=logdate, today=today)
    else:
        parser.print_help()


if __name__ == '__main__':
    sys.exit(main())
