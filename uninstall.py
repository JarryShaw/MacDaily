#!/usr/bin/python3
# -*- coding: utf-8 -*-


import argparse
import datetime
import libuninstall
import os
import pathlib
import platform
import sys


# version string
__version__ = '0.4.0'


# display mode names
NAME = dict(
    pip = 'Python',
    brew = 'Homebrew',
    cask = 'Caskroom',
)


# mode actions
MODE = dict(
    all = lambda *args, **kwargs: libuninstall.uninstall_all(*args, **kwargs),
    pip = lambda *args, **kwargs: libuninstall.uninstall_pip(*args, **kwargs),
    brew = lambda *args, **kwargs: libuninstall.uninstall_brew(*args, **kwargs),
    cask = lambda *args, **kwargs: libuninstall.uninstall_cask(*args, **kwargs),
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
    parser = argparse.ArgumentParser(prog='uninstall', description=(
        'Package Recursive Uninstall Manager'
    ))
    parser.add_argument('-V', '--version', action='version',
                        version='{}'.format(__version__))
    parser.add_argument('-a', '--all', action='store_true', default=False,
                        dest='all', help=(
                            'Uninstall all packages installed through pip, '
                            'Homebrew, and App Store.'
                        ))
    subparser = parser.add_subparsers(title='mode selection', metavar='MODE',
                        dest='mode', help=(
                            'Uninstall given packages installed through '
                            'a specified method, e.g.: pip, brew or cask.'
                        ))

    parser_pip = subparser.add_parser('pip', description=(
                            'Uninstall pip installed packages.'
                        ))
    parser_pip.add_argument('-a', '--all', action='store_true', default=True,
                        dest='all', help=(
                            'Uninstall all packages installed through pip.'
                        ))
    parser_pip.add_argument('-V', '--version', action='store', metavar='VER',
                        dest='version', type=int, help=(
                            'Indicate packages in which version of pip will '
                            'be uninstalled.'
                        ))
    parser_pip.add_argument('-s', '--system', action='store_true', default=False,
                        dest='system', help=(
                            'Uninstall pip packages on system level, i.e. python '
                            'installed through official installer.'
                        ))
    parser_pip.add_argument('-b', '--brew', action='store_true', default=False,
                        dest='brew', help=(
                            'Uninstall pip packages on Cellar level, i.e. python '
                            'installed through Homebrew.'
                        ))
    parser_pip.add_argument('-c', '--cpython', action='store_true', default=False,
                        dest='cpython', help=(
                            'Uninstall pip packages on CPython environment.'
                        ))
    parser_pip.add_argument('-y', '--pypy', action='store_true', default=False,
                        dest='pypy', help=(
                            'Uninstall pip packages on Pypy environment.'
                        ))
    parser_pip.add_argument('-p', '--package', metavar='PKG', action='append',
                        dest='package', help=(
                            'Name of packages to be uninstalled, default is null.'
                        ))
    parser_pip.add_argument('-i', '--ignore-dependencies', action='store_true',
                        default=False, dest='idep', help=(
                            'Run in irrecursive mode, i.e. ignore dependencies '
                            'of installing packages.'
                        ))
    parser_pip.add_argument('-q', '--quiet', action='store_true', default=False,
                        help=(
                            'Run in quiet mode, with no output information.'
                        ))
    parser_pip.add_argument('-v', '--verbose', action='store_true', default=False,
                        help=(
                            'Run in verbose mode, with more information.'
                        ))
    parser_pip.add_argument('-Y', '--yes', action='store_true', default=False,
                        dest='yes', help=(
                            'Yes for all selections.'
                        ))

    parser_brew = subparser.add_parser('brew', description=(
                            'Uninstall Homebrew installed packages.'
                        ))
    parser_brew.add_argument('-a', '--all', action='store_true', default=False,
                        dest='all', help=(
                            'Uninstall all packages installed through Homebrew.'
                        ))
    parser_brew.add_argument('-p', '--package', metavar='PKG', action='append',
                        dest='package', help=(
                            'Name of packages to be uninstalled, default is null.'
                        ))
    parser_brew.add_argument('-f', '--force', action='store_true', default=False,
                        help=(
                            'Use "--force" when running `brew uninstall`.'
                        ))
    parser_brew.add_argument('-i', '--ignore-dependencies', action='store_true',
                        default=False, dest='idep', help=(
                            'Run in irrecursive mode, i.e. ignore dependencies '
                            'of installing packages.'
                        ))
    parser_brew.add_argument('-q', '--quiet', action='store_true', default=False,
                        help=(
                            'Run in quiet mode, with no output information.'
                        ))
    parser_brew.add_argument('-v', '--verbose', action='store_true', default=False,
                        help=(
                            'Run in verbose mode, with more information.'
                        ))
    parser_brew.add_argument('-Y', '--yes', action='store_true', default=False,
                        dest='yes', help=(
                            'Yes for all selections.'
                        ))

    parser_cask = subparser.add_parser('cask', description=(
                            'Uninstall installed Caskroom packages.'
                        ))
    parser_cask.add_argument('-a', '--all', action='store_true', default=False,
                        dest='all', help=(
                            'Uninstall all packages installed through Caskroom.'
                        ))
    parser_cask.add_argument('-p', '--package', metavar='PKG', action='append',
                        dest='package', help=(
                            'Name of packages to be uninstalled, default is null.'
                        ))
    parser_cask.add_argument('-f', '--force', action='store_true', default=False,
                        help=(
                            'Use "--force" when running `brew cask uninstall`.'
                        ))
    parser_cask.add_argument('-q', '--quiet', action='store_true', default=False,
                        help=(
                            'Run in quiet mode, with no output information.'
                        ))
    parser_cask.add_argument('-v', '--verbose', action='store_true', default=False,
                        help=(
                            'Run in verbose mode, with more information.'
                        ))
    parser_cask.add_argument('-Y', '--yes', action='store_true', default=False,
                        dest='yes', help=(
                            'Yes for all selections.'
                        ))

    parser.add_argument('-f', '--force', action='store_true', default=False,
                        help=(
                            'Run in force mode, only for Homebrew and Caskroom.'
                        ))
    parser.add_argument('-i', '--ignore-dependencies', action='store_true',
                        default=False, dest='idep', help=(
                            'Run in irrecursive mode, only for Python and Homebrew.'
                        ))
    parser.add_argument('-q', '--quiet', action='store_true', default=False,
                        help=(
                            'Run in quiet mode, with no output information.'
                        ))
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help=(
                            'Run in verbose mode, with more information.'
                        ))
    parser.add_argument('-Y', '--yes', action='store_true', default=False,
                        dest='yes', help=(
                            'Yes for all selections.'
                        ))

    return parser


