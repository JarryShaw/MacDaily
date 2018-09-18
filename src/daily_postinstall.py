# -*- coding: utf-8 -*-


import argparse
import base64
import datetime
import os
import pwd
import shutil
import subprocess
import sys
import tempfile

from macdaily.daily_config import parse
from macdaily.daily_utility import beholder, aftermath, make_pipe, make_path, archive, storage
from macdaily.libprinstall import postinstall


# version string
__version__ = '2018.09.14'


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


def postinstall(argv, config, *, logdate, logtime, today):
    parser = get_parser()
    args = parser.parse_args(argv)

    if args.package is None:
        parser.print_help()
        return

    tmppath, logpath, arcpath, tarpath = make_path(config, mode='postinstall', logdate=logdate)
    tmpfile = tempfile.NamedTemporaryFile(dir=tmppath, prefix='postinstall-', suffix='.log')
    logname = '{}/{}/{}.log'.format(logpath, logdate, logtime)
    tmpname = tmpfile.name

    PIPE = make_pipe(config)
    USER = config['Account']['username']
    PASS = base64.b64encode(PIPE.stdout.readline().strip()).decode()

    mode = '-*- Arguments -*-'.center(80, ' ')
    with open(logname, 'a') as logfile:
        logfile.write(datetime.date.strftime(today, ' %+ ').center(80, '—'))
        logfile.write('\n\nCMD: {} {}'.format(python, program))
        logfile.write('\n\n{}\n\n'.format(mode))
        for key, value in args.__dict__.items():
            logfile.write('ARG: {} = {}\n'.format(key, value))

    if pwd.getpwuid(os.stat(logname).st_uid) != USER:
        subprocess.run(['sudo', 'chown', '-R', USER, config['Path']['tmpdir'], config['Path']['logdir']],
                       stdin=PIPE.stdout, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    log = aftermath(logfile=logname, tmpfile=tmpname, command='prinstall', logmode='postinstall')(
            postinstall)(args, file=logname, temp=tmpname, disk=config['Path']['arcdir'], password=PASS,
                         bash_timeout=config['Environment'].getint('bash-timeout', fallback=1_000),
                         sudo_timeout=str(config['Environment'].getint('sudo-timeout', fallback=300) // 2))

    if log != dict():
        if not args.quiet:
            print('-*- {}Postinstall Logs{} -*-'.format(blue, reset).center(length, ' '), '\n', sep='')
        mode = '-*- Postinstall Logs -*-'.center(80, ' ')
        with open(logname, 'a') as logfile:
            logfile.write('\n\n{}\n\n'.format(mode))

            mode = 'brew';  name = 'Homebrew'
            if log and all(log):
                pkgs = ', '.format().join(log)
                logfile.write('LOG: postinstalled following {} packages: {}\n'.format(name, pkgs))
                if not args.quiet:
                    pkgs_coloured = '{}, {}'.format(reset, red).join(log)
                    print('postinstall: {}{}{}: '
                          'postinstalled following {}{}{} packages: {}{}{}'.format(green, mode, reset, bold, name, reset, red, pkgs_coloured, reset))
            else:
                logfile.write("LOG: no package postinstalled in {}\n".format(name))
                if not args.quiet:
                    print('postinstall: {}{}{}: no package postinstalled in {}{}{}'.format(green, mode, reset, bold, name, reset))

            filelist = archive(config, logpath=logpath, arcpath=arcpath, tarpath=tarpath, logdate=logdate, today=today)
            if filelist:
                files = ', '.join(filelist)
                logfile.write('LOG: archived following ancient logs: {}\n'.format(files))
                if not args.quiet:
                    print('uninstall: {}cleanup{}: ancient logs archived into {}{}{}'.format(green, reset, under, arcpath, reset))
            else:
                logfile.write('LOG: no ancient logs archived\n'.format())
                if not args.quiet:
                    print('uninstall: {}cleanup{}: no ancient logs archived'.format(green, reset))

    with contextlib.suppress(Exception):
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
    postinstall(argv, config, logdate=logdate, logtime=logtime, today=today)


if __name__ == '__main__':
    sys.exit(main())
