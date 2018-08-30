# -*- coding: utf-8 -*-


import argparse
import datetime
import getpass
import os
import pwd
import subprocess
import sys

from macdaily.daily_utility import *
from macdaily.libdependency import *


# version string
__version__ = '2018.08.29'


# display mode names
NAME = dict(
    pip = 'Python',
    brew = 'Homebrew',
)


# mode actions
MODE = dict(
    all = lambda *args, **kwargs: dependency_all(*args, **kwargs),
    pip = lambda *args, **kwargs: dependency_pip(*args, **kwargs),
    brew = lambda *args, **kwargs: dependency_brew(*args, **kwargs),
)


# terminal commands
python = sys.executable         # Python version
program = ' '.join(sys.argv)    # arguments


# terminal display
reset  = '\033[0m'      # reset
bold   = '\033[1m'      # bold
under  = '\033[4m'      # underline
red    = '\033[91m'     # bright red foreground
green  = '\033[92m'     # bright green foreground
blue   = '\033[96m'     # bright blue foreground


# user name
USER = getpass.getuser()


def get_parser():
    parser = argparse.ArgumentParser(prog='dependency', description=(
                    'Trivial Package Dependency Manager'
                ), usage=(
                    'macdaily dependency [-hV] [-t] [-a] [--[no-]MODE] MODE ... '
                ), epilog=(
                    'aliases: dependency, deps, dep, dp, de, d'
                ))
    parser.add_argument('-V', '--version', action='version', version=__version__)
    parser.add_argument('-a', '--all', action='append_const', const='all',
                        dest='mode', help=(
                            'show dependencies of all packages installed '
                            'through pip and Homebrew'
                        ))

    parser.add_argument('--pip', action='append_const', const='pip', dest='mode', help=argparse.SUPPRESS)
    parser.add_argument('--brew', action='append_const', const='brew', dest='mode', help=argparse.SUPPRESS)

    parser.add_argument('--no-pip', action='store_true', default=False, help=argparse.SUPPRESS)
    parser.add_argument('--no-brew', action='store_true', default=False, help=argparse.SUPPRESS)

    subparser = parser.add_subparsers(title='mode selection', metavar='MODE',
                        dest='mode', help=(
                            'show dependencies of packages installed through '
                            'a specified method, e.g.: pip or brew'
                        ))

    parser_pip = subparser.add_parser('pip', description=(
                            'Show Dependencies of Python Packages'
                        ), usage=(
                            'macdaily dependency pip [-h] [-qv] [-bcsy] [-V VER] [-a] [-p PKG]'
                        ))
    parser_pip.add_argument('-a', '--all', action='store_true', default=True,
                        dest='all', help=(
                            'show dependencies of all packages installed through pip'
                        ))
    parser_pip.add_argument('-v', '--python_version', action='store', metavar='VER',
                        choices=[
                            1, 2, 20, 21, 22, 23, 24, 25, 26, 27,
                            0, 3, 30, 31, 32, 33, 34, 35, 36, 37,
                        ], dest='version', type=int, default=0, help=(
                            'indicate which version of pip will be updated'
                        ))
    parser_pip.add_argument('-s', '--system', action='store_true', default=False,
                        dest='system', help=(
                            'show dependencies of pip packages on system level, i.e. python '
                            'installed through official installer'
                        ))
    parser_pip.add_argument('-b', '--brew', action='store_true', default=False,
                        dest='brew', help=(
                            'show dependencies of pip packages on Cellar level, i.e. python '
                            'installed through Homebrew'
                        ))
    parser_pip.add_argument('-c', '--cpython', action='store_true', default=False,
                        dest='cpython', help=(
                            'show dependencies of pip packages on CPython environment'
                        ))
    parser_pip.add_argument('-y', '--pypy', action='store_true', default=False,
                        dest='pypy', help=(
                            'show dependencies of pip packages on PyPy environment'
                        ))
    parser_pip.add_argument('-p', '--package', metavar='PKG', action='append',
                        dest='package', help=(
                            'name of packages to be shown, default is all'
                        ))
    parser_pip.add_argument('-t', '--tree', action='store_true', default=False,
                        help=(
                            'show dependencies as a tree. This feature requests '
                            '`pipdeptree`'
                        ))
    parser_pip.add_argument('--show-log', action='store_true', default=False,
                        help=(
                            'open log in Console upon completion of command'
                        ))

    parser_brew = subparser.add_parser('brew', description=(
                            'Show Dependencies of Homebrew Packages'
                        ), usage=(
                            'macdaily dependency brew [-h] [-t] [-a] [-p PKG]'
                        ))
    parser_brew.add_argument('-a', '--all', action='store_true', default=True,
                        dest='all', help=(
                            'show dependencies of all packages installed through Homebrew'
                        ))
    parser_brew.add_argument('-p', '--package', metavar='PKG', action='append',
                        dest='package', help=(
                            'name of packages to be shown, default is all'
                        ))
    parser_brew.add_argument('-t', '--tree', action='store_true', default=False,
                        help=(
                            'show dependencies as a tree'
                        ))
    parser_brew.add_argument('--show-log', action='store_true', default=False,
                        help=(
                            'open log in Console upon completion of command'
                        ))

    parser.add_argument('-t', '--tree', action='store_true', default=False,
                        help=(
                            'show dependencies as a tree. This feature may request '
                            '`pipdeptree`'
                        ))
    parser.add_argument('--show-log', action='store_true', default=False,
                        help=(
                            'open log in Console upon completion of command'
                        ))

    return parser


