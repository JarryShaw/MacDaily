# -*- coding: utf-8 -*-


import argparse
import datetime
import os
import pathlib
import platform
import re
import sys

from jsdaily.daily_archive import main as archive
from jsdaily.daily_config import *
from jsdaily.daily_dependency import main as dependency
from jsdaily.daily_logging import main as logging
from jsdaily.daily_postinstall import main as postinstall
from jsdaily.daily_reinstall import main as reinstall
from jsdaily.daily_uninstall import main as uninstall
from jsdaily.daily_update import main as update
from jsdaily.daily_utility import beholder


# change working directory
os.chdir(os.path.dirname(__file__))


# version string
__version__ = '1.3.4'


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
                            'update', 'up', 'upgrade',                      # jsupdate
                            'uninstall', 'remove', 'rm', 'r', 'un',         # jsuninstall
                            'reinstall', 're',                              # jsreinstall
                            'postinstall', 'post', 'ps',                    # jspostinstall
                            'dependency', 'deps', 'dp',                     # jsdependency
                            'logging', 'log',                               # jslogging
                            'launch', 'init',                               # launch
                            'config', 'cfg',                                # config
                            'archive',                                      # archive
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
    command = args.command.lower()
    if command in ('update', 'up', 'upgrade',):
        update(argv, cfgdct, logdate=logdate, logtime=logtime, today=today)
    elif command in ('uninstall', 'remove', 'rm', 'r', 'un',):
        uninstall(argv, cfgdct, logdate=logdate, logtime=logtime, today=today)
    elif command in ('reinstall', 're',):
        reinstall(argv, cfgdct, logdate=logdate, logtime=logtime, today=today)
    elif command in ('postinstall', 'post', 'ps',):
        postinstall(argv, cfgdct, logdate=logdate, logtime=logtime, today=today)
    elif command in ('dependency', 'deps', 'dp',):
        dependency(argv, cfgdct, logdate=logdate, logtime=logtime, today=today)
    elif command in ('logging', 'log',):
        logging(argv, cfgdct, logdate=logdate, logtime=logtime, today=today)
    elif command in ('launch', 'init',):
        launch(cfgdct)
    elif command in ('config', 'cfg',):
        config()
    elif command in ('archive',):
        archive(cfgdct, logdate=logdate, today=today)
    else:
        parser.print_help()


if __name__ == '__main__':
    sys.exit(main())
