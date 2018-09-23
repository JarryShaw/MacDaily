# -*- coding: utf-8 -*-

import argparse
import base64
import contextlib
import datetime
import multiprocessing
import os
import pwd
import shutil
import signal
import subprocess
import sys
import tempfile

from macdaily.daily_config import parse
from macdaily.daily_utility import (aftermath, archive, beholder, blue, bold,
                                    green, length, make_path, make_pipe,
                                    program, python, red, reset, under)
from macdaily.libuninstall import *

# version string
__version__ = '2018.09.23'

# display mode names
NAME = dict(
    pip='Python',
    brew='Homebrew',
    cask='Caskroom',
)

# mode actions
MODE = dict(
    all=lambda *args, **kwargs: uninstall_all(*args, **kwargs),
    pip=lambda *args, **kwargs: uninstall_pip(*args, **kwargs),
    brew=lambda *args, **kwargs: uninstall_brew(*args, **kwargs),
    cask=lambda *args, **kwargs: uninstall_cask(*args, **kwargs),
)


def get_parser():
    parser = argparse.ArgumentParser(
                prog='uninstall',
                description='Package Recursive Uninstall Manager',
                usage='macdaily uninstall [-hV] [-qv] [-fiY] [-a] [--[no-]MODE] MODE ...',
                epilog='aliases: uninstall, remove, rm, r, un')
    parser.add_argument('-V', '--version', action='version', version=__version__)
    parser.add_argument('-a', '--all', action='append_const', const='all', dest='mode',
                        help='uninstall all packages installed through pip, Homebrew, and Caskroom')

    parser.add_argument('--pip', action='append_const', const='pip', dest='mode', help=argparse.SUPPRESS)
    parser.add_argument('--brew', action='append_const', const='brew', dest='mode', help=argparse.SUPPRESS)
    parser.add_argument('--cask', action='append_const', const='cask', dest='mode', help=argparse.SUPPRESS)

    parser.add_argument('--no-pip', action='store_true', default=False, help=argparse.SUPPRESS)
    parser.add_argument('--no-brew', action='store_true', default=False, help=argparse.SUPPRESS)
    parser.add_argument('--no-cask', action='store_true', default=False, help=argparse.SUPPRESS)

    subparser = parser.add_subparsers(title='mode selection', metavar='MODE', dest='mode',
                                      help=('uninstall given packages installed through a specified method, '
                                            'e.g.: pip, brew or cask'))

    parser_pip = subparser.add_parser('pip', description='Uninstall Installed Python Packages',
                                      usage='macdaily uninstall pip [-h] [-qv] [-iY] [-bcsy] [-V VER] [-a] [-p PKG]')
    parser_pip.add_argument('-a', '--all', action='store_true', default=True, dest='all',
                            help='uninstall all packages installed through pip')
    parser_pip.add_argument('-V', '--python_version', action='store', metavar='VER', dest='version',
                            choices=[0, 1, 2, 20, 21, 22, 23, 24, 25, 26, 27, 3, 30, 31, 32, 33, 34, 35, 36, 37],
                            type=int, default=0, help='indicate packages in which version of pip will be uninstalled')
    parser_pip.add_argument('-s', '--system', action='store_true', default=False, dest='system',
                            help=('uninstall pip packages on system level, '
                                  'i.e. python installed through official installer'))
    parser_pip.add_argument('-b', '--brew', action='store_true', default=False, dest='brew',
                            help='uninstall pip packages on Cellar level, i.e. python installed through Homebrew')
    parser_pip.add_argument('-c', '--cpython', action='store_true', default=False, dest='cpython',
                            help='uninstall pip packages on CPython environment')
    parser_pip.add_argument('-y', '--pypy', action='store_true', default=False, dest='pypy',
                            help='uninstall pip packages on Pypy environment')
    parser_pip.add_argument('-p', '--package', metavar='PKG', action='append', dest='package',
                            help='name of packages to be uninstalled, default is null')
    parser_pip.add_argument('-i', '--ignore-dependencies', action='store_true', default=False, dest='idep',
                            help='run in non-recursive mode, i.e. ignore dependencies of uninstalling packages')
    parser_pip.add_argument('-q', '--quiet', action='store_true', default=False,
                            help='run in quiet mode, with no output information')
    parser_pip.add_argument('-v', '--verbose', action='store_true', default=False,
                            help='run in verbose mode, with more information')
    parser_pip.add_argument('-Y', '--yes', action='store_true', default=False, dest='yes',
                            help='yes for all selections')
    parser_pip.add_argument('--show-log', action='store_true', default=False,
                            help='open log in Console upon completion of command')

    parser_brew = subparser.add_parser('brew', description='Uninstall Installed Homebrew Formulae',
                                       usage='macdaily uninstall brew [-h] [-qv] [-iY] [-f] [-a] [-p PKG]')
    parser_brew.add_argument('-a', '--all', action='store_true', default=False, dest='all',
                             help='uninstall all formulae installed through Homebrew')
    parser_brew.add_argument('-p', '--package', metavar='PKG', action='append', dest='package',
                             help='name of formulae to be uninstalled, default is null')
    parser_brew.add_argument('-f', '--force', action='store_true', default=False,
                             help='use "--force" when running `brew uninstall`')
    parser_brew.add_argument('-i', '--ignore-dependencies', action='store_true', default=False, dest='idep',
                             help='run in non-recursive mode, i.e. ignore dependencies of uninstalling formulae')
    parser_brew.add_argument('-q', '--quiet', action='store_true', default=False,
                             help='run in quiet mode, with no output information')
    parser_brew.add_argument('-v', '--verbose', action='store_true', default=False,
                             help='run in verbose mode, with more information')
    parser_brew.add_argument('-Y', '--yes', action='store_true', default=False, dest='yes',
                             help='yes for all selections')
    parser_brew.add_argument('--show-log', action='store_true', default=False,
                             help='open log in Console upon completion of command')

    parser_cask = subparser.add_parser('cask', description='Uninstall Installed Caskroom Binaries',
                                       usage='macdaily uninstall cask [-h] [-qv] [-Y] [-f] [-a] [-p PKG]')
    parser_cask.add_argument('-a', '--all', action='store_true', default=False, dest='all',
                             help='uninstall all casks installed through Caskroom')
    parser_cask.add_argument('-p', '--package', metavar='PKG', action='append', dest='package',
                             help='name of casks to be uninstalled, default is null')
    parser_cask.add_argument('-f', '--force', action='store_true', default=False,
                             help='use "--force" when running `brew cask uninstall`')
    parser_cask.add_argument('-q', '--quiet', action='store_true', default=False,
                             help='run in quiet mode, with no output information')
    parser_cask.add_argument('-v', '--verbose', action='store_true', default=False,
                             help='run in verbose mode, with more information')
    parser_cask.add_argument('-Y', '--yes', action='store_true', default=False, dest='yes',
                             help='yes for all selections')
    parser_cask.add_argument('--show-log', action='store_true', default=False,
                             help='open log in Console upon completion of command')

    parser.add_argument('-f', '--force', action='store_true', default=False,
                        help='run in force mode, only for Homebrew and Caskroom')
    parser.add_argument('-i', '--ignore-dependencies', action='store_true', default=False, dest='idep',
                        help='run in non-recursive mode, only for Python and Homebrew')
    parser.add_argument('-q', '--quiet', action='store_true', default=False,
                        help='run in quiet mode, with no output information')
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help='run in verbose mode, with more information')
    parser.add_argument('-Y', '--yes', action='store_true', default=False, dest='yes',
                        help='yes for all selections')
    parser.add_argument('--show-log', action='store_true', default=False,
                        help='open log in Console upon completion of command')

    return parser


