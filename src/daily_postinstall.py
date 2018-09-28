# -*- coding: utf-8 -*-

import argparse
import contextlib
import datetime
import os
import sys
import tempfile

from macdaily.daily_config import parse
from macdaily.daily_utility import (aftermath, archive, beholder, blue, bold,
                                    get_pass, green, length, make_context,
                                    make_path, record_args, red, reset, under)
from macdaily.libprinstall import postinstall

try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess

# version string
__version__ = '2018.09.28'


def get_parser():
    parser = argparse.ArgumentParser(
                prog='postinstall',
                description='Homebrew Package Postinstall Manager',
                usage='macdaily postinstall [-hV] [-qv] [-eps PKG] [-a] [--no-cleanup]',
                epilog='aliases: postinstall, post')
    parser.add_argument('-V', '--version', action='version', version=__version__)
    parser.add_argument('-a', '--all', action='append_const', const='all', dest='package',
                        help='postinstall all packages installed through Homebrew')

    parser.add_argument('-p', '--package', metavar='PKG', action='append', dest='package',
                        help='name of packages to be postinstalled, default is all')
    parser.add_argument('-s', '--startswith', metavar='START', action='store', dest='start',
                        help='postinstall procedure starts from which package, sort in initial alphabets')
    parser.add_argument('-e', '--endswith', metavar='START', action='store', dest='end',
                        help='postinstall procedure ends until which package, sort in initial alphabets')
    parser.add_argument('-q', '--quiet', action='store_true', default=False,
                        help='run in quiet mode, with no output information')
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help='run in verbose mode, with detailed output information')
    parser.add_argument('--no-cleanup', action='store_true', default=False,
                        help='do not remove postinstall caches & downloads')
    parser.add_argument('--show-log', action='store_true', default=False,
                        help='open log in Console upon completion of command')

    return parser


def postinstall_(argv, config, logdate, logtime, today):
    parser = get_parser()
    args = parser.parse_args(argv)

    if args.package is None:
        parser.print_help()
        sys.exit(1)

    def _postinstall():
        return aftermath(logfile=logname, tmpfile=tmpname, command='prinstall', logmode='postinstall')(
                postinstall)(args, file=logname, temp=tmpname, disk=config['Path']['arcdir'], password=PASS,
                             bash_timeout=bash_timeout, sudo_timeout=sudo_timeout)

    def _record_logs():
        if not log:
            logfile.write('LOG: no packages postinstalled\n')
            return
        logfile.write("\n\n{}\n\n".format('-*- Postinstall Logs -*-'.center(80, ' ')))
        print('-*- {}Postinstall Logs{} -*-'.format(blue, reset).center(length, ' '), '\n', sep='')

        if log and all(log):
            pkgs = ', '.format().join(log)
            pkgs_coloured = '{}, {}'.format(reset, red).join(log)
            logfile.write('LOG: postinstalled following Homebrew packages: {}\n'.format(pkgs))
            print('postinstall: {}brew{}: '
                  'postinstalled following {}Homebrew{} packages: {}{}{}'.format(green, reset, bold, reset, red, pkgs_coloured, reset))
        else:
            logfile.write("LOG: no package postinstalled in Homebrew\n".format())
            print('postinstall: {}brew{}: no package postinstalled in {}Homebrew{}'.format(green, reset, bold, reset))

        filelist = archive(config, logpath, arcpath, tarpath, logdate, today)
        if filelist:
            files = ', '.join(filelist)
            logfile.write('LOG: archived following ancient logs: {}\n'.format(files))
            print('uninstall: {}cleanup{}: ancient logs archived into {}{}{}'.format(green, reset, under, arcpath, reset))
        else:
            logfile.write('LOG: no ancient logs archived\n'.format())
            print('uninstall: {}cleanup{}: no ancient logs archived'.format(green, reset))

    tmppath, logpath, arcpath, tarpath = make_path(config, mode='postinstall', logdate=logdate)
    tmpfile = tempfile.NamedTemporaryFile(dir=tmppath, prefix='postinstall-', suffix='.log')
    logname = os.path.join(logpath, logdate, '{}.log'.format(logtime))
    tmpname = tmpfile.name

    bash_timeout = config['Environment'].getint('bash-timeout', fallback=1000)
    sudo_timeout = str(config['Environment'].getint('sudo-timeout', fallback=300) // 2)

    with open(logname, 'w') as logfile:
        record_args(args, today, logfile)
    PASS = get_pass(config, logname)
    with open(os.devnull, 'w') as devnull:
        with make_context(args, devnull):
            log = _postinstall()
            with open(logname, 'a') as logfile:
                _record_logs()
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
    postinstall_(argv, config, logdate=logdate, logtime=logtime, today=today)


if __name__ == '__main__':
    sys.tracebacklimit = 0
    sys.exit(main())
