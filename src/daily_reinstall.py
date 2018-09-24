# -*- coding: utf-8 -*-

import argparse
import base64
import contextlib
import datetime
import os
import pwd
import shutil
import subprocess
import sys
import tempfile

from macdaily.daily_config import parse
from macdaily.daily_utility import (aftermath, archive, beholder, blue, bold,
                                    green, length, make_path, make_pipe,
                                    program, python, red, reset, under)
from macdaily.libprinstall import *

# version string
__version__ = '2018.09.24'

# display mode names
NAME = dict(
    brew='Homebrew',
    cask='Caskroom',
)

# mode actions
MODE = dict(
    all=lambda *args, **kwargs: reinstall_all(*args, **kwargs),
    brew=lambda *args, **kwargs: reinstall_brew(*args, **kwargs),
    cask=lambda *args, **kwargs: reinstall_cask(*args, **kwargs),
    cleanup=lambda *args, **kwargs: reinstall_cleanup(*args, **kwargs),
)


def get_parser():
    parser = argparse.ArgumentParser(
                prog='reinstall',
                description='Homebrew Package Reinstall Manager',
                usage='macdaily reinstall [-hV] [-qv] [-f] [-es PKG] [-a] [--[no-]MODE] MODE ...',
                epilog='aliases: reinstall, re')
    parser.add_argument('-V', '--version', action='version', version=__version__)
    parser.add_argument('-a', '--all', action='append_const', const='all', dest='mode',
                        help='reinstall all packages installed through Homebrew and Caskroom')

    parser.add_argument('--brew', action='append_const', const='brew', dest='mode', help=argparse.SUPPRESS)
    parser.add_argument('--cask', action='append_const', const='cask', dest='mode', help=argparse.SUPPRESS)
    parser.add_argument('--cleanup', action='append_const', const='cleanup', dest='mode', help=argparse.SUPPRESS)

    parser.add_argument('--no-brew', action='store_true', default=False, help=argparse.SUPPRESS)
    parser.add_argument('--no-cask', action='store_true', default=False, help=argparse.SUPPRESS)
    parser.add_argument('--no-cleanup', action='store_true', default=False, help=argparse.SUPPRESS)

    subparser = parser.add_subparsers(title='mode selection', metavar='MODE', dest='mode',
                                      help=('reinstall packages installed through a specified method, '
                                            'e.g.: brew or cask, or alternatively and simply, cleanup'))

    parser_brew = subparser.add_parser('brew', description='Reinstall Homebrew Packages',
                                       usage=('macdaily reinstall brew '
                                              '[-hV] [-qv] [-f] [-se PKG] [-a] [--[no-]MODE] MODE ...'))
    parser_brew.add_argument('-a', '--all', action='store_true', default=False, dest='all',
                             help='reinstall all packages installed through Homebrew')
    parser_brew.add_argument('-p', '--package', metavar='PKG', action='append', dest='package',
                             help='name of packages to be reinstalled, default is null')
    parser_brew.add_argument('-s', '--startswith', metavar='START', action='store', dest='start',
                             help='reinstall procedure starts from which package, sort in initial alphabets')
    parser_brew.add_argument('-e', '--endswith', metavar='START', action='store', dest='end',
                             help='reinstall procedure ends until which package, sort in initial alphabets')
    parser_brew.add_argument('-f', '--force', action='store_true', default=False,
                             help='run in force mode, using for `brew reinstall`')
    parser_brew.add_argument('-q', '--quiet', action='store_true', default=False,
                             help='run in quiet mode, with no output information')
    parser_brew.add_argument('-v', '--verbose', action='store_true', default=False,
                             help='run in verbose mode, with detailed output information')
    parser_brew.add_argument('--show-log', action='store_true', default=False,
                             help='open log in Console upon completion of command')

    parser_cask = subparser.add_parser('cask', description='Reinstall Caskroom Packages',
                                       usage=('macdaily reinstall cask '
                                              '[-hV] [-qv] [-se PKG] [-a] [--[no-]MODE] MODE ... '))
    parser_cask.add_argument('-a', '--all', action='store_true', default=False, dest='all',
                             help='reinstall all packages installed through Caskroom')
    parser_cask.add_argument('-p', '--package', metavar='PKG', action='append', dest='package',
                             help='name of packages to be reinstalled, default is null')
    parser_cask.add_argument('-s', '--startswith', metavar='START', action='store', dest='start',
                             help='reinstall procedure starts from which package, sort in initial alphabets')
    parser_cask.add_argument('-e', '--endswith', metavar='START', action='store', dest='end',
                             help='reinstall procedure ends until which package, sort in initial alphabets')
    parser_cask.add_argument('-q', '--quiet', action='store_true', default=False,
                             help='run in quiet mode, with no output information')
    parser_cask.add_argument('-v', '--verbose', action='store_true', default=False,
                             help='run in verbose mode, with detailed output information')
    parser_cask.add_argument('--show-log', action='store_true', default=False,
                             help='open log in Console upon completion of command')

    parser_cleanup = subparser.add_parser('cleanup', description='Cleanup Caches & Downloads',
                                          usage='macdaily reinstall cleanup [-h] [-q] [--no-brew] [--no-cask]')
    parser_cleanup.add_argument('--no-brew', dest='brew', action='store_false', default=True,
                                help='do not remove Homebrew caches & downloads')
    parser_cleanup.add_argument('--no-cask', dest='cask', action='store_false', default=True,
                                help='do not remove Caskroom caches & downloads')
    parser_cleanup.add_argument('-q', '--quiet', action='store_true', default=False,
                                help='run in quiet mode, with no output information')
    parser_cleanup.add_argument('--show-log', action='store_true', default=False,
                                help='open log in Console upon completion of command')

    parser.add_argument('-s', '--startswith', metavar='START', action='store', dest='start',
                        help='reinstall procedure starts from which package, sort in initial alphabets')
    parser.add_argument('-e', '--endswith', metavar='START', action='store', dest='end',
                        help='reinstall procedure ends until which package, sort in initial alphabets')
    parser.add_argument('-f', '--force', action='store_true', default=False,
                        help='run in force mode, using for `brew reinstall`')
    parser.add_argument('-q', '--quiet', action='store_true', default=False,
                        help='run in quiet mode, with no output information')
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help='run in verbose mode, with detailed output information')
    parser.add_argument('--show-log', action='store_true', default=False,
                        help='open log in Console upon completion of command')

    return parser


