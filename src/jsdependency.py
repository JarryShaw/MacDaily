#!/usr/bin/python3
# -*- coding: utf-8 -*-


import argparse
import datetime
import os
import pathlib
import platform
import sys
import zipfile


from jsdaily.libdependency import *


# version string
__version__ = '0.8.0'


# today
today = datetime.datetime.today()


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
python = sys.prefix             # Python version
program = ' '.join(sys.argv)    # arguments


# terminal display
red = 'tput setaf 1'    # blush / red
green = 'tput setaf 2'  # green
blue = 'tput setaf 14'  # blue
bold = 'tput bold'      # bold
under = 'tput smul'     # underline
reset = 'tput sgr0'     # reset


# error handling class
class UnsupoortedOS(RuntimeError):
    def __init__(self, message, *args, **kwargs):
        sys.tracebacklimit = 0
        super().__init__(message, *args, **kwargs)


def get_parser():
    parser = argparse.ArgumentParser(prog='jsdeps', description=(
        'Trivial Package Dependency Manager'
    ), usage=(
        'jsdeps [-hV] [-t] [-a] [--[no-]MODE] MODE ... '
    ))
    parser.add_argument('-V', '--version', action='version', version=__version__)
    parser.add_argument('-a', '--all', action='append_const', const='all',
                        dest='mode', help=(
                            'show dependencies of all packages installed '
                            'through pip and Homebrew'
                        ))

    parser.add_argument('--brew', action='append_const', const='brew', dest='mode', help=argparse.SUPPRESS)
    parser.add_argument('--cask', action='append_const', const='cask', dest='mode', help=argparse.SUPPRESS)

    parser.add_argument('--no-brew', action='store_true', default=False, help=argparse.SUPPRESS)
    parser.add_argument('--no-cask', action='store_true', default=False, help=argparse.SUPPRESS)

    subparser = parser.add_subparsers(title='mode selection', metavar='MODE',
                        dest='mode', help=(
                            'show dependencies of packages installed through '
                            'a specified method, e.g.: pip or brew'
                        ))

    parser_pip = subparser.add_parser('pip', description=(
                            'Show Dependencies of Python Packages'
                        ), usage=(
                            'jsdeps pip [-h] [-qv] [-bcsy] [-V VER] [-a] [-p PKG]'
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

    parser_brew = subparser.add_parser('brew', description=(
                            'Show Dependencies of Homebrew Packages'
                        ), usage=(
                            'jsdeps brew [-h] [-t] [-a] [-p PKG]'
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

    parser.add_argument('-t', '--tree', action='store_true', default=False,
                        help=(
                            'show dependencies as a tree. This feature may request '
                            '`pipdeptree`'
                        ))

    return parser


def main():
    if platform.system() != 'Darwin':
        raise UnsupoortedOS('dependency: script runs only on macOS')

    parser = get_parser()
    args = parser.parse_args()

    if args.mode is None:
        parser.print_help()
        return

    pathlib.Path('/tmp/log').mkdir(parents=True, exist_ok=True)
    pathlib.Path('/Library/Logs/Scripts/dependency').mkdir(parents=True, exist_ok=True)

    logdate = datetime.date.strftime(today, '%y%m%d')
    logname = f'/Library/Logs/Scripts/dependency/{logdate}.log'

    mode = '-*- Arguments -*-'.center(80, ' ')
    with open(logname, 'a') as logfile:
        logfile.write(datetime.date.strftime(today, '%+').center(80, '—'))
        logfile.write(f'\n\nCMD: {python} {program}')
        logfile.write(f'\n\n{mode}\n\n')
        for key, value in args.__dict__.items():
            logfile.write(f'ARG: {key} = {value}\n')

    if isinstance(args.mode, str):
        args.mode = [args.mode]
    for mode in args.mode:
        dependency = MODE.get(mode)
        log = dependency(args, file=logname, date=logdate)

    arcfile = '/Library/Logs/Scripts/archive.zip'
    filelist = list()
    with zipfile.ZipFile(arcfile, 'a', zipfile.ZIP_DEFLATED) as zf:
        abs_src = os.path.abspath('/Library/Logs/Scripts')
        for dirname, subdirs, files in os.walk('/Library/Logs/Scripts/dependency'):
            for filename in files:
                if filename == '.DS_Store':
                    continue
                name, ext = os.path.splitext(filename)
                if ext != '.log':
                    continue
                ctime = datetime.datetime.strptime(name, '%y%m%d')
                delta = today - ctime
                if delta > datetime.timedelta(7):
                    absname = os.path.abspath(os.path.join(dirname, filename))
                    arcname = absname[len(abs_src) + 1:]
                    zf.write(absname, arcname)
                    filelist.append(arcname)
                    os.remove(absname)

    mode = '-*- Dependency Logs -*-'.center(80, ' ')
    with open(logname, 'a') as logfile:
        logfile.write(f'\n\n{mode}\n\n')

        for mode in log:
            name = NAME.get(mode, mode)
            if log[mode] and all(log[mode]):
                pkgs = f', '.join(log[mode])
                logfile.write(f'LOG: Showed dependencies of following {name} packages: {pkgs}.\n')
            else:
                logfile.write(f'LOG: No dependencies showed in {name} packages.\n')

        if filelist:
            files = ', '.join(filelist)
            logfile.write(f'LOG: Archived following old logs: {files}\n')
            if not args.quiet:
                os.system(f'echo "dependency: $({green})cleanup$({reset}): '
                          f'ancient logs archived into $({under}){arcfile}$({reset})"')
        logfile.write('\n\n\n\n')


if __name__ == '__main__':
    sys.exit(main())
