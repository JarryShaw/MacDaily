# -*- coding: utf-8 -*-

import argparse
import base64
import contextlib
import datetime
import os
import pwd
import shutil
import subprocess
import sys
import tempfile

from macdaily.daily_config import parse
from macdaily.daily_utility import (aftermath, archive, beholder, blue, bold,
                                    green, length, make_path, make_pipe,
                                    program, python, red, reset, under)
from macdaily.libdependency import *

# version string
__version__ = '2018.09.23'

# display mode names
NAME = dict(
    pip='Python',
    brew='Homebrew',
)

# mode actions
MODE = dict(
    all=lambda *args, **kwargs: dependency_all(*args, **kwargs),
    pip=lambda *args, **kwargs: dependency_pip(*args, **kwargs),
    brew=lambda *args, **kwargs: dependency_brew(*args, **kwargs),
)


def get_parser():
    parser = argparse.ArgumentParser(prog='dependency',
                                     description='Trivial Package Dependency Manager',
                                     usage='macdaily dependency [-hV] [-t] [-a] [--[no-]MODE] MODE ...',
                                     epilog='aliases: dependency, deps, dp')
    parser.add_argument('-V', '--version', action='version', version=__version__)
    parser.add_argument('-a', '--all', action='append_const', const='all', dest='mode',
                        help='show dependencies of all packages installed through pip and Homebrew')

    parser.add_argument('--pip', action='append_const', const='pip', dest='mode', help=argparse.SUPPRESS)
    parser.add_argument('--brew', action='append_const', const='brew', dest='mode', help=argparse.SUPPRESS)

    parser.add_argument('--no-pip', action='store_true', default=False, help=argparse.SUPPRESS)
    parser.add_argument('--no-brew', action='store_true', default=False, help=argparse.SUPPRESS)

    subparser = parser.add_subparsers(title='mode selection', metavar='MODE', dest='mode',
                                      help=('show dependencies of packages installed through a specified method, '
                                            'e.g.: pip or brew'))

    parser_pip = subparser.add_parser('pip', description='Show Dependencies of Python Packages',
                                      usage='macdaily dependency pip [-h] [-qv] [-bcsy] [-V VER] [-a] [-p PKG]')
    parser_pip.add_argument('-a', '--all', action='store_true', default=True, dest='all',
                            help='show dependencies of all packages installed through pip')
    parser_pip.add_argument('-v', '--python_version', action='store', metavar='VER', dest='version', type=int,
                            choices=[0, 1, 2, 20, 21, 22, 23, 24, 25, 26, 27, 3, 30, 31, 32, 33, 34, 35, 36, 37],
                            default=0, help='indicate which version of pip will be updated')
    parser_pip.add_argument('-s', '--system', action='store_true', default=False, dest='system',
                            help=('show dependencies of pip packages on system level, '
                                  'i.e. python installed through official installer'))
    parser_pip.add_argument('-b', '--brew', action='store_true', default=False, dest='brew',
                            help=('show dependencies of pip packages on Cellar level, '
                                  'i.e. python installed through Homebrew'))
    parser_pip.add_argument('-c', '--cpython', action='store_true', default=False, dest='cpython',
                            help='show dependencies of pip packages on CPython environment')
    parser_pip.add_argument('-y', '--pypy', action='store_true', default=False, dest='pypy',
                            help='show dependencies of pip packages on PyPy environment')
    parser_pip.add_argument('-p', '--package', metavar='PKG', action='append', dest='package',
                            help='name of packages to be shown, default is all')
    parser_pip.add_argument('-t', '--tree', action='store_true', default=False,
                            help='show dependencies as a tree. This feature requests `pipdeptree`')
    parser_pip.add_argument('--show-log', action='store_true', default=False,
                            help='open log in Console upon completion of command')

    parser_brew = subparser.add_parser('brew', description='Show Dependencies of Homebrew Packages',
                                       usage='macdaily dependency brew [-h] [-t] [-a] [-p PKG]')
    parser_brew.add_argument('-a', '--all', action='store_true', default=True, dest='all',
                             help='show dependencies of all packages installed through Homebrew')
    parser_brew.add_argument('-p', '--package', metavar='PKG', action='append', dest='package',
                             help='name of packages to be shown, default is all')
    parser_brew.add_argument('-t', '--tree', action='store_true', default=False,
                             help='show dependencies as a tree')
    parser_brew.add_argument('--show-log', action='store_true', default=False,
                             help='open log in Console upon completion of command')

    parser.add_argument('-t', '--tree', action='store_true', default=False,
                        help='show dependencies as a tree. This feature may request `pipdeptree`')
    parser.add_argument('--show-log', action='store_true', default=False,
                        help='open log in Console upon completion of command')

    return parser


