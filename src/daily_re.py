# -*- coding: utf-8 -*-


import argparse
import calendar
import datetime
import os
import pathlib
import platform
import shutil
import subprocess
import sys
import tarfile
import zipfile

from jsdaily.libprinstall import *


# version string
__version__ = '1.0.1'


# today
today = datetime.datetime.today()


# display mode names
NAME = dict(
    brew = 'Homebrew',
    cask = 'Caskroom',
)


# mode actions
MODE = dict(
    all = lambda *args, **kwargs: reinstall_all(*args, **kwargs),
    brew = lambda *args, **kwargs: reinstall_brew(*args, **kwargs),
    cask = lambda *args, **kwargs: reinstall_cask(*args, **kwargs),
    cleanup = lambda *args, **kwargs: reinstall_cleanup(*args, **kwargs),
)


# terminal commands
python = sys.prefix             # Python version
program = ' '.join(sys.argv)    # arguments


# terminal display
reset  = '\033[0m'      # reset
bold   = '\033[1m'      # bold
under  = '\033[4m'      # underline
red    = '\033[91m'     # bright red foreground
green  = '\033[92m'     # bright green foreground
blue   = '\033[96m'     # bright blue foreground


def get_parser():
    parser = argparse.ArgumentParser(prog='jsreinstall', description=(
                    'Homebrew Package Reinstall Manager'
                ), usage=(
                    'jsreinstall [-hV] [-qv] [-f] [-es PKG] [-a] [--[no-]MODE] MODE ... '
                ))
    parser.add_argument('-V', '--version', action='version',
                        version='{}'.format(__version__))
    parser.add_argument('-a', '--all', action='append_const', const='all',
                        dest='mode', help=(
                            'reinstall all packages installed through Homebrew '
                            'and Caskroom'
                        ))

    parser.add_argument('--brew', action='append_const', const='brew', dest='mode', help=argparse.SUPPRESS)
    parser.add_argument('--cask', action='append_const', const='cask', dest='mode', help=argparse.SUPPRESS)
    parser.add_argument('--cleanup', action='append_const', const='cleanup', dest='mode', help=argparse.SUPPRESS)

    parser.add_argument('--no-brew', action='store_true', default=False, help=argparse.SUPPRESS)
    parser.add_argument('--no-cask', action='store_true', default=False, help=argparse.SUPPRESS)
    parser.add_argument('--no-cleanup', action='store_true', default=False, help=argparse.SUPPRESS)

    subparser = parser.add_subparsers(title='mode selection', metavar='MODE',
                        dest='mode', help=(
                            'reinstall packages installed through a '
                            'specified method, e.g.: brew or cask, or '
                            'alternatively and simply, cleanup'
                        ))

    parser_brew = subparser.add_parser('brew', description=(
                            'Reinstall Homebrew Packages'
                        ), usage=(
                            'jsreinstall brew [-hV] [-qv] [-f] [-se PKG] [-a] [--[no-]MODE] MODE ... '
                        ))
    parser_brew.add_argument('-a', '--all', action='store_true', default=False,
                        dest='all', help=(
                            'reinstall all packages installed through Homebrew'
                        ))
    parser_brew.add_argument('-p', '--package', metavar='PKG', action='append',
                        dest='package', help=(
                            'name of packages to be reinstalled, default is null'
                        ))
    parser_brew.add_argument('-s', '--startwith', metavar='START', action='store',
                        dest='start', help=(
                            'reinstall procedure starts from which package, sort '
                            'in initial alphabets'
                        ))
    parser_brew.add_argument('-e', '--endwith', metavar='START', action='store',
                        dest='end', help=(
                            'reinstall procedure ends until which package, sort '
                            'in initial alphabets'
                        ))
    parser_brew.add_argument('-f', '--force', action='store_true', default=False,
                        help=(
                            'run in force mode, using for `brew reinstall`'
                        ))
    parser_brew.add_argument('-q', '--quiet', action='store_true', default=False,
                        help=(
                            'run in quiet mode, with no output information'
                        ))
    parser_brew.add_argument('-v', '--verbose', action='store_true', default=False,
                        help=(
                            'run in verbose mode, with detailed output information'
                        ))

    parser_cask = subparser.add_parser('cask', description=(
                            'Reinstall Caskroom Packages'
                        ), usage=(
                            'jsreinstall cask [-hV] [-qv] [-se PKG] [-a] [--[no-]MODE] MODE ... '
                        ))
    parser_cask.add_argument('-a', '--all', action='store_true', default=False,
                        dest='all', help=(
                            'reinstall all packages installed through Caskroom'
                        ))
    parser_cask.add_argument('-p', '--package', metavar='PKG', action='append',
                        dest='package', help=(
                            'name of packages to be reinstalled, default is null'
                        ))
    parser_cask.add_argument('-s', '--startwith', metavar='START', action='store',
                        dest='start', help=(
                            'reinstall procedure starts from which package, sort '
                            'in initial alphabets'
                        ))
    parser_cask.add_argument('-e', '--endwith', metavar='START', action='store',
                        dest='end', help=(
                            'reinstall procedure ends until which package, sort '
                            'in initial alphabets'
                        ))
    parser_cask.add_argument('-q', '--quiet', action='store_true', default=False,
                        help=(
                            'run in quiet mode, with no output information'
                        ))
    parser_cask.add_argument('-v', '--verbose', action='store_true', default=False,
                        help=(
                            'run in verbose mode, with detailed output information'
                        ))

    parser_cleanup = subparser.add_parser('cleanup', description=(
                            'Cleanup Caches & Downloads'
                        ), usage=(
                            'jsreinstall cleanup [-h] [-q] [--no-brew] [--no-cask]'
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

    parser.add_argument('-s', '--startwith', metavar='START', action='store',
                        dest='start', help=(
                            'reinstall procedure starts from which package, sort '
                            'in initial alphabets'
                        ))
    parser.add_argument('-e', '--endwith', metavar='START', action='store',
                        dest='end', help=(
                            'reinstall procedure ends until which package, sort '
                            'in initial alphabets'
                        ))
    parser.add_argument('-f', '--force', action='store_true', default=False,
                        help=(
                            'run in force mode, using for `brew reinstall`'
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


def main(argv=None):
    try:
        parser = get_parser()
        args = parser.parse_args(argv)

        if args.mode is None:
            parser.print_help()
            return

        tmpdir = '/tmp/log'
        logdir = '/Library/Logs/Scripts/reinstall'
        arcdir = '/Library/Logs/Scripts/archive/reinstall'
        tardir = '/Library/Logs/Scripts/tarfile/reinstall'

        logdate = datetime.date.strftime(today, '%y%m%d')
        logtime = datetime.date.strftime(today, '%H%M%S')
        logname = f'{logdir}/{logdate}/{logtime}.log'

        pathlib.Path(arcdir).mkdir(parents=True, exist_ok=True)
        pathlib.Path(tardir).mkdir(parents=True, exist_ok=True)
        pathlib.Path(tmpdir).mkdir(parents=True, exist_ok=True)
        pathlib.Path(f'{logdir}/{logdate}').mkdir(parents=True, exist_ok=True)

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
            reinstall = MODE.get(mode)
            log = reinstall(args, file=logname, date=logdate)

        filelist = list()
        for subdir in os.listdir(logdir):
            if subdir == '.DS_Store':
                continue
            absdir = os.path.join(logdir, subdir)
            if not os.path.isdir(absdir):
                continue
            if subdir != logdate:
                tarname = f'{arcdir}/{subdir}.tar.gz'
                with tarfile.open(tarname, 'w:gz') as tf:
                    abs_src = os.path.abspath(absdir)
                    for dirname, subdirs, files in os.walk(absdir):
                        for filename in files:
                            if filename == '.DS_Store':
                                continue
                            name, ext = os.path.splitext(filename)
                            if ext != '.log':
                                continue
                            absname = os.path.abspath(os.path.join(dirname, filename))
                            arcname = absname[len(abs_src) + 1:]
                            tf.add(absname, arcname)
                            filelist.append(arcname)
                    shutil.rmtree(absdir)

        ctime = datetime.datetime.fromtimestamp(os.stat(arcdir).st_birthtime)
        delta = today - ctime
        if delta > datetime.timedelta(7):
            arcdate = datetime.date.strftime(ctime, '%y%m%d')
            tarname = f'{tardir}/{arcdate}-{logdate}.tar.bz'
            with tarfile.open(tarname, 'w:bz2') as tf:
                abs_src = os.path.abspath(arcdir)
                for dirname, subdirs, files in os.walk(arcdir):
                    for filename in files:
                        if filename == '.DS_Store':
                            continue
                        name, ext = os.path.splitext(filename)
                        if ext != '.gz':
                            continue
                        absname = os.path.abspath(os.path.join(dirname, filename))
                        arcname = absname[len(abs_src) + 1:]
                        tf.add(absname, arcname)
                        filelist.append(arcname)
                shutil.rmtree(arcdir)

        ctime = datetime.datetime.fromtimestamp(os.stat('/Library/Logs/Scripts/tarfile').st_birthtime)
        delta = today - ctime
        if delta > datetime.timedelta(calendar.monthrange(today.year, today.month)[1]):
            arcdate = datetime.date.strftime(ctime, '%y%m%d')
            tarname = f'{tmpdir}/{arcdate}-{logdate}.tar.xz'
            with tarfile.open(tarname, 'w:xz') as tf:
                abs_src = os.path.abspath('/Library/Logs/Scripts/tarfile')
                for dirname, subdirs, files in os.walk('/Library/Logs/Scripts/tarfile'):
                    for filename in files:
                        if filename == '.DS_Store':
                            continue
                        name, ext = os.path.splitext(filename)
                        if ext != '.bz':
                            continue
                        absname = os.path.abspath(os.path.join(dirname, filename))
                        arcname = absname[len(abs_src) + 1:]
                        tf.add(absname, arcname)
                        filelist.append(arcname)
                shutil.rmtree('/Library/Logs/Scripts/tarfile')

            dskpath = pathlib.Path('/Volumes/Jarry Shaw/')
            if dskpath.exists() and dskpath.is_dir():
                arcfile = '/Volumes/Jarry Shaw/Developers/archive.zip'
                with zipfile.ZipFile(arcfile, 'a', zipfile.ZIP_DEFLATED) as zf:
                    arcname = os.path.split(tarname)[1]
                    zf.write(tarname, arcname)
                    filelist.append(arcname)
                    os.remove(tarname)

        mode = '-*- Reinstall Logs -*-'.center(80, ' ')
        with open(logname, 'a') as logfile:
            logfile.write(f'\n\n{mode}\n\n')
            if not args.quiet:
                print(f'-*- {blue}Reinstall Logs{reset} -*-\n')

            for mode in log:
                name = NAME.get(mode)
                if name is None:    continue
                if log[mode] and all(log[mode]):
                    pkgs = f', '.join(log[mode])
                    logfile.write(f'LOG: reinstalled following {name} packages: {pkgs}\n')
                    if not args.quiet:
                        pkgs_coloured = f'{reset}, {red}'.join(log[mode])
                        print(
                            f'reinstall: {green}{mode}{reset}: '
                            f'reinstalled following {bold}{name}{reset} packages: {red}{pkgs_coloured}{reset}'
                        )
                else:
                    logfile.write(f"LOG: no package reinstalled in {name}\n")
                    if not args.quiet:
                        print(f'reinstall: {green}{mode}{reset}: no package reinstalled in {bold}{name}{reset}')

            if filelist:
                files = ', '.join(filelist)
                logfile.write(f'LOG: archived following old logs: {files}\n')
                if not args.quiet:
                    print(f'reinstall: {green}cleanup{reset}: ancient logs archived into {under}{arcdir}{reset}')
    except KeyboardInterrupt, PermissionError:
        logdate = datetime.date.strftime(today, '%y%m%d')
        logtime = datetime.date.strftime(today, '%H%M%S')
        subprocess.run(['bash', 'libprinstall/aftermath.sh', logdate, logtime, 'reinstall', 'true'])


if __name__ == '__main__':
    sys.exit(main())
