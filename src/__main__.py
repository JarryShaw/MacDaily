# -*- coding: utf-8 -*-

import argparse
import datetime
import importlib
import os
import pathlib
import sys

from macdaily.daily_archive import archive_ as archive
from macdaily.daily_bundle import bundle
from macdaily.daily_config import config, launch, parse
from macdaily.daily_dependency import dependency
from macdaily.daily_logging import logging
from macdaily.daily_postinstall import postinstall_ as postinstall
from macdaily.daily_reinstall import reinstall
from macdaily.daily_uninstall import uninstall
from macdaily.daily_update import update
from macdaily.daily_utility import UnsupportedOS, beholder, bold, reset

# change working directory
os.chdir(os.path.dirname(__file__))

# version string
__version__ = '2018.09.23'

# today
today = datetime.datetime.today()

# available commands
COMMANDS = '''\
MacDaily commands & corresponding subsidiaries:
    update, up, upgrade             apm, brew, cask, gem, mas, npm, pip, system
    uninstall, remove, rm, r, un    brew, cask, pip
    reinstall, re                   brew, cask
    postinstall, post               brew
    dependency, deps, dp            brew, pip
    logging, log                    apm, appstore, brew, cask, dotapp, gem, macapp, npm, pip
    bundle                          dump, load
    launch, init
    config, cfg
    archive
'''


def get_parser():
    parser = argparse.ArgumentParser(prog='MacDaily',
                                     description='Package Day-Care Manager',
                                     usage='macdaily [-h] command')
    parser.add_argument('-V', '--version', action='version', version=__version__)

    group = parser.add_argument_group('Commands',
                                      'MacDaily provides a friendly CLI workflow for the '
                                      'administrator of macOS to manipulate packages ')
    group.add_argument('command', help=argparse.SUPPRESS)

    return parser


def help_(argv, parser):
    if argv == []:
        parser.print_help()
        exit(1)

    def module(name):
        return importlib.import_module('macdaily.daily_{}'.format(name))

    command = argv[1].lower()
    if command in ('update', 'up', 'upgrade',):
        module('update').get_parser().print_help()
    elif command in ('uninstall', 'remove', 'rm', 'r', 'un',):
        module('uninstall').get_parser().print_help()
    elif command in ('reinstall', 're',):
        module('reinstall').get_parser().print_help()
    elif command in ('postinstall', 'post', 'ps',):
        module('postinstall').get_parser().print_help()
    elif command in ('dependency', 'deps', 'dp',):
        module('dependency').get_parser().print_help()
    elif command in ('logging', 'log',):
        module('logging').get_parser().print_help()
    elif command in ('launch', 'init',):
        print('macdaily: {}launch{}: launch new scheduled daemons'.format(bold, reset))
    elif command in ('config', 'cfg',):
        print('macdaily: {}config{}: manage your own preferences'.format(bold, reset))
    elif command in ('archive',):
        print('macdaily: {}archive{}: re-storing ancient logs'.format(bold, reset))
    else:
        print(COMMANDS)
        exit(1)


@beholder
def main():
    cfgdct = parse()
    parser = get_parser()
    mdargs = parser.parse_args(sys.argv[1:2])
    logdate = datetime.date.strftime(today, r'%y%m%d')
    logtime = datetime.date.strftime(today, r'%H%M%S')

    argv = sys.argv[2:]
    command = mdargs.command.lower()
    if command in ('update', 'up', 'upgrade',):
        update(argv, cfgdct, logdate, logtime, today)
    elif command in ('uninstall', 'remove', 'rm', 'r', 'un',):
        uninstall(argv, cfgdct, logdate, logtime, today)
    elif command in ('reinstall', 're',):
        reinstall(argv, cfgdct, logdate, logtime, today)
    elif command in ('postinstall', 'post', 'ps',):
        postinstall(argv, cfgdct, logdate, logtime, today)
    elif command in ('dependency', 'deps', 'dp',):
        dependency(argv, cfgdct, logdate, logtime, today)
    elif command in ('logging', 'log',):
        logging(argv, cfgdct, logdate, logtime, today)
    elif command in ('launch', 'init',):
        launch(cfgdct)
    elif command in ('archive',):
        archive(cfgdct, logdate, today)
    elif command in ('bundle',):
        bundle(argv, cfgdct, logdate, logtime, today)
    elif command in ('config', 'cfg',):
        config()
    elif command in ('help',):
        help_(argv, parser)
    elif command in ('commands',):
        print(COMMANDS)
    else:
        parser.print_help()
        exit(1)


if __name__ == '__main__':
    sys.tracebacklimit = 0
    sys.exit(main())
