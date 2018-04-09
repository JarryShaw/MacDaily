#!/usr/bin/python3
# -*- coding: utf-8 -*-


import argparse
import datetime
import os
import pathlib
import platform
import sys
import zipfile


from jsdaily.libuninstall import *


# version string
__version__ = '0.9.0'


# today
today = datetime.datetime.today()


# display mode names
NAME = dict(
    pip = 'Python',
    brew = 'Homebrew',
    cask = 'Caskroom',
)


# mode actions
MODE = dict(
    all = lambda *args, **kwargs: uninstall_all(*args, **kwargs),
    pip = lambda *args, **kwargs: uninstall_pip(*args, **kwargs),
    brew = lambda *args, **kwargs: uninstall_brew(*args, **kwargs),
    cask = lambda *args, **kwargs: uninstall_cask(*args, **kwargs),
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
    parser = argparse.ArgumentParser(prog='jsuninstall', description=(
                    'Package Recursive Uninstall Manager'
                ), usage=(
                    'jsuninstall [-hV] [-qv] [-fiY] [-a] [--[no-]MODE] MODE ... '
                ))
    parser.add_argument('-V', '--version', action='version', version=__version__)
    parser.add_argument('-a', '--all', action='append_const', const='all',
                        dest='mode', help=(
                            'uninstall all packages installed through pip, '
                            'Homebrew, and App Store'
                        ))

    parser.add_argument('--pip', action='append_const', const='pip', dest='mode', help=argparse.SUPPRESS)
    parser.add_argument('--brew', action='append_const', const='brew', dest='mode', help=argparse.SUPPRESS)
    parser.add_argument('--cask', action='append_const', const='cask', dest='mode', help=argparse.SUPPRESS)

    parser.add_argument('--no-pip', action='store_true', default=False, help=argparse.SUPPRESS)
    parser.add_argument('--no-brew', action='store_true', default=False, help=argparse.SUPPRESS)
    parser.add_argument('--no-cask', action='store_true', default=False, help=argparse.SUPPRESS)

    subparser = parser.add_subparsers(title='mode selection', metavar='MODE',
                        dest='mode', help=(
                            'uninstall given packages installed through '
                            'a specified method, e.g.: pip, brew or cask'
                        ))

    parser_pip = subparser.add_parser('pip', description=(
                            'Uninstall Installed Python Packages'
                        ), usage=(
                            'jsuninstall pip [-h] [-qv] [-iY] [-bcsy] [-V VER] [-a] [-p PKG]'
                        ))
    parser_pip.add_argument('-a', '--all', action='store_true', default=True,
                        dest='all', help=(
                            'uninstall all packages installed through pip'
                        ))
    parser_pip.add_argument('-V', '--python_version', action='store', metavar='VER',
                        choices=[
                            1, 2, 20, 21, 22, 23, 24, 25, 26, 27,
                            0, 3, 30, 31, 32, 33, 34, 35, 36, 37,
                        ], dest='version', type=int, default=0, help=(
                            'indicate packages in which version of pip will '
                            'be uninstalled'
                        ))
    parser_pip.add_argument('-s', '--system', action='store_true', default=False,
                        dest='system', help=(
                            'uninstall pip packages on system level, i.e. python '
                            'installed through official installer'
                        ))
    parser_pip.add_argument('-b', '--brew', action='store_true', default=False,
                        dest='brew', help=(
                            'uninstall pip packages on Cellar level, i.e. python '
                            'installed through Homebrew'
                        ))
    parser_pip.add_argument('-c', '--cpython', action='store_true', default=False,
                        dest='cpython', help=(
                            'uninstall pip packages on CPython environment'
                        ))
    parser_pip.add_argument('-y', '--pypy', action='store_true', default=False,
                        dest='pypy', help=(
                            'uninstall pip packages on Pypy environment'
                        ))
    parser_pip.add_argument('-p', '--package', metavar='PKG', action='append',
                        dest='package', help=(
                            'name of packages to be uninstalled, default is null'
                        ))
    parser_pip.add_argument('-i', '--ignore-dependencies', action='store_true',
                        default=False, dest='idep', help=(
                            'run in irrecursive mode, i.e. ignore dependencies '
                            'of installing packages'
                        ))
    parser_pip.add_argument('-q', '--quiet', action='store_true', default=False,
                        help=(
                            'run in quiet mode, with no output information'
                        ))
    parser_pip.add_argument('-v', '--verbose', action='store_true', default=False,
                        help=(
                            'run in verbose mode, with more information'
                        ))
    parser_pip.add_argument('-Y', '--yes', action='store_true', default=False,
                        dest='yes', help=(
                            'yes for all selections'
                        ))

    parser_brew = subparser.add_parser('brew', description=(
                            'Uninstall Installed Homebrew Packages'
                        ), usage=(
                            'jsuninstall brew [-h] [-qv] [-iY] [-f] [-a] [-p PKG]'
                        ))
    parser_brew.add_argument('-a', '--all', action='store_true', default=False,
                        dest='all', help=(
                            'uninstall all packages installed through Homebrew'
                        ))
    parser_brew.add_argument('-p', '--package', metavar='PKG', action='append',
                        dest='package', help=(
                            'name of packages to be uninstalled, default is null'
                        ))
    parser_brew.add_argument('-f', '--force', action='store_true', default=False,
                        help=(
                            'use "--force" when running `brew uninstall`'
                        ))
    parser_brew.add_argument('-i', '--ignore-dependencies', action='store_true',
                        default=False, dest='idep', help=(
                            'run in irrecursive mode, i.e. ignore dependencies '
                            'of installing packages'
                        ))
    parser_brew.add_argument('-q', '--quiet', action='store_true', default=False,
                        help=(
                            'run in quiet mode, with no output information'
                        ))
    parser_brew.add_argument('-v', '--verbose', action='store_true', default=False,
                        help=(
                            'run in verbose mode, with more information'
                        ))
    parser_brew.add_argument('-Y', '--yes', action='store_true', default=False,
                        dest='yes', help=(
                            'yes for all selections'
                        ))

    parser_cask = subparser.add_parser('cask', description=(
                            'Uninstall Installed Caskroom Packages'
                        ), usage=(
                            'jsuninstall cask [-h] [-qv] [-Y] [-f] [-a] [-p PKG]'
                        ))
    parser_cask.add_argument('-a', '--all', action='store_true', default=False,
                        dest='all', help=(
                            'uninstall all packages installed through Caskroom'
                        ))
    parser_cask.add_argument('-p', '--package', metavar='PKG', action='append',
                        dest='package', help=(
                            'name of packages to be uninstalled, default is null'
                        ))
    parser_cask.add_argument('-f', '--force', action='store_true', default=False,
                        help=(
                            'use "--force" when running `brew cask uninstall`'
                        ))
    parser_cask.add_argument('-q', '--quiet', action='store_true', default=False,
                        help=(
                            'run in quiet mode, with no output information'
                        ))
    parser_cask.add_argument('-v', '--verbose', action='store_true', default=False,
                        help=(
                            'run in verbose mode, with more information'
                        ))
    parser_cask.add_argument('-Y', '--yes', action='store_true', default=False,
                        dest='yes', help=(
                            'yes for all selections'
                        ))

    parser.add_argument('-f', '--force', action='store_true', default=False,
                        help=(
                            'run in force mode, only for Homebrew and Caskroom'
                        ))
    parser.add_argument('-i', '--ignore-dependencies', action='store_true',
                        default=False, dest='idep', help=(
                            'run in irrecursive mode, only for Python and Homebrew'
                        ))
    parser.add_argument('-q', '--quiet', action='store_true', default=False,
                        help=(
                            'run in quiet mode, with no output information'
                        ))
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help=(
                            'run in verbose mode, with more information'
                        ))
    parser.add_argument('-Y', '--yes', action='store_true', default=False,
                        dest='yes', help=(
                            'yes for all selections'
                        ))

    return parser


