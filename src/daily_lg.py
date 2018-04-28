# -*- coding: utf-8 -*-


import argparse
import calendar
import datetime
import os
import pathlib
import platform
import shlex
import shutil
import subprocess
import sys
import tarfile
import zipfile

from jsdaily.liblogging import *


# version string
__version__ = '1.1.0'


# today
today = datetime.datetime.today()


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
python = sys.prefix             # Python version
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
                    'jsdaily logging [-hV] [-q] [-a] [-bcsy] [-v VER] [--[no-]MODE] [MODE [MODE ...]]'
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

    return parser


def main(argv, config):
    logmode = None
    try:
        parser = get_parser()
        args = parser.parse_args(argv)

        modes = list()
        for mode in args.mode:
            if isinstance(mode, str):   modeds.append(mode)
            else:                       modes += mode
        if args.all:
            modes += ['apm', 'gem', 'pip', 'npm', 'brew', 'cask', 'dotapp', 'macapp', 'appstore']
        args.mode = set(modes) or None

        if args.mode is None:
            parser.print_help()
            return

        tmpdir = config['Path']['tmpdir']
        pathlib.Path(tmpdir).mkdir(parents=True, exist_ok=True)

        dskpath = pathlib.Path(config['Path']['dskdir'])
        if dskpath.exists() and dskpath.is_dir():
            pathlib.Path(config['Path']['arcdir']).mkdir(parents=True, exist_ok=True)

        logdate = datetime.date.strftime(today, '%y%m%d')
        logtime = datetime.date.strftime(today, '%H%M%S')

        arcflag = False
        for logmode in args.mode:
            flag = not config['Mode'].getboolean(logmode)
            if flag or args.__getattribute__(f'no_{logmode}'):
                continue

            logdir = config['Path']['logdir'] + f'/logging/{logmode}'
            arcdir = config['Path']['logdir'] + f'/archive/logging/{logmode}'
            tardir = config['Path']['logdir'] + f'/tarfile/logging/{logmode}'

            logname = f'{logdir}/{logdate}/{logtime}.log'

            pathlib.Path(arcdir).mkdir(parents=True, exist_ok=True)
            pathlib.Path(tardir).mkdir(parents=True, exist_ok=True)
            pathlib.Path(f'{logdir}/{logdate}').mkdir(parents=True, exist_ok=True)

            with open(logname, 'a') as logfile:
                logfile.write(datetime.date.strftime(today, ' %+ ').center(80, '—'))
                logfile.write(f'\n\n\nCMD: {python} {program}\n\n\n')
                for key, value in args.__dict__.items():
                    logfile.write(f'ARG: {key} = {value}\n')
                logfile.write('\n\n')

            logging = MODE.get(logmode)
            log = logging(args, file=shlex.quote(logname))

            filelist = list()
            for subdir in os.listdir(logdir):
                if subdir == '.DS_Store':
                    continue
                absdir = os.path.join(logdir, subdir)
                if not os.path.isdir(absdir):
                    continue
                if subdir != logdate:
                    tarname = f'{arcdir}/{subdir}.tar.gz'
                    with tarfile.open(tarname, 'w:gz') as tf:
                        abs_src = os.path.abspath(absdir)
                        for dirname, subdirs, files in os.walk(absdir):
                            for filename in files:
                                if filename == '.DS_Store':
                                    continue
                                name, ext = os.path.splitext(filename)
                                if ext != '.log':
                                    continue
                                absname = os.path.abspath(os.path.join(dirname, filename))
                                arcname = absname[len(abs_src) + 1:]
                                tf.add(absname, arcname)
                                filelist.append(arcname)
                        shutil.rmtree(absdir)

            ctime = datetime.datetime.fromtimestamp(os.stat(arcdir).st_birthtime)
            delta = today - ctime
            if delta > datetime.timedelta(7):
                arcdate = datetime.date.strftime(ctime, '%y%m%d')
                tarname = f'{tardir}/{arcdate}-{logdate}.tar.bz'
                with tarfile.open(tarname, 'w:bz2') as tf:
                    abs_src = os.path.abspath(arcdir)
                    for dirname, subdirs, files in os.walk(arcdir):
                        for filename in files:
                            if filename == '.DS_Store':
                                continue
                            name, ext = os.path.splitext(filename)
                            if ext != '.gz':
                                continue
                            absname = os.path.abspath(os.path.join(dirname, filename))
                            arcname = absname[len(abs_src) + 1:]
                            tf.add(absname, arcname)
                            filelist.append(arcname)
                    shutil.rmtree(arcdir)

            with open(logname, 'a') as logfile:
                if filelist:
                    arcflag = True
                    files = ', '.join(filelist)
                    logfile.write(f'LOG: archived following old logs: {files}\n')

        if dskpath.exists() and dskpath.is_dir():
            ctime = datetime.datetime.fromtimestamp(os.stat(config['Path']['logdir'] + '/tarfile').st_birthtime)
            delta = today - ctime
            if delta > datetime.timedelta(calendar.monthrange(today.year, today.month)[1]):
                arcdate = datetime.date.strftime(ctime, '%y%m%d')
                tarname = f'{tmpdir}/{arcdate}-{logdate}.tar.xz'
                with tarfile.open(tarname, 'w:xz') as tf:
                    abs_src = os.path.abspath('/Library/Logs/Scripts/tarfile')
                    for dirname, subdirs, files in os.walk(config['Path']['logdir'] + '/tarfile'):
                        for filename in files:
                            if filename == '.DS_Store':
                                continue
                            name, ext = os.path.splitext(filename)
                            if ext != '.bz':
                                continue
                            absname = os.path.abspath(os.path.join(dirname, filename))
                            arcname = absname[len(abs_src) + 1:]
                            tf.add(absname, arcname)
                    shutil.rmtree(config['Path']['logdir'] + '/tarfile')

                arcfile = config['Path']['arcdir'] + '/archive.zip'
                with zipfile.ZipFile(arcfile, 'a', zipfile.ZIP_DEFLATED) as zf:
                    arcname = os.path.split(tarname)[1]
                    zf.write(tarname, arcname)
                    os.remove(tarname)

        if arcflag and not args.quiet:
            arcdir = config['Path']['logdir'] + '/archive/logging'
            print(f'logging: {green}cleanup{reset}: ancient logs archived into {under}{arcdir}{reset}')
    except (KeyboardInterrupt, PermissionError):
        if logname and not args.quiet:
            print(f'logging: {red}{logmode}{reset}: logging procedure interrupted')


if __name__ == '__main__':
    sys.exit(main())
