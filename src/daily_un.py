# -*- coding: utf-8 -*-


import argparse
import calendar
import datetime
import os
import pathlib
import platform
import shlex
import shutil
import subprocess
import sys
import tarfile
import zipfile


from jsdaily.libuninstall import *


# version string
__version__ = '1.1.0'


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
reset  = '\033[0m'      # reset
bold   = '\033[1m'      # bold
under  = '\033[4m'      # underline
red    = '\033[91m'     # bright red foreground
green  = '\033[92m'     # bright green foreground
blue   = '\033[96m'     # bright blue foreground


def get_parser():
    parser = argparse.ArgumentParser(prog='uninstall', description=(
                    'Package Recursive Uninstall Manager'
                ), usage=(
                    'jsdaily uninstall [-hV] [-qv] [-fiY] [-a] [--[no-]MODE] MODE ... '
                ), epilog=(
                    'aliases: uninstall, remove, rm, r, un'
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
                            'jsdaily uninstall pip [-h] [-qv] [-iY] [-bcsy] [-V VER] [-a] [-p PKG]'
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
                            'run in non-recursive mode, i.e. ignore dependencies '
                            'of uninstalling packages'
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
                            'jsdaily uninstall brew [-h] [-qv] [-iY] [-f] [-a] [-p PKG]'
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
                            'run in non-recursive mode, i.e. ignore dependencies '
                            'of uninstalling packages'
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
                            'jsdaily uninstall cask [-h] [-qv] [-Y] [-f] [-a] [-p PKG]'
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
                            'run in non-recursive mode, only for Python and Homebrew'
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


def main(argv, config):
    try:
        parser = get_parser()
        args = parser.parse_args(argv)

        if args.mode is None:
            parser.print_help()
            return

        tmpdir = config['Path']['tmpdir']
        logdir = config['Path']['logdir'] + '/uninstall'
        arcdir = config['Path']['logdir'] + '/archive/uninstall'
        tardir = config['Path']['logdir'] + '/tarfile/uninstall'

        logdate = datetime.date.strftime(today, '%y%m%d')
        logtime = datetime.date.strftime(today, '%H%M%S')
        logname = f'{logdir}/{logdate}/{logtime}.log'
        tmpname = f'{tmpdir}/uninstall.log'

        pathlib.Path(arcdir).mkdir(parents=True, exist_ok=True)
        pathlib.Path(tardir).mkdir(parents=True, exist_ok=True)
        pathlib.Path(tmpdir).mkdir(parents=True, exist_ok=True)
        pathlib.Path(f'{logdir}/{logdate}').mkdir(parents=True, exist_ok=True)

        dskpath = pathlib.Path(config['Path']['dskdir'])
        if dskpath.exists() and dskpath.is_dir():
            pathlib.Path(config['Path']['arcdir']).mkdir(parents=True, exist_ok=True)

        mode = '-*- Arguments -*-'.center(80, ' ')
        with open(logname, 'a') as logfile:
            logfile.write(datetime.date.strftime(today, ' %+ ').center(80, '—'))
            logfile.write(f'\n\nCMD: {python} {program}')
            logfile.write(f'\n\n{mode}\n\n')
            for key, value in args.__dict__.items():
                logfile.write(f'ARG: {key} = {value}\n')

        for mode in config['Mode'].keys():
            flag = not config['Mode'].getboolean(mode)
            if flag:
                args.__setattr__(f'no_{mode}', flag)
        if isinstance(args.mode, str):
            args.mode = [args.mode]
        if 'all' in args.mode:
            args.mode = ['all']
        for mode in set(args.mode):
            uninstall = MODE.get(mode)
            log = uninstall(args, file=logname, temp=tmpname)

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

        if dskpath.exists() and dskpath.is_dir():
            ctime = datetime.datetime.fromtimestamp(os.stat(config['Path']['logdir'] + '/tarfile').st_birthtime)
            delta = today - ctime
            if delta > datetime.timedelta(calendar.monthrange(today.year, today.month)[1]):
                arcdate = datetime.date.strftime(ctime, '%y%m%d')
                tarname = f'{tmpdir}/{arcdate}-{logdate}.tar.xz'
                with tarfile.open(tarname, 'w:xz') as tf:
                    abs_src = os.path.abspath(config['Path']['logdir'] + '/tarfile')
                    for dirname, subdirs, files in os.walk(config['Path']['logdir'] + '/tarfile'):
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
                    shutil.rmtree(config['Path']['logdir'] + '/tarfile')

                arcfile = config['Path']['arcdir'] + '/archive.zip'
                with zipfile.ZipFile(arcfile, 'a', zipfile.ZIP_DEFLATED) as zf:
                    arcname = os.path.split(tarname)[1]
                    zf.write(tarname, arcname)
                    filelist.append(arcname)
                    os.remove(tarname)

        mode = '-*- Uninstall Logs -*-'.center(80, ' ')
        with open(logname, 'a') as logfile:
            logfile.write(f'\n\n{mode}\n\n')
            if not args.quiet:
                print(f'-*- {blue}Uninstall Logs{reset} -*-\n')

            for mode in log:
                name = NAME.get(mode)
                if name is None:    continue
                if log[mode] and all(log[mode]):
                    pkgs = f', '.join(log[mode])
                    comment = '' if args.idep else ' (including dependencies)'
                    logfile.write(f'LOG: uninstalled following {name} packages: {pkgs}{comment}\n')
                    if not args.quiet:
                        pkgs_coloured = f'{reset}, {red}'.join(log[mode])
                        print(
                            f'uninstall: {green}{mode}{reset}: '
                            f'uninstalled following {bold}{name}{reset} packages: {red}{pkgs_coloured}{reset}{comment}'
                        )
                else:
                    logfile.write(f'LOG: no package uninstalled in {name}\n')
                    if not args.quiet:
                        print(f'uninstall: {green}{mode}{reset}: no package uninstalled in {bold}{name}{reset}')

            if filelist:
                files = ', '.join(filelist)
                logfile.write(f'LOG: archived following old logs: {files}\n')
                if not args.quiet:
                    print(f'uninstall: {green}cleanup{reset}: ancient logs archived into {under}{arcdir}{reset}')
    except (KeyboardInterrupt, PermissionError):
        logdate = datetime.date.strftime(today, '%y%m%d')
        logtime = datetime.date.strftime(today, '%H%M%S')
        logfile = shlex.quote(config['Path']['logdir'] + f'/uninstall/{logdate}/{logtime}.log')
        tmpfile = shlex.quote(config['Path']['tmpdir'] + '/uninstall.log')
        subprocess.run(['bash', 'libuninstall/aftermath.sh', logfile, tmpfile, 'true'])


if __name__ == '__main__':
    sys.exit(main())
