# -*- coding: utf-8 -*-


import argparse
import configparser
import datetime
import os
import pathlib
import platform
import re
import sys

from jsdaily.daily_up import main as update
from jsdaily.daily_un import main as uninstall
from jsdaily.daily_re import main as reinstall
from jsdaily.daily_ps import main as postinstall
from jsdaily.daily_dp import main as dependency
from jsdaily.daily_lg import main as logging


__all__ = ['main']


# change working directory
# os.chdir(os.path.dirname(__file__))


# version string
__version__ = '1.1.0'


# today
today = datetime.datetime.today()


# default config
CONFIG = """\
[Path]
# In this section, paths for log files are specified.
# Please, under any circumstances, make sure they are valid.
logdir = /Library/Logs/Scripts      ; path where logs will be stored
tmpdir = /tmp/log                   ; path where temporary runtime logs go
dskdir = /Volumes/Your Disk         ; path where your hard disk lies
arcdir = ${dskdir}/Developers       ; path where ancient logs archive

[Mode]
# In this section, flags for modes are configured.
# If you would like to disable the mode, set it to "false".
apm      = true     ; Atom packages
gem      = true     ; Ruby gems
npm      = true     ; Node.js modules
pip      = true     ; Python packages
brew     = true     ; Homebrew Cellars
cask     = true     ; Caskroom Casks
dotapp   = true     ; Applications (*.app)
macapp   = true     ; applications in /Application folder
cleanup  = true     ; cleanup caches
appstore = true     ; Mac App Store applications
"""


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
                        ], help=argparse.SUPPRESS)

    return parser


def main():
    if platform.system() != 'Darwin':
        raise UnsupoortedOS('jsdaily: script runs only on macOS')

    parser = get_parser()
    args = parser.parse_args(sys.argv[1:2])

    config = configparser.ConfigParser(
        inline_comment_prefixes=(';',),
        interpolation=configparser.ExtendedInterpolation())
    config.SECTCRE = re.compile(r"\[ *(?P<header>[^]]+?) *\]")
    config.read_string(CONFIG)

    rcpath = pathlib.Path('~/.dailyrc').expanduser()
    if rcpath.exists() and rcpath.is_file():
        try:
            with open(rcpath, 'r') as config_file:
                config.read_file(config_file)
        except configparser.Error as error:
            sys.tracebacklimit = 0
            raise error from None
    else:
        try:
            with open(rcpath, 'w') as config_file:
                config_file.write(CONFIG)
        except BaseException as error:
            sys.tracebacklimit = 0
            raise error from None

    argv = sys.argv[2:]
    if args.command in ('update', 'up', 'U', 'upgrade'):
        update(argv, config)
    elif args.command in ('uninstall', 'remove', 'rm', 'r', 'un'):
        uninstall(argv, config)
    elif args.command in ('reinstall', 're', 'R'):
        reinstall(argv, config)
    elif args.command in ('postinstall', 'post', 'ps', 'p'):
        postinstall(argv, config)
    elif args.command in ('dependency', 'deps', 'dep', 'dp', 'de', 'd'):
        dependency(argv, config)
    elif args.command in ('logging', 'log', 'lg', 'l'):
        logging(argv, config)
    else:
        parser.print_help()


if __name__ == '__main__':
    sys.exit(main())
