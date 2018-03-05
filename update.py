#!/usr/bin/python3
# -*- coding: utf-8 -*-


import argparse
import datetime
import libupdate
import os
import pathlib
import platform
import sys


# version string
__version__ = '0.6.0'


# display mode names
NAME = dict(
    apm = 'Atom',
    pip = 'Python',
    brew = 'Homebrew',
    cask = 'Caskroom',
    appstore = 'App Store',
)


# mode actions
MODE = dict(
    all = lambda *args, **kwargs: libupdate.update_all(*args, **kwargs),
    apm = lambda *args, **kwargs: libupdate.update_apm(*args, **kwargs),
    pip = lambda *args, **kwargs: libupdate.update_pip(*args, **kwargs),
    brew = lambda *args, **kwargs: libupdate.update_brew(*args, **kwargs),
    cask = lambda *args, **kwargs: libupdate.update_cask(*args, **kwargs),
    appstore = lambda *args, **kwargs: libupdate.update_appstore(*args, **kwargs),
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
    parser = argparse.ArgumentParser(prog='update', description=(
        'Automatic Package Update Manager'
    ))
    parser.add_argument('-V', '--version', action='version',
                        version='{}'.format(__version__))
    parser.add_argument('-a', '--all', action='store_true', default=False,
                        dest='all', help=(
                            'Update all packages installed through pip, '
                            'Homebrew, and App Store.'
                        ))
    subparser = parser.add_subparsers(title='mode selection', metavar='MODE',
                        dest='mode', help=(
                            'Update outdated packages installed through '
                            'a specified method, e.g.: apm, pip, brew, '
                            'cask, or appstore.'
                        ))

    parser_apm = subparser.add_parser('apm', description=(
                            'Update installed Atom packages.'
                        ))
    parser_apm.add_argument('-a', '--all', action='store_true', default=False,
                        dest='all', help=(
                            'Update all packages installed through apm.'
                        ))
    parser_apm.add_argument('-p', '--package', metavar='PKG', action='append',
                        dest='package', help=(
                            'Name of packages to be updated, default is all.'
                        ))
    parser_apm.add_argument('-q', '--quiet', action='store_true', default=False,
                        help=(
                            'Run in quiet mode, with no output information.'
                        ))
    parser_apm.add_argument('-v', '--verbose', action='store_true', default=False,
                        help=(
                            'Run in verbose mode, with detailed output information.'
                        ))
    # parser_apm.add_argument('extra', metavar='MODE', nargs='*', help='Other commands.')

    parser_pip = subparser.add_parser('pip', description=(
                            'Update installed Python packages.'
                        ))
    parser_pip.add_argument('-a', '--all', action='store_true', default=True,
                        dest='all', help=(
                            'Update all packages installed through pip.'
                        ))
    parser_pip.add_argument('-V', '--version', action='store', metavar='VER',
                        dest='version', type=int, help=(
                            'Indicate which version of pip will be updated.'
                        ))
    parser_pip.add_argument('-s', '--system', action='store_true', default=False,
                        dest='system', help=(
                            'Update pip packages on system level, i.e. python '
                            'installed through official installer.'
                        ))
    parser_pip.add_argument('-b', '--brew', action='store_true', default=False,
                        dest='brew', help=(
                            'Update pip packages on Cellar level, i.e. python '
                            'installed through Homebrew.'
                        ))
    parser_pip.add_argument('-c', '--cpython', action='store_true', default=False,
                        dest='cpython', help=(
                            'Update pip packages on CPython environment.'
                        ))
    parser_pip.add_argument('-y', '--pypy', action='store_true', default=False,
                        dest='pypy', help=(
                            'Update pip packages on PyPy environment.'
                        ))
    parser_pip.add_argument('-p', '--package', metavar='PKG', action='append',
                        dest='package', help=(
                            'Name of packages to be updated, default is all.'
                        ))
    parser_pip.add_argument('-q', '--quiet', action='store_true', default=False,
                        help=(
                            'Run in quiet mode, with no output information.'
                        ))
    parser_pip.add_argument('-v', '--verbose', action='store_true', default=False,
                        help=(
                            'Run in verbose mode, with detailed output information.'
                        ))
    # parser_pip.add_argument('extra', metavar='MODE', nargs='*', help='Other commands.')

    parser_brew = subparser.add_parser('brew', description=(
                            'Update installed Homebrew packages.'
                        ))
    parser_brew.add_argument('-a', '--all', action='store_true', default=False,
                        dest='all', help=(
                            'Update all packages installed through Homebrew.'
                        ))
    parser_brew.add_argument('-p', '--package', metavar='PKG', action='append',
                        dest='package', help=(
                            'Name of packages to be updated, default is all.'
                        ))
    parser_brew.add_argument('-f', '--force', action='store_true', default=False,
                        help=(
                            'Use "--force" when running `brew update`.'
                        ))
    parser_brew.add_argument('-m', '--merge', action='store_true', default=False,
                        help=(
                            'Use "--merge" when running `brew update`.'
                        ))
    parser_brew.add_argument('-q', '--quiet', action='store_true', default=False,
                        help=(
                            'Run in quiet mode, with no output information.'
                        ))
    parser_brew.add_argument('-v', '--verbose', action='store_true', default=False,
                        help=(
                            'Run in verbose mode, with detailed output information.'
                        ))
    # parser_brew.add_argument('extra', metavar='MODE', nargs='*', help='Other commands.')

    parser_cask = subparser.add_parser('cask', description=(
                            'Update installed Caskroom packages.'
                        ))
    parser_cask.add_argument('-a', '--all', action='store_true', default=False,
                        dest='all', help=(
                            'Update all packages installed through Caskroom.'
                        ))
    parser_cask.add_argument('-p', '--package', metavar='PKG', action='append',
                        dest='package', help=(
                            'Name of packages to be updated, default is all.'
                        ))
    parser_cask.add_argument('-f', '--force', action='store_true', default=False,
                        help=(
                            'Use "--force" when running `brew cask upgrade`.'
                        ))
    parser_cask.add_argument('-g', '--greedy', action='store_true', default=False,
                        help=(
                            'Use "--greedy" when running `brew cask outdated`, '
                            'and directly run `brew cask upgrade --greedy`.'
                        ))
    parser_cask.add_argument('-q', '--quiet', action='store_true', default=False,
                        help=(
                            'Run in quiet mode, with no output information.'
                        ))
    parser_cask.add_argument('-v', '--verbose', action='store_true', default=False,
                        help=(
                            'Run in verbose mode, with detailed output information.'
                        ))
    # parser_cask.add_argument('extra', metavar='MODE', nargs='*', help='Other commands.')

    parser_appstore = subparser.add_parser('appstore', description=(
                            'Update installed App Store packages.'
                        ))
    parser_appstore.add_argument('-a', '--all', action='store_true', default=False,
                        dest='all', help=(
                            'Update all packages installed through App Store.'
                        ))
    parser_appstore.add_argument('-p', '--package', metavar='PKG', action='append',
                        dest='package', help=(
                            'Name of packages to be updated, default is all.'
                        ))
    parser_appstore.add_argument('-q', '--quiet', action='store_true', default=False,
                        help=(
                            'Run in quiet mode, with no output information.'
                        ))
    # parser_appstore.add_argument('extra', metavar='MODE', nargs='*', help='Other commands.')

    parser.add_argument('-f', '--force', action='store_true', default=False,
                        help=(
                            'Run in force mode, only for Homebrew or Caskroom.'
                        ))
    parser.add_argument('-m', '--merge', action='store_true', default=False,
                        help=(
                            'Run in merge mode, only for Homebrew.'
                        ))
    parser.add_argument('-g', '--greedy', action='store_true', default=False,
                        help=(
                            'Run in greedy mode, only for Caskroom.'
                        ))
    parser.add_argument('-q', '--quiet', action='store_true', default=False,
                        help=(
                            'Run in quiet mode, with no output information.'
                        ))
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help=(
                            'Run in verbose mode, with detailed output information.'
                        ))
    # parser.add_argument('extra', metavar='MODE', nargs='*', help='Other commands.')

    return parser