def main():
    if platform.system() != 'Darwin':
        os.system(f'echo "Script $({under})uninstall$({reset}) runs only on $({bold})$({red})macOS$({reset})."')
        sys.exit(1)

    parser = get_parser()
    args = parser.parse_args()

    pathlib.Path('/tmp/log').mkdir(parents=True, exist_ok=True)
    pathlib.Path('/Library/Logs/Scripts/uninstall').mkdir(parents=True, exist_ok=True)

    logdate = datetime.date.strftime(datetime.datetime.today(), '%y%m%d')
    logname = f'/Library/Logs/Scripts/uninstall/{logdate}.log'

    mode = '-*- Arguments -*-'.center(80, ' ')
    with open(logname, 'a') as logfile:
        logfile.write(datetime.date.strftime(datetime.datetime.today(), '%+').center(80, '—'))
        logfile.write(f'\n\nCMD: {python} {program}')
        logfile.write(f'\n\n{mode}\n\n')
        for key, value in args.__dict__.items():
            logfile.write(f'ARG: {key} = {value}\n')

    log = MODE.get(args.mode or 'all')(args, file=logname, date=logdate)
    if not args.quiet:
        os.system(f'echo "-*- $({blue})Uninstall Logs$({reset}) -*-"; echo ;')

        for mode in log:
            name = NAME.get(mode, mode)
            if log[mode] and all(log[mode]):
                pkgs = ', '.join(log[mode])
                comment = '' if args.idep else ' (including dependencies)'
                os.system(f'echo "Uninstalled following {name} packages: $({red}){pkgs}$({reset}){comment}."; echo ;')
            else:
                os.system(f'echo "$({green})No package uninstalled in {name}.$({reset})"; echo ;')

    mode = '-*- Uninstall Logs -*-'.center(80, ' ')
    with open(logname, 'a') as logfile:
        logfile.write(f'\n\n{mode}\n\n')
        for mode in log:
            name = NAME.get(mode, mode)
            if log[mode] and all(log[mode]):
                pkgs = ', '.join(log[mode])
                comment = '' if args.idep else ' (including dependencies)'
                logfile.write(f'LOG: Uninstalled following {name} packages: {pkgs}{comment}.\n')
            else:
                logfile.write(f'LOG: No package uninstalled in {name}.\n')
        logfile.write('\n\n\n\n')


if __name__ == '__main__':
    sys.exit(main())
