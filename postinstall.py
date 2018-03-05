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
    parser = argparse.ArgumentParser(prog='postinstall', description=(
        'Homebrew Package Postinstall Manager'
    ))
    parser.add_argument('-V', '--version', action='version',
                        version='{}'.format(__version__))
    parser.add_argument('-a', '--all', action='store_true', default=True,
                        dest='all', help=(
                            'Postinstall all packages installed through Homebrew.'
                        ))
    parser.add_argument('-p', '--package', metavar='PKG', action='append',
                        dest='package', help=(
                            'Name of packages to be postinstalled, default is all.'
                        ))
    parser.add_argument('-s', '--startwith', metavar='START', action='store',
                        dest='start', help=(
                            'Postinstall procedure starts from which package, sort '
                            'in initial alphabets.'
                        ))
    parser.add_argument('-e', '--endwith', metavar='START', action='store',
                        dest='end', help=(
                            'Postinstall procedure ends until which package, sort '
                            'in initial alphabets.'
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
        os.system(f'echo "Script $({under})postinstall$({reset}) runs only on $({bold})$({red})macOS$({reset})."')
        sys.exit(1)

    parser = get_parser()
    args = parser.parse_args()

    pathlib.Path('/tmp/log').mkdir(parents=True, exist_ok=True)
    pathlib.Path('/Library/Logs/Scripts/postinstall').mkdir(parents=True, exist_ok=True)

    logdate = datetime.date.strftime(datetime.datetime.today(), '%y%m%d')
    logname = f'/Library/Logs/Scripts/postinstall/{logdate}.log'

    mode = '-*- Arguments -*-'.center(80, ' ')
    with open(logname, 'a') as logfile:
        logfile.write(datetime.date.strftime(datetime.datetime.today(), '%+').center(80, '—'))
        logfile.write(f'\n\nCMD: {python} {program}')
        logfile.write(f'\n\n{mode}\n\n')
        for key, value in args.__dict__.items():
            logfile.write(f'ARG: {key} = {value}\n')

    log = libprinstall.postinstall(args, file=logname, date=logdate)
    if not args.quiet:
        os.system(f'echo "-*- $({blue})Postinstall Logs$({reset}) -*-"; echo ;')

        if log and all(log):
            pkgs = ', '.join(log)
            os.system(f'echo "Postinstalled following Homebrew packages: $({red}){pkgs}$({reset})."; echo ;')
        else:
            os.system(f'echo "$({green})No package postinstalled in Homebrew.$({reset})"; echo ;')

    mode = '-*- Postinstall Logs -*-'.center(80, ' ')
    with open(logname, 'a') as logfile:
        logfile.write(f'\n\n{mode}\n\n')
        if log and all(log):
            pkgs = ', '.join(log)
            logfile.write(f'LOG: Postinstalled following Homebrew packages: {pkgs}.\n')
        else:
            logfile.write(f'LOG: No package postinstalled in Homebrew.\n')
        logfile.write('\n\n\n\n')


if __name__ == '__main__':
    sys.exit(main())
