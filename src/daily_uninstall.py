# -*- coding: utf-8 -*-


import argparse
import base64
import datetime
import multiprocessing
import os
import pwd
import shutil
import signal
import subprocess
import sys
import tempfile

from macdaily.daily_config import *
from macdaily.daily_utility import *
from macdaily.libuninstall import *


# version string
__version__ = '2018.09.12'


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
python = sys.executable         # Python version
program = ' '.join(sys.argv)    # arguments


# terminal display
reset  = '\033[0m'      # reset
bold   = '\033[1m'      # bold
under  = '\033[4m'      # underline
red    = '\033[91m'     # bright red foreground
green  = '\033[92m'     # bright green foreground
blue   = '\033[96m'     # bright blue foreground
length = shutil.get_terminal_size().columns
                        # terminal length


def get_parser():
    parser = argparse.ArgumentParser(prog='uninstall', description=(
                    'Package Recursive Uninstall Manager'
                ), usage=(
                    'macdaily uninstall [-hV] [-qv] [-fiY] [-a] [--[no-]MODE] MODE ... '
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
                            'macdaily uninstall pip [-h] [-qv] [-iY] [-bcsy] [-V VER] [-a] [-p PKG]'
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
    parser_pip.add_argument('--show-log', action='store_true', default=False,
                        help=(
                            'open log in Console upon completion of command'
                        ))

    parser_brew = subparser.add_parser('brew', description=(
                            'Uninstall Installed Homebrew Packages'
                        ), usage=(
                            'macdaily uninstall brew [-h] [-qv] [-iY] [-f] [-a] [-p PKG]'
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
    parser_brew.add_argument('--show-log', action='store_true', default=False,
                        help=(
                            'open log in Console upon completion of command'
                        ))

    parser_cask = subparser.add_parser('cask', description=(
                            'Uninstall Installed Caskroom Packages'
                        ), usage=(
                            'macdaily uninstall cask [-h] [-qv] [-Y] [-f] [-a] [-p PKG]'
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
    parser_cask.add_argument('--show-log', action='store_true', default=False,
                        help=(
                            'open log in Console upon completion of command'
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
    parser.add_argument('--show-log', action='store_true', default=False,
                        help=(
                            'open log in Console upon completion of command'
                        ))

    return parser


def uninstall(argv, config, *, logdate, logtime, today):
    parser = get_parser()
    args = parser.parse_args(argv)

    if args.mode is None:
        parser.print_help()
        return

    tmppath, logpath, arcpath, tarpath = make_path(config, mode='uninstall', logdate=logdate)
    tmpfile = tempfile.NamedTemporaryFile(dir=tmppath, prefix='uninstall@', suffix='.log')
    logname = f'{logpath}/{logdate}/{logtime}.log'
    tmpname = tmpfile.name

    PIPE = make_pipe(config)
    USER = config['Account']['username']
    PASS = base64.b64encode(PIPE.stdout.readline().strip()).decode()

    mode = '-*- Arguments -*-'.center(80, ' ')
    with open(logname, 'a') as logfile:
        logfile.write(datetime.date.strftime(today, ' %+ ').center(80, '—'))
        logfile.write(f'\n\nCMD: {python} {program}')
        logfile.write(f'\n\n{mode}\n\n')
        for key, value in args.__dict__.items():
            logfile.write(f'ARG: {key} = {value}\n')

    if pwd.getpwuid(os.stat(logname).st_uid) != USER:
        subprocess.run(['sudo', 'chown', '-R', USER, config['Path']['tmpdir'], config['Path']['logdir']],
                       stdin=PIPE.stdout, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    reload_flag = multiprocessing.Value('B', False)
    def reload(*args, **kwargs):
        reload_flag.value = True
    signal.signal(signal.SIGUSR1, reload)

    for mode in config['Mode'].keys():
        try:
            flag = not config['Mode'].getboolean(mode, fallback=False)
        except ValueError as error:
            sys.tracebacklimit = 0
            raise error from None
        if flag:    setattr(args, f'no_{mode}', flag)
    if isinstance(args.mode, str):
        args.mode = [args.mode]
    if 'all' in args.mode:
        args.mode = ['all']

    bash_timeout = config['Environment'].getint('bash-timeout', fallback=1_000)
    sudo_timeout = str(config['Environment'].getint('sudo-timeout', fallback=300) // 2)

    for mode in set(args.mode):
        uninstall = MODE.get(mode)
        log = aftermath(logfile=logname, tmpfile=tmpname, command='uninstall')(
                uninstall)(args, file=logname, temp=tmpname, password=PASS, bash_timeout=bash_timeout, sudo_timeout=sudo_timeout)

    if log != dict():
        if not args.quiet:
            print(f'-*- {blue}Uninstall Logs{reset} -*-'.center(length, ' '), '\n', sep='')
        mode = '-*- Uninstall Logs -*-'.center(80, ' ')
        with open(logname, 'a') as logfile:
            logfile.write(f'\n\n{mode}\n\n')

            for mode in log:
                name = NAME.get(mode)
                if name is None:    continue
                if log[mode] and all(log[mode]):
                    pkgs = f', '.join(log[mode])
                    comment = '' if args.idep else ' (including dependencies)'
                    logfile.write(f'LOG: uninstalled following {name} packages: {pkgs}{comment}\n')
                    if not args.quiet:
                        pkgs_coloured = f'{reset}, {red}'.join(log[mode])
                        print(f'uninstall: {green}{mode}{reset}: '
                              f'uninstalled following {bold}{name}{reset} packages: {red}{pkgs_coloured}{reset}{comment}')
                else:
                    logfile.write(f'LOG: no package uninstalled in {name}\n')
                    if not args.quiet:
                        print(f'uninstall: {green}{mode}{reset}: no package uninstalled in {bold}{name}{reset}')

            filelist = archive(config, logpath=logpath, arcpath=arcpath, tarpath=tarpath, logdate=logdate, today=today)
            if filelist:
                files = ', '.join(filelist)
                logfile.write(f'LOG: archived following ancient logs: {files}\n')
                if not args.quiet:
                    print(f'uninstall: {green}cleanup{reset}: ancient logs archived into {under}{arcpath}{reset}')
            else:
                logfile.write(f'LOG: no ancient logs archived\n')
                if not args.quiet:
                    print(f'uninstall: {green}cleanup{reset}: no ancient logs archived')

            if reload_flag.value:
                proc = subprocess.run(['sudo', '--set-home', sys.executable, '-m', 'pip', 'uninstall', 'macdaily', '--yes'],
                                      stdin=PIPE.stdout, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=bash_timeout)
                if proc.returncode == 0:
                    if not args.quiet:
                        print(f'uninstall: {green}macdaily{reset}: package is now uninstalled')
                    logfile.write('LOG: macdaily is now uninstalled\n')
                else:
                    if not args.quiet:
                        print(f'uninstall: {red}macdaily{reset}: process failed, please try manually')
                    logfile.write('ERR: please try manually uninstall macdaily\n')

    try:    tmpfile.close()
    except: pass
    if args.show_log:
        subprocess.run(['open', '-a', 'Console', logname], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


@beholder
def main():
    config = parse()
    argv = sys.argv[1:]
    today = datetime.datetime.today()
    logdate = datetime.date.strftime(today, '%y%m%d')
    logtime = datetime.date.strftime(today, '%H%M%S')
    uninstall(argv, config, logdate=logdate, logtime=logtime, today=today)


if __name__ == '__main__':
    sys.exit(main())
