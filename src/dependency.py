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
__version__ = '0.7.5'


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


def get_parser():
    parser = argparse.ArgumentParser(prog='dependency', description=(
        'Trivial Package Dependency Manager'
    ))
    parser.add_argument('-V', '--version', action='version',
                        version='{}'.format(__version__))
    parser.add_argument('-a', '--all', action='store_true', default=True,
                        dest='all', help=(
                            'Show dependencies of all packages installed '
                            'through pip and Homebrew.'
                        ))
    subparser = parser.add_subparsers(title='mode selection', metavar='MODE',
                        dest='mode', help=(
                            'Show dependencies of packages installed through '
                            'a specified method, e.g.: pip or brew.'
                        ))

    parser_pip = subparser.add_parser('pip', description=(
                            'Show dependencies of Python packages.'
                        ))
    parser_pip.add_argument('-a', '--all', action='store_true', default=True,
                        dest='all', help=(
                            'Show dependencies of all packages installed through pip.'
                        ))
    parser_pip.add_argument('-v', '--pyver', action='store', metavar='VER',
                        choices=[
                            1, 2, 20, 21, 22, 23, 24, 25, 26, 27,
                            3, 30, 31, 32, 33, 34, 35, 36, 37,
                        ], dest='version', type=int, default=1, help=(
                            'Indicate which version of pip will be updated.'
                        ))
    parser_pip.add_argument('-s', '--system', action='store_true', default=False,
                        dest='system', help=(
                            'Show dependencies of pip packages on system level, i.e. python '
                            'installed through official installer.'
                        ))
    parser_pip.add_argument('-b', '--brew', action='store_true', default=False,
                        dest='brew', help=(
                            'Show dependencies of pip packages on Cellar level, i.e. python '
                            'installed through Homebrew.'
                        ))
    parser_pip.add_argument('-c', '--cpython', action='store_true', default=False,
                        dest='cpython', help=(
                            'Show dependencies of pip packages on CPython environment.'
                        ))
    parser_pip.add_argument('-y', '--pypy', action='store_true', default=False,
                        dest='pypy', help=(
                            'Show dependencies of pip packages on PyPy environment.'
                        ))
    parser_pip.add_argument('-p', '--package', metavar='PKG', action='append',
                        dest='package', help=(
                            'Name of packages to be shown, default is all.'
                        ))
    parser_pip.add_argument('-t', '--tree', action='store_true', default=False,
                        help=(
                            'Show dependencies as a tree. This feature requests '
                            '`pipdeptree`.'
                        ))

    parser_brew = subparser.add_parser('brew', description=(
                            'Show dependencies of Homebrew packages.'
                        ))
    parser_brew.add_argument('-a', '--all', action='store_true', default=True,
                        dest='all', help=(
                            'Show dependencies of all packages installed through Homebrew.'
                        ))
    parser_brew.add_argument('-p', '--package', metavar='PKG', action='append',
                        dest='package', help=(
                            'Name of packages to be shown, default is all.'
                        ))
    parser_brew.add_argument('-t', '--tree', action='store_true', default=False,
                        help=(
                            'Show dependencies as a tree.'
                        ))

    parser.add_argument('-t', '--tree', action='store_true', default=False,
                        help=(
                            'Show dependencies as a tree. This feature may request '
                            '`pipdeptree`.'
                        ))

    return parser


def main():
    if platform.system() != 'Darwin':
        os.system(f'echo "Script $({under})dependency$({reset}) runs only on $({bold})$({red})macOS$({reset})."')
        sys.exit(1)

    parser = get_parser()
    args = parser.parse_args()

    pathlib.Path('/tmp/log').mkdir(parents=True, exist_ok=True)
    pathlib.Path('/Library/Logs/Scripts/dependency').mkdir(parents=True, exist_ok=True)

    logdate = datetime.date.strftime(datetime.datetime.today(), '%y%m%d')
    logname = f'/Library/Logs/Scripts/dependency/{logdate}.log'

    mode = '-*- Arguments -*-'.center(80, ' ')
    with open(logname, 'a') as logfile:
        logfile.write(datetime.date.strftime(datetime.datetime.today(), '%+').center(80, '—'))
        logfile.write(f'\n\nCMD: {python} {program}')
        logfile.write(f'\n\n{mode}\n\n')
        for key, value in args.__dict__.items():
            logfile.write(f'ARG: {key} = {value}\n')

    dependency = MODE.get(args.mode or 'all')
    log = dependency(args, file=logname, date=logdate)

    filelist = list()
    with zipfile.ZipFile('/Library/Logs/Scripts/archive.zip', 'a', zipfile.ZIP_DEFLATED) as zf:
        abs_src = os.path.abspath('/Library/Logs/Scripts')
        for dirname, subdirs, files in os.walk('/Library/Logs/Scripts/dependency'):
            for filename in files:
                if filename == '.DS_Store':
                    continue
                filedate = datetime.datetime.strptime(filename.split('.')[0], '%y%m%d')
                today = datetime.datetime.today()
                delta = today - filedate
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
                pkgs = ', '.join(log[mode])
                logfile.write(f'LOG: Showed dependencies of following {name} packages: {pkgs}.\n')
            else:
                logfile.write(f'LOG: No dependencies showed in {name} packages.\n')

        if filelist:
            files = ', '.join(filelist)
            logfile.write(f'LOG: Archived following old logs: {files}\n')
        logfile.write('\n\n\n\n')


if __name__ == '__main__':
    sys.exit(main())
