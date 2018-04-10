# -*- coding: utf-8 -*-


import argparse
import datetime
import liblogging
import os
import pathlib
import platform
import sys
import tarfile
import zipfile


# version string
__version__ = '0.5.1'


# today
today = datetime.datetime.today()


# mode actions
MODE = dict(
    apm = lambda *args, **kwargs: liblogging.logging_apm(*args, **kwargs),
    pip = lambda *args, **kwargs: liblogging.logging_pip(*args, **kwargs),
    brew = lambda *args, **kwargs: liblogging.logging_brew(*args, **kwargs),
    cask = lambda *args, **kwargs: liblogging.logging_cask(*args, **kwargs),
    dotapp = lambda *args, **kwargs: liblogging.logging_dotapp(*args, **kwargs),
    macapp = lambda *args, **kwargs: liblogging.logging_macapp(*args, **kwargs),
    appstore = lambda *args, **kwargs: liblogging.logging_appstore(*args, **kwargs),
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
        'Application & Package Logging Manager'
    ))
    parser.add_argument('-V', '--version', action='version', version=__version__)
    parser.add_argument('-a', '--all', action='store_true', dest='all', default=False,
                        help=(
                            'log applications and packages of all entries'
                        ))

    parser.add_argument('--apm', action='append_const', const='apm', dest='mode', help=argparse.SUPPRESS)
    parser.add_argument('--pip', action='append_const', const='pip', dest='mode', help=argparse.SUPPRESS)
    parser.add_argument('--brew', action='append_const', const='brew', dest='mode', help=argparse.SUPPRESS)
    parser.add_argument('--cask', action='append_const', const='cask', dest='mode', help=argparse.SUPPRESS)
    parser.add_argument('--dotapp', action='append_const', const='dotapp', dest='mode', help=argparse.SUPPRESS)
    parser.add_argument('--macapp', action='append_const', const='macapp', dest='mode', help=argparse.SUPPRESS)
    parser.add_argument('--appstore', action='append_const', const='appstore', dest='mode', help=argparse.SUPPRESS)

    parser.add_argument('--no-apm', action='store_true', default=False, help=argparse.SUPPRESS)
    parser.add_argument('--no-pip', action='store_true', default=False, help=argparse.SUPPRESS)
    parser.add_argument('--no-brew', action='store_true', default=False, help=argparse.SUPPRESS)
    parser.add_argument('--no-cask', action='store_true', default=False, help=argparse.SUPPRESS)
    parser.add_argument('--no-dotapp', action='store_true', default=False, help=argparse.SUPPRESS)
    parser.add_argument('--no-macapp', action='store_true', default=False, help=argparse.SUPPRESS)
    parser.add_argument('--no-appstore', action='store_true', default=False, help=argparse.SUPPRESS)

    parser.add_argument('mode', action='append', metavar='MODE', nargs='*',
                        choices=[
                            [], 'apm', 'pip', 'brew', 'cask',
                            'dotapp', 'macapp', 'appstore',
                        ], help=(
                            'name of logging mode, could be any from '
                            'followings, apm, pip, brew, cask, dotapp, '
                            'macapp, or appstore'
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


def main(argv=None):
    parser = get_parser()
    args = parser.parse_args(argv)

    if args.mode is None:
        parser.print_help()
        return

    print(args)
    return

    modes = list()
    for mode in args.mode:
        if isinstance(mode, list):
            modes += mode
        else:
            modeds.append(mode)
    if args.all:
        modes += ['apm', 'pip', 'brew', 'cask', 'dotapp', 'macapp', 'appstore']

    arcflag = False
    arcfile = '/Library/Logs/Scripts/archive.zip'
    for logmode in set(modes):
        pathlib.Path(f'/Library/Logs/Scripts/logging/{logmode}').mkdir(parents=True, exist_ok=True)
        logdate = datetime.date.strftime(today, '%y%m%d')
        logname = f'/Library/Logs/Scripts/logging/{logmode}/{logdate}.log'

        with open(logname, 'a') as logfile:
            logfile.write(datetime.date.strftime(today, '%+').center(80, '—'))
            logfile.write(f'\n\n\nCMD: {python} {program}\n\n\n')
            for key, value in args.__dict__.items():
                logfile.write(f'ARG: {key} = {value}\n')
            logfile.write('\n\n')

        logging = MODE.get(logmode)
        log = logging(args, file=logname, date=logdate)

        filelist = list()
        with zipfile.ZipFile(arcfile, 'a', zipfile.ZIP_DEFLATED) as zf:
            abs_src = os.path.abspath('/Library/Logs/Scripts')
            for dirname, subdirs, files in os.walk(f'/Library/Logs/Scripts/logging/{logmode}'):
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

        with open(logname, 'a') as logfile:
            if filelist:
                arcflag = True
                files = ', '.join(filelist)
                logfile.write(f'LOG: Archived following old logs: {files}\n')
            logfile.write('\n\n\n\n')

    if arcflag and not args.quiet:
        os.system(f'echo "logging: $({green})cleanup$({reset}): '
                  f'ancient logs archived into $({under}){arcfile}$({reset})"')


if __name__ == '__main__':
    sys.exit(main())
