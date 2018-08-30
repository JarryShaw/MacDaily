# -*- coding: utf-8 -*-


import argparse
import base64
import datetime
import os
import pwd
import shlex
import subprocess
import sys

from macdaily.daily_utility import *
from macdaily.liblogging import *


# version string
__version__ = '2018.08.30'


# mode actions
MODE = dict(
    apm = lambda *args, **kwargs: logging_apm(*args, **kwargs),
    gem = lambda *args, **kwargs: logging_gem(*args, **kwargs),
    npm = lambda *args, **kwargs: logging_npm(*args, **kwargs),
    pip = lambda *args, **kwargs: logging_pip(*args, **kwargs),
    brew = lambda *args, **kwargs: logging_brew(*args, **kwargs),
    cask = lambda *args, **kwargs: logging_cask(*args, **kwargs),
    dotapp = lambda *args, **kwargs: logging_dotapp(*args, **kwargs),
    macapp = lambda *args, **kwargs: logging_macapp(*args, **kwargs),
    appstore = lambda *args, **kwargs: logging_appstore(*args, **kwargs),
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


def get_parser():
    parser = argparse.ArgumentParser(prog='logging', description=(
                    'Application & Package Logging Manager'
                ), usage=(
                    'macdaily logging [-hV] [-q] [-a] [-bcsy] [-v VER] [--[no-]MODE] [MODE [MODE ...]]'
                ), epilog=(
                    'aliases: logging, log, lg, l'
                ))
    parser.add_argument('-V', '--version', action='version', version=__version__)
    parser.add_argument('-a', '--all', action='store_true', dest='all', default=False,
                        help=(
                            'log applications and packages of all entries'
                        ))

    parser.add_argument('--apm', action='append_const', const='apm', dest='mode', help=argparse.SUPPRESS)
    parser.add_argument('--gem', action='append_const', const='gem', dest='mode', help=argparse.SUPPRESS)
    parser.add_argument('--pip', action='append_const', const='pip', dest='mode', help=argparse.SUPPRESS)
    parser.add_argument('--npm', action='append_const', const='npm', dest='mode', help=argparse.SUPPRESS)
    parser.add_argument('--brew', action='append_const', const='brew', dest='mode', help=argparse.SUPPRESS)
    parser.add_argument('--cask', action='append_const', const='cask', dest='mode', help=argparse.SUPPRESS)
    parser.add_argument('--dotapp', action='append_const', const='dotapp', dest='mode', help=argparse.SUPPRESS)
    parser.add_argument('--macapp', action='append_const', const='macapp', dest='mode', help=argparse.SUPPRESS)
    parser.add_argument('--appstore', action='append_const', const='appstore', dest='mode', help=argparse.SUPPRESS)

    parser.add_argument('--no-apm', action='store_true', default=False, help=argparse.SUPPRESS)
    parser.add_argument('--no-gem', action='store_true', default=False, help=argparse.SUPPRESS)
    parser.add_argument('--no-pip', action='store_true', default=False, help=argparse.SUPPRESS)
    parser.add_argument('--no-npm', action='store_true', default=False, help=argparse.SUPPRESS)
    parser.add_argument('--no-brew', action='store_true', default=False, help=argparse.SUPPRESS)
    parser.add_argument('--no-cask', action='store_true', default=False, help=argparse.SUPPRESS)
    parser.add_argument('--no-dotapp', action='store_true', default=False, help=argparse.SUPPRESS)
    parser.add_argument('--no-macapp', action='store_true', default=False, help=argparse.SUPPRESS)
    parser.add_argument('--no-appstore', action='store_true', default=False, help=argparse.SUPPRESS)

    parser.add_argument('mode', action='append', metavar='MODE', nargs='*',
                        choices=[
                            [], 'apm', 'gem', 'pip', 'npm', 'brew',
                            'cask', 'dotapp', 'macapp', 'appstore',
                        ], help=(
                            'name of logging mode, could be any from '
                            'followings, apm, gem, pip, npm, brew, cask, '
                            'dotapp, macapp, or appstore'
                        ))

    parser.add_argument('-v', '--python_version', action='store', metavar='VER',
                        choices=[
                            1, 2, 20, 21, 22, 23, 24, 25, 26, 27,
                            0, 3, 30, 31, 32, 33, 34, 35, 36, 37,
                        ], dest='version', type=int, default=0, help=(
                            'indicate which version of pip will be logged'
                        ))
    parser.add_argument('-s', '--system', action='store_true', default=False,
                        dest='system', help=(
                            'log pip packages on system level, i.e. python '
                            'installed through official installer'
                        ))
    parser.add_argument('-b', '--brewed', action='store_true', default=False,
                        dest='brew', help=(
                            'log pip packages on Cellar level, i.e. python '
                            'installed through Homebrew'
                        ))
    parser.add_argument('-c', '--cpython', action='store_true', default=False,
                        dest='cpython', help=(
                            'log pip packages on CPython environment'
                        ))
    parser.add_argument('-y', '--pypy', action='store_true', default=False,
                        dest='pypy', help=(
                            'log pip packages on PyPy environment'
                        ))
    parser.add_argument('-q', '--quiet', action='store_true', default=False,
                        help=(
                            'run in quiet mode, with no output information'
                        ))
    parser.add_argument('--show-log', action='store_true', default=False,
                        help=(
                            'open log in Console upon completion of command'
                        ))

    return parser


def main(argv, config, *, logdate, logtime, today):
    parser = get_parser()
    args = parser.parse_args(argv)

    modes = list()
    for mode in args.mode:
        if isinstance(mode, str):   modes.append(mode)
        else:                       modes += mode
    if args.all:
        for mode in {'apm', 'gem', 'pip', 'npm', 'brew', 'cask', 'dotapp', 'macapp', 'appstore'}:
            try:
                flag = config['Mode'].getboolean(mode)
            except ValueError as error:
                sys.tracebacklimit = 0
                raise error from None
            if flag and (not getattr(args, f'no_{mode}', False)):
                modes.append(mode)
    args.mode = set(modes) or None

    if args.mode is None:
        parser.print_help()
        return

    PIPE = make_pipe(config)
    USER = config['Account']['username']
    PASS = base64.b64encode(PIPE.stdout.readline().strip()).decode()

    arcflag = False
    for logmode in args.mode:
        tmppath, logpath, arcpath, tarpath = make_path(config, mode=f'logging/{logmode}', logdate=logdate)
        logname = f'{logpath}/{logdate}/{logtime}.log'

        with open(logname, 'a') as logfile:
            logfile.write(datetime.date.strftime(today, ' %+ ').center(80, '—'))
            logfile.write(f'\n\n\nCMD: {python} {program}\n\n\n')
            for key, value in args.__dict__.items():
                logfile.write(f'ARG: {key} = {value}\n')
            logfile.write('\n\n')

        if pwd.getpwuid(os.stat(logname).st_uid) != USER:
            subprocess.run(
                ['sudo', 'chown', '-R', USER, config['Path']['tmpdir'], config['Path']['logdir']],
                stdin=PIPE.stdout, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )

        try:
            logging = MODE.get(logmode)
            log = logging(args, file=shlex.quote(logname), password=PASS)
        except subprocess.TimeoutExpired as error:
            with open(logname, 'a') as logfile:
                logfile.write('\nERR: operation timeout\n')
            if not args.quiet:
                print(f'logging: {red}{logmode}{reset}: operation timeout')
        except BaseException as error:
            with open(logname, 'a') as logfile:
                logfile.write('\nWAR: procedure interrupted\n')
            if not args.quiet:
                print(f'logging: {red}{logmode}{reset}: procedure interrupted')
            sys.tracebacklimit = 0
            raise error from None

        with open(logname, 'a') as logfile:
            filelist = archive(config, logpath=logpath, arcpath=arcpath, tarpath=tarpath, logdate=logdate, today=today, mvflag=False)
            if filelist:
                arcflag = True
                files = ', '.join(filelist)
                logfile.write(f'LOG: archived following old logs: {files}\n')

        if args.show_log:
            subprocess.run(['open', '-a', 'Console', logname], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    storage(config, logdate=logdate, today=today)
    if arcflag and not args.quiet:
        arcdir = config['Path']['logdir'] + '/archive/logging'
        print(f'logging: {green}cleanup{reset}: ancient logs archived into {under}{arcdir}{reset}')


if __name__ == '__main__':
    from macdaily.daily_config import parse

    config = parse()
    today = datetime.datetime.today()
    argv = parser.parse_args(sys.argv[1:])
    logdate = datetime.date.strftime(today, '%y%m%d')
    logtime = datetime.date.strftime(today, '%H%M%S')
    sys.exit(main(argv, config, *, logdate=logdate, logtime=logtime, today=today))
