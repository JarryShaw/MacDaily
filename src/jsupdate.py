#!/usr/bin/python3
# -*- coding: utf-8 -*-


import argparse
import datetime
import os
import pathlib
import platform
import sys
import zipfile


from jsdaily.libupdate import *


# version string
__version__ = '0.11.2'


# today
today = datetime.datetime.today()


# display mode names
NAME = dict(
    apm = 'Atom',
    gem = 'Ruby',
    npm = 'Node.js',
    pip = 'Python',
    brew = 'Homebrew',
    cask = 'Caskroom',
    appstore = 'App Store',
)


# mode actions
MODE = dict(
    all = lambda *args, **kwargs: update_all(*args, **kwargs),
    apm = lambda *args, **kwargs: update_apm(*args, **kwargs),
    gem = lambda *args, **kwargs: update_gem(*args, **kwargs),
    npm = lambda *args, **kwargs: update_npm(*args, **kwargs),
    pip = lambda *args, **kwargs: update_pip(*args, **kwargs),
    brew = lambda *args, **kwargs: update_brew(*args, **kwargs),
    cask = lambda *args, **kwargs: update_cask(*args, **kwargs),
    cleanup = lambda *args, **kwargs: update_cleanup(*args, **kwargs),
    appstore = lambda *args, **kwargs: update_appstore(*args, **kwargs),
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
    parser = argparse.ArgumentParser(prog='jsupdate', description=(
                    'Automatic Package Update Manager'
                ), usage=(
                    'jsupdate [-hV] [-qv] [-fgm] [-a] [--[no-]MODE] MODE ... '
                ))
    parser.add_argument('-V', '--version', action='version', version=__version__)
    parser.add_argument('-a', '--all', action='append_const', const='all',
                        dest='mode', help=(
                            'update all packages installed through Atom, pip '
                            'RubyGem, Node.js, Homebrew, App Store, and etc'
                        ))

    parser.add_argument('--apm', action='append_const', const='apm', dest='mode', help=argparse.SUPPRESS)
    parser.add_argument('--gem', action='append_const', const='gem', dest='mode', help=argparse.SUPPRESS)
    parser.add_argument('--npm', action='append_const', const='npm', dest='mode', help=argparse.SUPPRESS)
    parser.add_argument('--pip', action='append_const', const='pip', dest='mode', help=argparse.SUPPRESS)
    parser.add_argument('--brew', action='append_const', const='brew', dest='mode', help=argparse.SUPPRESS)
    parser.add_argument('--cask', action='append_const', const='cask', dest='mode', help=argparse.SUPPRESS)
    parser.add_argument('--cleanup', action='append_const', const='cleanup', dest='mode', help=argparse.SUPPRESS)
    parser.add_argument('--appstore', action='append_const', const='appstore', dest='mode', help=argparse.SUPPRESS)

    parser.add_argument('--no-apm', action='store_true', default=False, help=argparse.SUPPRESS)
    parser.add_argument('--no-gem', action='store_true', default=False, help=argparse.SUPPRESS)
    parser.add_argument('--no-npm', action='store_true', default=False, help=argparse.SUPPRESS)
    parser.add_argument('--no-pip', action='store_true', default=False, help=argparse.SUPPRESS)
    parser.add_argument('--no-brew', action='store_true', default=False, help=argparse.SUPPRESS)
    parser.add_argument('--no-cask', action='store_true', default=False, help=argparse.SUPPRESS)
    parser.add_argument('--no-cleanup', action='store_true', default=False, help=argparse.SUPPRESS)
    parser.add_argument('--no-appstore', action='store_true', default=False, help=argparse.SUPPRESS)

    subparser = parser.add_subparsers(title='mode selection', metavar='MODE',
                        dest='mode', help=(
                            'update outdated packages installed through '
                            'a specified method, e.g.: apm, pip, brew, '
                            'cask, appstore, or alternatively and simply, '
                            'cleanup'
                        ))

    parser_apm = subparser.add_parser('apm', description=(
                            'Update Installed Atom Packages'
                        ), usage=(
                            'jsupdate apm [-h] [-qv] [-a] [-p PKG]'
                        ))
    parser_apm.add_argument('-a', '--all', action='store_true', default=False,
                        dest='all', help=(
                            'update all packages installed through apm'
                        ))
    parser_apm.add_argument('-p', '--package', metavar='PKG', action='append',
                        dest='package', help=(
                            'name of packages to be updated, default is all'
                        ))
    parser_apm.add_argument('-q', '--quiet', action='store_true', default=False,
                        help=(
                            'run in quiet mode, with no output information'
                        ))
    parser_apm.add_argument('-v', '--verbose', action='store_true', default=False,
                        help=(
                            'run in verbose mode, with detailed output information'
                        ))

    parser_gem = subparser.add_parser('gem', description=(
                            'Update Installed Ruby Packages'
                        ), usage=(
                            'jsupdate gem [-h] [-qv] [-a] [-p PKG]'
                        ))
    parser_gem.add_argument('-a', '--all', action='store_true', default=False,
                        dest='all', help=(
                            'update all packages installed through gem'
                        ))
    parser_gem.add_argument('-p', '--package', metavar='PKG', action='append',
                        dest='package', help=(
                            'name of packages to be updated, default is all'
                        ))
    parser_gem.add_argument('-q', '--quiet', action='store_true', default=False,
                        help=(
                            'run in quiet mode, with no output information'
                        ))
    parser_gem.add_argument('-v', '--verbose', action='store_true', default=False,
                        help=(
                            'run in verbose mode, with detailed output information'
                        ))

    parser_npm = subparser.add_parser('npm', description=(
                            'Update Installed Node.js Packages'
                        ), usage=(
                            'jsupdate npm [-h] [-qv] [-a] [-p PKG]'
                        ))
    parser_npm.add_argument('-a', '--all', action='store_true', default=False,
                        dest='all', help=(
                            'update all packages installed through npm'
                        ))
    parser_npm.add_argument('-p', '--package', metavar='PKG', action='append',
                        dest='package', help=(
                            'name of packages to be updated, default is all'
                        ))
    parser_npm.add_argument('-q', '--quiet', action='store_true', default=False,
                        help=(
                            'run in quiet mode, with no output information'
                        ))
    parser_npm.add_argument('-v', '--verbose', action='store_true', default=False,
                        help=(
                            'run in verbose mode, with detailed output information'
                        ))

    parser_pip = subparser.add_parser('pip', description=(
                            'Update Installed Python Packages'
                        ), usage=(
                            'jsupdate pip [-h] [-qv] [-bcsy] [-V VER] [-a] [-p PKG]'
                        ))
    parser_pip.add_argument('-a', '--all', action='store_true', default=False,
                        dest='all', help=(
                            'update all packages installed through pip'
                        ))
    parser_pip.add_argument('-V', '--python_version', action='store', metavar='VER',
                        choices=[
                            1, 2, 20, 21, 22, 23, 24, 25, 26, 27,
                            0, 3, 30, 31, 32, 33, 34, 35, 36, 37,
                        ], dest='version', type=int, default=0, help=(
                            'indicate which version of pip will be updated'
                        ))
    parser_pip.add_argument('-s', '--system', action='store_true', default=False,
                        dest='system', help=(
                            'update pip packages on system level, i.e. python '
                            'installed through official installer'
                        ))
    parser_pip.add_argument('-b', '--brew', action='store_true', default=False,
                        dest='brew', help=(
                            'update pip packages on Cellar level, i.e. python '
                            'installed through Homebrew'
                        ))
    parser_pip.add_argument('-c', '--cpython', action='store_true', default=False,
                        dest='cpython', help=(
                            'update pip packages on CPython environment'
                        ))
    parser_pip.add_argument('-y', '--pypy', action='store_true', default=False,
                        dest='pypy', help=(
                            'update pip packages on PyPy environment'
                        ))
    parser_pip.add_argument('-p', '--package', metavar='PKG', action='append',
                        dest='package', help=(
                            'name of packages to be updated, default is all'
                        ))
    parser_pip.add_argument('-q', '--quiet', action='store_true', default=False,
                        help=(
                            'run in quiet mode, with no output information'
                        ))
    parser_pip.add_argument('-v', '--verbose', action='store_true', default=False,
                        help=(
                            'run in verbose mode, with detailed output information'
                        ))

    parser_brew = subparser.add_parser('brew', description=(
                            'Update Installed Homebrew Packages'
                        ), usage=(
                            'jsupdate brew [-h] [-qv] [-fm] [-a] [-p PKG] [--no-cleanup]'
                        ))
    parser_brew.add_argument('-a', '--all', action='store_true', default=False,
                        dest='all', help=(
                            'update all packages installed through Homebrew'
                        ))
    parser_brew.add_argument('-p', '--package', metavar='PKG', action='append',
                        dest='package', help=(
                            'name of packages to be updated, default is all'
                        ))
    parser_brew.add_argument('-f', '--force', action='store_true', default=False,
                        help=(
                            'use "--force" when running `brew update`'
                        ))
    parser_brew.add_argument('-m', '--merge', action='store_true', default=False,
                        help=(
                            'use "--merge" when running `brew update`'
                        ))
    parser_brew.add_argument('-q', '--quiet', action='store_true', default=False,
                        help=(
                            'run in quiet mode, with no output information'
                        ))
    parser_brew.add_argument('-v', '--verbose', action='store_true', default=False,
                        help=(
                            'run in verbose mode, with detailed output information'
                        ))
    parser_brew.add_argument('--no-cleanup', action='store_false', default=True,
                        dest='nocleanup', help=(
                            'do not remove caches & downloads'
                        ))

    parser_cask = subparser.add_parser('cask', description=(
                            'Update Installed Caskroom Packages'
                        ), usage=(
                            'jsupdate cask [-h] [-qv] [-fg] [-a] [-p PKG] [--no-cleanup]'
                        ))
    parser_cask.add_argument('-a', '--all', action='store_true', default=False,
                        dest='all', help=(
                            'update all packages installed through Caskroom'
                        ))
    parser_cask.add_argument('-p', '--package', metavar='PKG', action='append',
                        dest='package', help=(
                            'name of packages to be updated, default is all'
                        ))
    parser_cask.add_argument('-f', '--force', action='store_true', default=False,
                        help=(
                            'use "--force" when running `brew cask upgrade`'
                        ))
    parser_cask.add_argument('-g', '--greedy', action='store_true', default=False,
                        help=(
                            'use "--greedy" when running `brew cask outdated`, '
                            'and directly run `brew cask upgrade --greedy`'
                        ))
    parser_cask.add_argument('-q', '--quiet', action='store_true', default=False,
                        help=(
                            'run in quiet mode, with no output information'
                        ))
    parser_cask.add_argument('-v', '--verbose', action='store_true', default=False,
                        help=(
                            'run in verbose mode, with detailed output information'
                        ))
    parser_cask.add_argument('--no-cleanup', action='store_false', default=True,
                        dest='nocleanup', help=(
                            'do not remove caches & downloads'
                        ))

    parser_cleanup = subparser.add_parser('cleanup', description=(
                            'Cleanup Caches & Downloads'
                        ), usage=(
                            'jsupdate cleanup [-h] [-q] [--no-brew] [--no-cask]'
                        ))
    parser_cleanup.add_argument('--no-gem', dest='gem', action='store_false', default=True,
                        help=(
                            'do not remove Ruby caches & downloads'
                        ))
    parser_cleanup.add_argument('--no-npm', dest='npm', action='store_false', default=True,
                        help=(
                            'do not remove Node.js caches & downloads'
                        ))
    parser_cleanup.add_argument('--no-pip', dest='pip', action='store_false', default=True,
                        help=(
                            'do not remove Python caches & downloads'
                        ))
    parser_cleanup.add_argument('--no-brew', dest='brew', action='store_false', default=True,
                        help=(
                            'do not remove Homebrew caches & downloads'
                        ))
    parser_cleanup.add_argument('--no-cask', dest='cask', action='store_false', default=True,
                        help=(
                            'do not remove Caskroom caches & downloads'
                        ))
    parser_cleanup.add_argument('-q', '--quiet', action='store_true', default=False,
                        help=(
                            'run in quiet mode, with no output information'
                        ))

    parser_appstore = subparser.add_parser('appstore', description=(
                            'Update installed App Store packages'
                        ), usage=(
                            'jsupdate appstore [-h] [-q] [-a] [-p PKG]'
                        ))
    parser_appstore.add_argument('-a', '--all', action='store_true', default=False,
                        dest='all', help=(
                            'update all packages installed through App Store'
                        ))
    parser_appstore.add_argument('-p', '--package', metavar='PKG', action='append',
                        dest='package', help=(
                            'name of packages to be updated, default is all'
                        ))
    parser_appstore.add_argument('-r', '--restart', action='store_true', default=False,
                        dest='restart', help=(
                            'automatically restart if necessary'
                        ))
    parser_appstore.add_argument('-q', '--quiet', action='store_true', default=False,
                        help=(
                            'run in quiet mode, with no output information'
                        ))

    parser.add_argument('-f', '--force', action='store_true', default=False,
                        help=(
                            'run in force mode, only for Homebrew or Caskroom'
                        ))
    parser.add_argument('-m', '--merge', action='store_true', default=False,
                        help=(
                            'run in merge mode, only for Homebrew'
                        ))
    parser.add_argument('-g', '--greedy', action='store_true', default=False,
                        help=(
                            'run in greedy mode, only for Caskroom'
                        ))
    parser.add_argument('-r', '--restart', action='store_true', default=False,
                        dest='restart', help=(
                            'automatically restart if necessary, only for App Store'
                        ))
    parser.add_argument('-q', '--quiet', action='store_true', default=False,
                        help=(
                            'run in quiet mode, with no output information'
                        ))
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help=(
                            'run in verbose mode, with detailed output information'
                        ))

    return parser