def main():
    if platform.system() != 'Darwin':
        raise UnsupoortedOS('uninstall: script runs only on macOS')

    parser = get_parser()
    args = parser.parse_args()

    if args.mode is None:
        parser.print_help()
        return

    pathlib.Path('/tmp/log').mkdir(parents=True, exist_ok=True)
    pathlib.Path('/Library/Logs/Scripts/uninstall').mkdir(parents=True, exist_ok=True)

    logdate = datetime.date.strftime(today, '%y%m%d')
    logname = f'/Library/Logs/Scripts/uninstall/{logdate}.log'

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
        uninstall = MODE.get(mode)
        log = uninstall(args, file=logname, date=logdate)

    arcfile = '/Library/Logs/Scripts/archive.zip'
    filelist = list()
    with zipfile.ZipFile(arcfile, 'a', zipfile.ZIP_DEFLATED) as zf:
        abs_src = os.path.abspath('/Library/Logs/Scripts')
        for dirname, subdirs, files in os.walk('/Library/Logs/Scripts/uninstall'):
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

    mode = '-*- Uninstall Logs -*-'.center(80, ' ')
    with open(logname, 'a') as logfile:
        logfile.write(f'\n\n{mode}\n\n')
        if not args.quiet:
            os.system(f'echo "-*- $({blue})Uninstall Logs$({reset}) -*-"; echo ;')

        for mode in log:
            name = NAME.get(mode, mode)
            if log[mode] and all(log[mode]):
                pkgs = f', '.join(log[mode])
                comment = '' if args.idep else ' (including dependencies)'
                logfile.write(f'LOG: Uninstalled following {name} packages: {pkgs}{comment}.\n')
                if not args.quiet:
                    pkgs_coloured = f'$({reset}), $({red})'.join(log[mode])
                    os.system(f'echo "uninstall: $({green}){mode}$({reset}): '
                              f'uninstalled following $({bold}){name}$({reset}) packages: $({red}){pkgs_coloured}$({reset}){comment}"')
            else:
                logfile.write(f'LOG: No package uninstalled in {name}.\n')
                if not args.quiet:
                    os.system(f'echo "uninstall: $({green}){mode}$({reset}): '
                              f'no package uninstalled in $({bold}){name}$({reset})"')

        if filelist:
            files = ', '.join(filelist)
            logfile.write(f'LOG: Archived following old logs: {files}\n')
            if not args.quiet:
                os.system(f'echo "uninstall: $({green})cleanup$({reset}): '
                          f'ancient logs archived into $({under}){arcfile}$({reset})."')
        logfile.write('\n\n\n\n')


if __name__ == '__main__':
    sys.exit(main())
