# -*- coding: utf-8 -*-


import argparse
import datetime
import getpass
import os
import pwd
import subprocess
import sys

from macdaily.daily_utility import *
from macdaily.libprinstall import postinstall


# version string
__version__ = '2018.08.29'


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
    parser = argparse.ArgumentParser(prog='postinstall', description=(
        'Homebrew Package Postinstall Manager'
    ), usage=(
        'macdaily postinstall [-hV] [-qv] [-eps PKG] [-a] [--no-cleanup] '
    ), epilog=(
        'aliases: postinstall, post, ps, p'
    ))
    parser.add_argument('-V', '--version', action='version', version=__version__)
    parser.add_argument('-a', '--all', action='append_const', const='all',
                        dest='package', help=(
                            'postinstall all packages installed through Homebrew'
                        ))

    parser.add_argument('-p', '--package', metavar='PKG', action='append',
                        dest='package', help=(
                            'name of packages to be postinstalled, default is all'
                        ))
    parser.add_argument('-s', '--startwith', metavar='START', action='store',
                        dest='start', help=(
                            'postinstall procedure starts from which package, sort '
                            'in initial alphabets'
                        ))
    parser.add_argument('-e', '--endwith', metavar='START', action='store',
                        dest='end', help=(
                            'postinstall procedure ends until which package, sort '
                            'in initial alphabets'
                        ))
    parser.add_argument('-q', '--quiet', action='store_true', default=False,
                        help=(
                            'run in quiet mode, with no output information'
                        ))
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help=(
                            'run in verbose mode, with detailed output information'
                        ))
    parser.add_argument('--no-cleanup', action='store_true', default=False,
                        help=(
                            'do not remove postinstall caches & downloads'
                        ))
    parser.add_argument('--show-log', action='store_true', default=False,
                        help=(
                            'open log in Console upon completion of command'
                        ))

    return parser


def main(argv, config, *, logdate, logtime, today):
    parser = get_parser()
    args = parser.parse_args(argv)

    if args.package is None:
        parser.print_help()
        return

    tmppath, logpath, arcpath, tarpath = make_path(config, mode='postinstall', logdate=logdate)
    logname = f'{logpath}/{logdate}/{logtime}.log'
    tmpname = f'{tmppath}/postinstall.log'

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

    log = aftermath(logfile=logname, tmpfile=tmpname, command='prinstall'
            )(postinstall)(args, file=logname, temp=tmpname, disk=config['Path']['arcdir'])

    if log == set():    return
    mode = '-*- Postinstall Logs -*-'.center(80, ' ')
    with open(logname, 'a') as logfile:
        logfile.write(f'\n\n{mode}\n\n')
        if not args.quiet:
            print(f'-*- {blue}Postinstall Logs{reset} -*-\n')

        mode = 'brew';  name = 'Homebrew'
        if log and all(log):
            pkgs = f', '.join(log)
            logfile.write(f'LOG: postinstalled following {name} packages: {pkgs}\n')
            if not args.quiet:
                pkgs_coloured = f'{reset}, {red}'.join(log)
                print(  f'postinstall: {green}{mode}{reset}: '
                        f'postinstalled following {bold}{name}{reset} packages: {red}{pkgs_coloured}{reset}'    )
        else:
            logfile.write(f"LOG: no package postinstalled in {name}\n")
            if not args.quiet:
                print(f'postinstall: {green}{mode}{reset}: no package postinstalled in {bold}{name}{reset}')

        filelist = archive(config, logpath=logpath, arcpath=arcpath, tarpath=tarpath, logdate=logdate, today=today)
        if filelist:
            files = ', '.join(filelist)
            logfile.write(f'LOG: archived following old logs: {files}\n')
            if not args.quiet:
                print(f'postinstall: {green}cleanup{reset}: ancient logs archived into {under}{arcdir}{reset}')

    if args.show_log:
        subprocess.run(['open', '-a', 'Console', logname], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
