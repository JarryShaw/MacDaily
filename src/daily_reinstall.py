# -*- coding: utf-8 -*-


import argparse
import datetime
import getpass
import os
import pwd
import subprocess
import sys

from macdaily.daily_utility import *
from macdaily.libprinstall import *


# version string
__version__ = '2018.08.29'


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
python = sys.executable         # Python version
program = ' '.join(sys.argv)    # arguments


# terminal display
reset  = '\033[0m'      # reset
bold   = '\033[1m'      # bold
under  = '\033[4m'      # underline
red    = '\033[91m'     # bright red foreground
green  = '\033[92m'     # bright green foreground
blue   = '\033[96m'     # bright blue foreground


# user name
USER = getpass.getuser()


def get_parser():
    parser = argparse.ArgumentParser(prog='reinstall', description=(
                    'Homebrew Package Reinstall Manager'
                ), usage=(
                    'macdaily reinstall [-hV] [-qv] [-f] [-es PKG] [-a] [--[no-]MODE] MODE ... '
                ), epilog=(
                    'aliases: reinstall, re, R'
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
                            'macdaily reinstall brew [-hV] [-qv] [-f] [-se PKG] [-a] [--[no-]MODE] MODE ... '
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
    parser_brew.add_argument('--show-log', action='store_true', default=False,
                        help=(
                            'open log in Console upon completion of command'
                        ))

    parser_cask = subparser.add_parser('cask', description=(
                            'Reinstall Caskroom Packages'
                        ), usage=(
                            'macdaily reinstall cask [-hV] [-qv] [-se PKG] [-a] [--[no-]MODE] MODE ... '
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
    parser_cask.add_argument('--show-log', action='store_true', default=False,
                        help=(
                            'open log in Console upon completion of command'
                        ))

    parser_cleanup = subparser.add_parser('cleanup', description=(
                            'Cleanup Caches & Downloads'
                        ), usage=(
                            'macdaily reinstall cleanup [-h] [-q] [--no-brew] [--no-cask]'
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
    parser_cleanup.add_argument('--show-log', action='store_true', default=False,
                        help=(
                            'open log in Console upon completion of command'
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
    parser.add_argument('--show-log', action='store_true', default=False,
                        help=(
                            'open log in Console upon completion of command'
                        ))

    return parser


def main(argv, config, *, logdate, logtime, today):
    parser = get_parser()
    args = parser.parse_args(argv)

    if args.mode is None:
        parser.print_help()
        return

    tmppath, logpath, arcpath, tarpath = make_path(config, mode='reinstall', logdate=logdate)
    logname = f'{logpath}/{logdate}/{logtime}.log'
    tmpname = f'{tmppath}/reinstall.log'

    mode = '-*- Arguments -*-'.center(80, ' ')
    with open(logname, 'a') as logfile:
        logfile.write(datetime.date.strftime(today, ' %+ ').center(80, '—'))
        logfile.write(f'\n\nCMD: {python} {program}')
        logfile.write(f'\n\n{mode}\n\n')
        for key, value in args.__dict__.items():
            logfile.write(f'ARG: {key} = {value}\n')

    if pwd.getpwuid(os.stat(logname).st_uid) != USER:
        subprocess.run(
            ['sudo', '--user', 'root', '--set-home', 'chown', '-R', USER, config['Path']['tmpdir'], config['Path']['logdir']],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

    for mode in config['Mode'].keys():
        try:
            flag = not config['Mode'].getboolean(mode)
        except ValueError as error:
            sys.tracebacklimit = 0
            raise error from None
        if flag:
            args.__setattr__(f'no_{mode}', flag)
    if isinstance(args.mode, str):
        args.mode = [args.mode]
    if 'all' in args.mode:
        args.mode = ['all']

    for mode in set(args.mode):
        reinstall = MODE.get(mode)
        log = aftermath(logfile=logname, tmpfile=tmpname, command='prinstall'
                )(reinstall)(args, file=logname, temp=tmpname, disk=config['Path']['arcdir'])

    if log == set():    return
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
                    print(  f'reinstall: {green}{mode}{reset}: '
                            f'reinstalled following {bold}{name}{reset} packages: {red}{pkgs_coloured}{reset}'  )
            else:
                logfile.write(f"LOG: no package reinstalled in {name}\n")
                if not args.quiet:
                    print(f'reinstall: {green}{mode}{reset}: no package reinstalled in {bold}{name}{reset}')

        filelist = archive(config, logpath=logpath, arcpath=arcpath, tarpath=tarpath, logdate=logdate, today=today)
        if filelist:
            files = ', '.join(filelist)
            logfile.write(f'LOG: archived following old logs: {files}\n')
            if not args.quiet:
                print(f'reinstall: {green}cleanup{reset}: ancient logs archived into {under}{arcdir}{reset}')

    if args.show_log:
        subprocess.run(['open', '-a', 'Console', logname], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