def uninstall(argv, config, logdate, logtime, today):
    parser = get_parser()
    args = parser.parse_args(argv)

    if args.mode is None:
        parser.print_help()
        exit(1)

    tmppath, logpath, arcpath, tarpath = make_path(config, mode='uninstall', logdate=logdate)
    tmpfile = tempfile.NamedTemporaryFile(dir=tmppath, prefix='uninstall-', suffix='.log')
    logname = '{}/{}/{}.log'.format(logpath, logdate, logtime)
    tmpname = tmpfile.name

    PIPE = make_pipe(config)
    USER = config['Account']['username']
    PASS = base64.b64encode(PIPE.stdout.readline().strip()).decode()

    with open(logname, 'a') as logfile:
        logfile.write(datetime.date.strftime(today, ' %+ ').center(80, '—'))
        logfile.write('\n\nCMD: {} {}'.format(python, program))
        logfile.write("\n\n{}\n\n".format('-*- Arguments - *-'.center(80, ' ')))
        for key, value in args.__dict__.items():
            logfile.write('ARG: {} = {}\n'.format(key, value))

    if pwd.getpwuid(os.stat(logname).st_uid) != USER:
        subprocess.run(['sudo', 'chown', '-R', USER, config['Path']['tmpdir'], config['Path']['logdir']],
                       stdin=PIPE.stdout, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def reload(*args, **kwargs):
        reload_flag.value = True

    reload_flag = multiprocessing.Value('B', False)
    signal.signal(signal.SIGUSR1, reload)

    for mode in config['Mode'].keys():
        if (not config['Mode'].getboolean(mode, fallback=False)):
            setattr(args, 'no_{}'.format(mode), True)
    if isinstance(args.mode, str):
        args.mode = [args.mode]
    if 'all' in args.mode:
        args.mode = ['all']

    bash_timeout = config['Environment'].getint('bash-timeout', fallback=1000)
    sudo_timeout = str(config['Environment'].getint('sudo-timeout', fallback=300) // 2)

    for mode in set(args.mode):
        uninstall = MODE.get(mode)
        log = aftermath(logfile=logname, tmpfile=tmpname, command='uninstall')(
                uninstall)(args, file=logname, temp=tmpname, password=PASS,
                           bash_timeout=bash_timeout, sudo_timeout=sudo_timeout)

    if log != dict():
        if not args.quiet:
            print('-*- {}Uninstall Logs{} -*-'.format(blue, reset).center(length, ' '), '\n', sep='')
        mode = '-*- Uninstall Logs -*-'.center(80, ' ')
        with open(logname, 'a') as logfile:
            logfile.write('\n\n{}\n\n'.format(mode))
            for mode in log:
                name = NAME.get(mode)
                if log[mode] and all(log[mode]):
                    pkgs = ', '.format().join(log[mode])
                    comment = '' if args.idep else ' (including dependencies)'
                    logfile.write('LOG: uninstalled following {} packages: {}{}\n'.format(name, pkgs, comment))
                    if not args.quiet:
                        pkgs_coloured = '{}, {}'.format(reset, red).join(log[mode])
                        print('uninstall: {}{}{}: '
                              'uninstalled following {}{}{} packages: '
                              '{}{}{}{}'.format(green, mode, reset, bold, name, reset, red, pkgs_coloured, reset, comment))
                else:
                    logfile.write('LOG: no package uninstalled in {}\n'.format(name))
                    if not args.quiet:
                        print('uninstall: {}{}{}: no package uninstalled in {}{}{}'.format(green, mode, reset, bold, name, reset))

            filelist = archive(config, logpath, arcpath, tarpath, logdate, today)
            if filelist:
                files = ', '.join(filelist)
                logfile.write('LOG: archived following ancient logs: {}\n'.format(files))
                if not args.quiet:
                    print('uninstall: {}cleanup{}: ancient logs archived into {}{}{}'.format(green, reset, under, arcpath, reset))
            else:
                logfile.write('LOG: no ancient logs archived\n'.format())
                if not args.quiet:
                    print('uninstall: {}cleanup{}: no ancient logs archived'.format(green, reset))

            if reload_flag.value:
                proc = subprocess.run(['sudo', '--set-home', sys.executable, '-m',
                                       'pip', 'uninstall', 'macdaily', '--yes'],
                                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                      stdin=PIPE.stdout, timeout=bash_timeout)
                try:
                    proc.check_returncode()
                except subprocess.CalledProcessError:
                    if not args.quiet:
                        print('uninstall: {}macdaily{}: process failed, please try manually'.format(red, reset))
                    logfile.write('ERR: please try manually uninstall macdaily\n')
                else:
                    if not args.quiet:
                        print('uninstall: {}macdaily{}: package is now uninstalled'.format(green, reset))
                    logfile.write('LOG: macdaily is now uninstalled\n')

    with contextlib.suppress(OSError):
        tmpfile.close()
    if args.show_log:
        subprocess.run(['open', '-a', 'Console', logname], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


@beholder
def main():
    config = parse()
    argv = sys.argv[1:]
    today = datetime.datetime.today()
    logdate = datetime.date.strftime(today, '%y%m%d')
    logtime = datetime.date.strftime(today, '%H%M%S')
    uninstall(argv, config, logdate, logtime, today)


if __name__ == '__main__':
    sys.tracebacklimit = 0
    sys.exit(main())