def main():
    if platform.system() != 'Darwin':
        raise UnsupoortedOS('update: script runs only on macOS')

    parser = get_parser()
    args = parser.parse_args()

    if args.mode is None:
        parser.print_help()
        return

    pathlib.Path('/tmp/log').mkdir(parents=True, exist_ok=True)
    pathlib.Path('/Library/Logs/Scripts/update').mkdir(parents=True, exist_ok=True)

    logdate = datetime.date.strftime(today, '%y%m%d')
    logname = f'/Library/Logs/Scripts/update/{logdate}.log'

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
        update = MODE.get(mode)
        log = update(args, file=logname, date=logdate)

    arcfile = '/Library/Logs/Scripts/archive.zip'
    filelist = list()
    with zipfile.ZipFile(arcfile, 'a', zipfile.ZIP_DEFLATED) as zf:
        abs_src = os.path.abspath('/Library/Logs/Scripts')
        for dirname, subdirs, files in os.walk('/Library/Logs/Scripts/update'):
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

    mode = '-*- Update Logs -*-'.center(80, ' ')
    with open(logname, 'a') as logfile:
        logfile.write(f'\n\n{mode}\n\n')
        if not args.quiet:
            os.system(f'echo "-*- $({blue})Update Logs$({reset}) -*-"; echo ;')

        for mode in log:
            name = NAME.get(mode, mode)
            if log[mode] and all(log[mode]):
                pkgs = f', '.join(log[mode])
                logfile.write(f'LOG: Updated following {name} packages: {pkgs}.\n')
                if not args.quiet:
                    pkgs_coloured = f'$({reset}), $({red})'.join(log[mode])
                    os.system(f'echo "update: $({green}){mode}$({reset}): '
                              f'updated following $({bold}){name}$({reset}) packages: $({red}){pkgs_coloured}$({reset})"')
            else:
                logfile.write(f"LOG: No package updated in {name}.\n")
                if not args.quiet:
                    os.system(f'echo "update: $({green}){mode}$({reset}): '
                              f'no package updated in $({bold}){name}$({reset})"')

        if filelist:
            files = ', '.join(filelist)
            logfile.write(f'LOG: Archived following old logs: {files}\n')
            if not args.quiet:
                os.system(f'echo "update: $({green})cleanup$({reset}): '
                          f'ancient logs archived into $({under}){arcfile}$({reset})"')
        logfile.write('\n\n\n\n')


if __name__ == '__main__':
    sys.exit(main())
