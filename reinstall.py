#!/usr/bin/python3
# -*- coding: utf-8 -*-


import argparse
import datetime
import libprinstall
import os
import pathlib
import platform
import sys


# version string
__version__ = '0.4.1'


# display mode names
NAME = dict(
    brew = 'Homebrew',
    cask = 'Caskroom',
)


# mode actions
MODE = dict(
    all = lambda *args, **kwargs: libprinstall.reinstall_all(*args, **kwargs),
    brew = lambda *args, **kwargs: libprinstall.reinstall_brew(*args, **kwargs),
    cask = lambda *args, **kwargs: libprinstall.reinstall_cask(*args, **kwargs),
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
    parser = argparse.ArgumentParser(prog='reinstall', description=(
        'Homebrew Package Reinstall Manager'
    ))
    parser.add_argument('-V', '--version', action='version',
                        version='{}'.format(__version__))
    parser.add_argument('-a', '--all', action='store_true', default=False,
                        dest='all', help=(
                            'Reinstall all packages installed through Homebrew '
                            'and Caskroom.'
                        ))
    subparser = parser.add_subparsers(title='mode selection', metavar='MODE',
                        dest='mode', help=(
                            'Reinstall packages installed through a '
                            'specified method, e.g.: brew or cask.'
                        ))

    parser_brew = subparser.add_parser('brew', description=(
                            'Reinstall Homebrew packages.'
                        ))
    parser_brew.add_argument('-a', '--all', action='store_true', default=False,
                        dest='all', help=(
                            'Reinstall all packages installed through Homebrew.'
                        ))
    parser_brew.add_argument('-p', '--package', metavar='PKG', action='append',
                        dest='package', help=(
                            'Name of packages to be reinstalled, default is null.'
                        ))
    parser_brew.add_argument('-s', '--startwith', metavar='START', action='store',
                        dest='start', help=(
                            'Reinstall procedure starts from which package, sort '
                            'in initial alphabets.'
                        ))
    parser_brew.add_argument('-e', '--endwith', metavar='START', action='store',
                        dest='end', help=(
                            'Reinstall procedure ends until which package, sort '
                            'in initial alphabets.'
                        ))
    parser_brew.add_argument('-f', '--force', action='store_true', default=False,
                        help=(
                            'Run in force mode, using for `brew reinstall`.'
                        ))
    parser_brew.add_argument('-q', '--quiet', action='store_true', default=False,
                        help=(
                            'Run in quiet mode, with no output information.'
                        ))
    parser_brew.add_argument('-v', '--verbose', action='store_true', default=False,
                        help=(
                            'Run in verbose mode, with detailed output information.'
                        ))

    parser_cask = subparser.add_parser('cask', description=(
                            'Reinstall Caskroom packages.'
                        ))
    parser_cask.add_argument('-a', '--all', action='store_true', default=False,
                        dest='all', help=(
                            'Reinstall all packages installed through Caskroom.'
                        ))
    parser_cask.add_argument('-p', '--package', metavar='PKG', action='append',
                        dest='package', help=(
                            'Name of packages to be reinstalled, default is null.'
                        ))
    parser_cask.add_argument('-s', '--startwith', metavar='START', action='store',
                        dest='start', help=(
                            'Reinstall procedure starts from which package, sort '
                            'in initial alphabets.'
                        ))
    parser_cask.add_argument('-e', '--endwith', metavar='START', action='store',
                        dest='end', help=(
                            'Reinstall procedure ends until which package, sort '
                            'in initial alphabets.'
                        ))
    parser_cask.add_argument('-q', '--quiet', action='store_true', default=False,
                        help=(
                            'Run in quiet mode, with no output information.'
                        ))
    parser_cask.add_argument('-v', '--verbose', action='store_true', default=False,
                        help=(
                            'Run in verbose mode, with detailed output information.'
                        ))

    parser.add_argument('-s', '--startwith', metavar='START', action='store',
                        dest='start', help=(
                            'Reinstall procedure starts from which package, sort '
                            'in initial alphabets.'
                        ))
    parser.add_argument('-e', '--endwith', metavar='START', action='store',
                        dest='end', help=(
                            'Reinstall procedure ends until which package, sort '
                            'in initial alphabets.'
                        ))
    parser.add_argument('-f', '--force', action='store_true', default=False,
                        help=(
                            'Run in force mode, using for `brew reinstall`.'
                        ))
    parser.add_argument('-q', '--quiet', action='store_true', default=False,
                        help=(
                            'Run in quiet mode, with no output information.'
                        ))
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help=(
                            'Run in verbose mode, with detailed output information.'
                        ))

    return parser


def main():
    if platform.system() != 'Darwin':
        os.system(f'echo "Script $({under})reinstall$({reset}) runs only on $({bold})$({red})macOS$({reset})."')
        sys.exit(1)

    parser = get_parser()
    args = parser.parse_args()

    pathlib.Path('/tmp/log').mkdir(parents=True, exist_ok=True)
    pathlib.Path('/Library/Logs/Scripts/reinstall').mkdir(parents=True, exist_ok=True)

    logdate = datetime.date.strftime(datetime.datetime.today(), '%y%m%d')
    logname = f'/Library/Logs/Scripts/reinstall/{logdate}.log'

    mode = '-*- Arguments -*-'.center(80, ' ')
    with open(logname, 'a') as logfile:
        logfile.write(datetime.date.strftime(datetime.datetime.today(), '%+').center(80, '—'))
        logfile.write(f'\n\nCMD: {python} {program}')
        logfile.write(f'\n\n{mode}\n\n')
        for key, value in args.__dict__.items():
            logfile.write(f'ARG: {key} = {value}\n')

    log = MODE.get(args.mode or 'all')(args, file=logname, date=logdate)
    if not args.quiet:
        os.system(f'echo "-*- $({blue})Reinstall Logs$({reset}) -*-"; echo ;')

        for mode in log:
            name = NAME.get(mode, mode)
            if log[mode] and all(log[mode]):
                pkgs = ', '.join(log[mode])
                os.system(f'echo "Reinstalled following {name} packages: $({red}){pkgs}$({reset})."; echo ;')
            else:
                os.system(f'echo "$({green})No package reinstalled in {name}.$({reset})"; echo ;')

    mode = '-*- Reinstall Logs -*-'.center(80, ' ')
    with open(logname, 'a') as logfile:
        logfile.write(f'\n\n{mode}\n\n')
        for mode in log:
            name = NAME.get(mode, mode)
            if log[mode] and all(log[mode]):
                pkgs = ', '.join(log[mode])
                logfile.write(f'LOG: Reinstalled following {name} packages: {pkgs}.\n')
            else:
                logfile.write(f'LOG: No package reinstalled in {name}.\n')
        logfile.write('\n\n\n\n')


if __name__ == '__main__':
    sys.exit(main())