def dependency(argv, config, logdate, logtime, today):
    parser = get_parser()
    args = parser.parse_args(argv)

    if args.mode is None:
        parser.print_help()
        exit(1)

    tmppath, logpath, arcpath, tarpath = make_path(config, mode='dependency', logdate=logdate)
    tmpfile = tempfile.NamedTemporaryFile(dir=tmppath, prefix='dependency-', suffix='.log')
    logname = os.path.join(logpath, logdate, '{}.log'.format(logtime))
    tmpname = tmpfile.name

    PIPE = make_pipe(config)
    USER = config['Account']['username']
    BASH = config['Environment'].getint('bash-timeout', fallback=1000)

    with open(logname, 'a') as logfile:
        logfile.write(datetime.date.strftime(today, ' %+ ').center(80, '—'))
        logfile.write('\n\nCMD: {} {}'.format(python, program))
        logfile.write("\n\n{}\n\n".format('-*- Arguments -*-'.center(80, ' ')))
        for key, value in args.__dict__.items():
            logfile.write('ARG: {} = {}\n'.format(key, value))

    if pwd.getpwuid(os.stat(logname).st_uid) != USER:
        subprocess.run(['sudo', 'chown', '-R', USER, config['Path']['tmpdir'], config['Path']['logdir']],
                       stdin=PIPE.stdout, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    for mode in config['Mode'].keys():
        if not config['Mode'].getboolean(mode, fallback=False):
            setattr(args, 'no_{}'.format(mode), True)
    if isinstance(args.mode, str):
        args.mode = [args.mode]
    if 'all' in args.mode:
        args.mode = ['all']

    for mode in set(args.mode):
        dependency = MODE.get(mode)
        log = aftermath(logfile=logname, tmpfile=tmpname, command='update')(
                dependency)(args, file=logname, temp=tmpname, bash_timeout=BASH)

    mode = '-*- Dependency Logs -*-'.center(80, ' ')
    with open(logname, 'a') as logfile:
        logfile.write('\n\n{}\n\n'.format(mode))
        if log != dict():
            for mode in log:
                name = NAME.get(mode)
                if log[mode] and all(log[mode]):
                    pkgs = ', '.format().join(log[mode])
                    logfile.write('LOG: showed dependencies of following {} packages: {}\n'.format(name, pkgs))
                else:
                    logfile.write('LOG: no dependencies showed in {} packages\n'.format(name))

            filelist = archive(config, logpath, arcpath, tarpath, logdate, today)
            if filelist:
                files = ', '.join(filelist)
                logfile.write('LOG: archived following old logs: {}\n'.format(files))
            else:
                logfile.write('LOG: no ancient logs archived\n')
        else:
            logfile.write('LOG: no dependencies showed\n')

    with contextlib.suppress(OSError):
        tmpfile.close()
    if args.show_log:
        subprocess.run(['open', '-a', 'Console', logname], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


@beholder
def main():
    config = parse()
    argv = sys.argv[1:]
    today = datetime.datetime.today()
    logdate = datetime.date.strftime(today, r'%y%m%d')
    logtime = datetime.date.strftime(today, r'%H%M%S')
    dependency(argv, config, logdate, logtime, today)


if __name__ == '__main__':
    sys.tracebacklimit = 0
    sys.exit(main())