def main(argv, config, *, logdate, logtime, today):
    parser = get_parser()
    args = parser.parse_args(argv)

    if args.mode is None:
        parser.print_help()
        return

    tmppath, logpath, arcpath, tarpath = make_path(config, mode='dependency', logdate=logdate)
    logname = f'{logpath}/{logdate}/{logtime}.log'
    tmpname = f'{tmppath}/dependency.log'

    mode = '-*- Arguments -*-'.center(80, ' ')
    with open(logname, 'a') as logfile:
        logfile.write(datetime.date.strftime(today, ' %+ ').center(80, '—'))
        logfile.write(f'\n\nCMD: {python} {program}')
        logfile.write(f'\n\n{mode}\n\n')
        for key, value in args.__dict__.items():
            logfile.write(f'ARG: {key} = {value}\n')

    if pwd.getpwuid(os.stat(logname).st_uid) != USER:
        subprocess.run(
            ['sudo', '--user', 'root', '--set-home', 'chown', '-R', USER, config['Path']['tmpdir'], config['Path']['logdir']],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

    for mode in config['Mode'].keys():
        try:
            flag = not config['Mode'].getboolean(mode)
        except ValueError as error:
            sys.tracebacklimit = 0
            raise error from None
        if flag:
            args.__setattr__(f'no_{mode}', flag)
    if isinstance(args.mode, str):
        args.mode = [args.mode]
    if 'all' in args.mode:
        args.mode = ['all']

    for mode in set(args.mode):
        dependency = MODE.get(mode)
        log = aftermath(logfile=logname, tmpfile=tmpname, command='update'
                )(dependency)(args, file=logname, temp=tmpname)

    if log == set():    return
    mode = '-*- Dependency Logs -*-'.center(80, ' ')
    with open(logname, 'a') as logfile:
        logfile.write(f'\n\n{mode}\n\n')

        for mode in log:
            name = NAME.get(mode)
            if name is None:    continue
            if log[mode] and all(log[mode]):
                pkgs = f', '.join(log[mode])
                logfile.write(f'LOG: showed dependencies of following {name} packages: {pkgs}\n')
            else:
                logfile.write(f'LOG: no dependencies showed in {name} packages\n')

        filelist = archive(config, logpath=logpath, arcpath=arcpath, tarpath=tarpath, logdate=logdate, today=today)
        if filelist:
            files = ', '.join(filelist)
            logfile.write(f'LOG: archived following old logs: {files}\n')

    if args.show_log:
        subprocess.run(['open', '-a', 'Console', logname], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