def reinstall(argv, config, logdate, logtime, today):
    parser = get_parser()
    args = parser.parse_args(argv)

    if args.mode is None:
        parser.print_help()
        exit(1)

    tmppath, logpath, arcpath, tarpath = make_path(config, mode='reinstall', logdate=logdate)
    tmpfile = tempfile.NamedTemporaryFile(dir=tmppath, prefix='reinstall-', suffix='.log')
    logname = os.path.join(logpath, logdate, '{}.log'.format(logtime))
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

    for mode in config['Mode'].keys():
        if (not config['Mode'].getboolean(mode, fallback=False)):
            setattr(args, 'no_{}'.format(mode), True)
    if isinstance(args.mode, str):
        args.mode = [args.mode]
    if 'all' in args.mode:
        args.mode = ['all']

    arcdir = config['Path']['arcdir']
    bash_timeout = config['Environment'].getint('bash-timeout', fallback=1000)
    sudo_timeout = str(config['Environment'].getint('sudo-timeout', fallback=300) // 2)

    for mode in set(args.mode):
        reinstall = MODE.get(mode)
        log = aftermath(logfile=logname, tmpfile=tmpname, command='prinstall', logmode='reinstall')(
                reinstall)(args, file=logname, temp=tmpname, disk=arcdir, password=PASS,
                           bash_timeout=bash_timeout, sudo_timeout=sudo_timeout)

    if log != dict():
        if not args.quiet:
            print('-*- {}Reinstall Logs{} -*-'.format(blue, reset).center(length, ' '), '\n', sep='')
        mode = '-*- Reinstall Logs -*-'.center(80, ' ')
        with open(logname, 'a') as logfile:
            logfile.write('\n\n{}\n\n'.format(mode))
            for mode in log:
                name = NAME.get(mode)
                if log[mode] and all(log[mode]):
                    pkgs = ', '.format().join(log[mode])
                    logfile.write('LOG: reinstalled following {} packages: {}\n'.format(name, pkgs))
                    if not args.quiet:
                        pkgs_coloured = '{}, {}'.format(reset, red).join(log[mode])
                        print('reinstall: {}{}{}: '
                              'reinstalled following {}{}{} packages: {}{}{}'.format(green, mode, reset, bold, name, reset, red, pkgs_coloured, reset))
                else:
                    logfile.write("LOG: no package reinstalled in {}\n".format(name))
                    if not args.quiet:
                        print('reinstall: {}{}{}: no package reinstalled in {}{}{}'.format(green, mode, reset, bold, name, reset))

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

    with contextlib.suppress(OSError):
        tmpfile.close()
    if args.show_log:
        subprocess.run(['open', '-a', 'Console', logname], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


@beholder
def main():
    config = parse()
    argv = sys.argv[1:]
    today = datetime.datetime.today()
    logdate = datetime.date.strftime(today, r'%y%m%d')
    logtime = datetime.date.strftime(today, r'%H%M%S')
    reinstall(argv, config, logdate, logtime, today)


if __name__ == '__main__':
    sys.exit(main())