def main():
    if platform.system() != 'Darwin':
        os.system(f'echo "Script $({under})update$({reset}) runs only on $({bold})$({red})macOS$({reset})."')
        sys.exit(1)

    # sys.argv.insert(1, '--all')
    parser = get_parser()
    args = parser.parse_args()

    pathlib.Path('/tmp/log').mkdir(parents=True, exist_ok=True)
    pathlib.Path('/Library/Logs/Scripts/update').mkdir(parents=True, exist_ok=True)

    logdate = datetime.date.strftime(datetime.datetime.today(), '%y%m%d')
    logname = f'/Library/Logs/Scripts/update/{logdate}.log'

    mode = '-*- Arguments -*-'.center(80, ' ')
    with open(logname, 'a') as logfile:
        logfile.write(datetime.date.strftime(datetime.datetime.today(), '%+').center(80, '—'))
        logfile.write(f'\n\nCMD: {python} {program}')
        logfile.write(f'\n\n{mode}\n\n')
        for key, value in args.__dict__.items():
            logfile.write(f'ARG: {key} = {value}\n')

    log = MODE.get(args.mode or 'all')(args, file=logname, date=logdate)
    if not args.quiet:
        os.system(f'echo "-*- $({blue})Update Logs$({reset}) -*-"; echo ;')

        for mode in log:
            name = NAME.get(mode, mode)
            if log[mode] and all(log[mode]):
                pkgs = ', '.join(log[mode])
                os.system(f'echo "Updated following {name} packages: $({red}){pkgs}$({reset})."; echo ;')
            else:
                os.system(f'echo "$({green})No package updated in {name}.$({reset})"; echo ;')

    mode = '-*- Update Logs -*-'.center(80, ' ')
    with open(logname, 'a') as logfile:
        logfile.write(f'\n\n{mode}\n\n')
        for mode in log:
            name = NAME.get(mode, mode)
            if log[mode] and all(log[mode]):
                pkgs = ', '.join(log[mode])
                logfile.write(f'LOG: Updated following {name} packages: {pkgs}.\n')
            else:
                logfile.write(f"LOG: No package updated in {name}.\n")
        logfile.write('\n\n\n\n')


if __name__ == '__main__':
    sys.exit(main())
