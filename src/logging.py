#!/usr/bin/python3
# -*- coding: utf-8 -*-


import argparse
import datetime
import os
import pathlib
import platform
import sys
import zipfile


from jsdaily.liblogging import *


# version string
__version__ = '0.4.1'


# mode actions
MODE = dict(
    apm = lambda *args, **kwargs: logging_apm(*args, **kwargs),
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
bold = 'tput bold'      # bold
under = 'tput smul'     # underline
reset = 'tput sgr0'     # reset


def get_parser():
    parser = argparse.ArgumentParser(prog='logging', description=(
        'Application and Package Logging Manager'
    ))
    parser.add_argument('-V', '--version', action='version',
                        version='{}'.format(__version__))
    parser.add_argument('mode', action='store', metavar='MODE', nargs='*',
                        type=str, help=(
                            'The name of logging mode, could be any from '
                            'followings, apm, pip, brew, cask, dotapps, '
                            'macapps, or appstore.'
                        ))
    parser.add_argument('-a', '--all', action='store_true', default=False,
                        dest='all', help=(
                            'Log applications and packages of all entries.'
                        ))
    parser.add_argument('-v', '--pyver', action='store', metavar='VER',
                        choices=[
                            1, 2, 20, 21, 22, 23, 24, 25, 26, 27,
                            3, 30, 31, 32, 33, 34, 35, 36, 37,
                        ], dest='version', type=int, default=1, help=(
                            'Indicate which version of pip will be logged.'
                        ))
    parser.add_argument('-s', '--system', action='store_true', default=False,
                        dest='system', help=(
                            'Log pip packages on system level, i.e. python '
                            'installed through official installer.'
                        ))
    parser.add_argument('-b', '--brew', action='store_true', default=False,
                        dest='brew', help=(
                            'Log pip packages on Cellar level, i.e. python '
                            'installed through Homebrew.'
                        ))
    parser.add_argument('-c', '--cpython', action='store_true', default=False,
                        dest='cpython', help=(
                            'Log pip packages on CPython environment.'
                        ))
    parser.add_argument('-y', '--pypy', action='store_true', default=False,
                        dest='pypy', help=(
                            'Log pip packages on PyPy environment.'
                        ))
    parser.add_argument('-q', '--quiet', action='store_true', default=False,
                        help=(
                            'Run in quiet mode, with no output information.'
                        ))
    return parser


def main():
    if platform.system() != 'Darwin':
        os.system(f'echo "Script $({under})logging$({reset}) runs only on $({bold})$({red})macOS$({reset})."')
        sys.exit(1)

    parser = get_parser()
    args = parser.parse_args()

    if args.all:
        modes = ['apm', 'pip', 'brew', 'cask', 'macapp', 'appstore', 'dotapp']
    else:
        modes = args.mode

    for logmode in modes:
        logging = MODE.get(logmode)
        if logging is None:
            parser.print_usage()
            print(f"logging: error: argument MODE: invalid choice: '{logmode}'", end=' ')
            print("(choose from 'apm', 'pip', 'brew', 'cask', 'dotapp', 'macapp', 'appstore')")
            continue

        pathlib.Path(f'/Library/Logs/Scripts/logging/{logmode}').mkdir(parents=True, exist_ok=True)
        logdate = datetime.date.strftime(datetime.datetime.today(), '%y%m%d')
        logname = f'/Library/Logs/Scripts/logging/{logmode}/{logdate}.log'

        with open(logname, 'a') as logfile:
            logfile.write(datetime.date.strftime(datetime.datetime.today(), '%+').center(80, '—'))
            logfile.write(f'\n\n\nCMD: {python} {program}\n\n\n')
            for key, value in args.__dict__.items():
                logfile.write(f'ARG: {key} = {value}\n')
            logfile.write('\n\n')

        log = logging(args, file=logname)

        filelist = list()
        with zipfile.ZipFile('/Library/Logs/Scripts/archive.zip', 'a', zipfile.ZIP_DEFLATED) as zf:
            abs_src = os.path.abspath('/Library/Logs/Scripts')
            for dirname, subdirs, files in os.walk(f'/Library/Logs/Scripts/logging/{logmode}'):
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

        with open(logname, 'a') as logfile:
            if filelist:
                files = ', '.join(filelist)
                logfile.write(f'LOG: Archived following old logs: {files}\n')
            logfile.write('\n\n\n\n')


if __name__ == '__main__':
    sys.exit(main())
