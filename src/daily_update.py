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
from macdaily.libupdate import *

# version string
__version__ = '2018.09.21b2'

# display mode names
NAME = dict(
    apm='Atom',
    gem='Ruby',
    mas='Mac App Store',
    npm='Node.js',
    pip='Python',
    brew='Homebrew',
    cask='Caskroom',
    system='System Software',
)

# mode actions
MODE = dict(
    all=lambda *args, **kwargs: update_all(*args, **kwargs),
    apm=lambda *args, **kwargs: update_apm(*args, **kwargs),
    gem=lambda *args, **kwargs: update_gem(*args, **kwargs),
    mas=lambda *args, **kwargs: update_mas(*args, **kwargs),
    npm=lambda *args, **kwargs: update_npm(*args, **kwargs),
    pip=lambda *args, **kwargs: update_pip(*args, **kwargs),
    brew=lambda *args, **kwargs: update_brew(*args, **kwargs),
    cask=lambda *args, **kwargs: update_cask(*args, **kwargs),
    system=lambda *args, **kwargs: update_system(*args, **kwargs),
    cleanup=lambda *args, **kwargs: update_cleanup(*args, **kwargs),
)


def get_parser():
    parser = argparse.ArgumentParser(
                prog='update',
                description='Automatic Package Update Manager',
                usage='macdaily update [-hV] [-qv] [-fgm] [-a] [--[no-]MODE] MODE ...',
                epilog='aliases: update, up, upgrade')
    parser.add_argument('-V', '--version', action='version', version=__version__)
    parser.add_argument('-a', '--all', action='append_const', const='all', dest='mode',
                        help=('update all packages installed through Atom, RubyGem, Node.js, '
                              'Homebrew, Caskroom, Mac App Store, and etc'))

    parser.add_argument('--apm', action='append_const', const='apm', dest='mode', help=argparse.SUPPRESS)
    parser.add_argument('--gem', action='append_const', const='gem', dest='mode', help=argparse.SUPPRESS)
    parser.add_argument('--mas', action='append_const', const='mas', dest='mode', help=argparse.SUPPRESS)
    parser.add_argument('--npm', action='append_const', const='npm', dest='mode', help=argparse.SUPPRESS)
    parser.add_argument('--pip', action='append_const', const='pip', dest='mode', help=argparse.SUPPRESS)
    parser.add_argument('--brew', action='append_const', const='brew', dest='mode', help=argparse.SUPPRESS)
    parser.add_argument('--cask', action='append_const', const='cask', dest='mode', help=argparse.SUPPRESS)
    parser.add_argument('--system', action='append_const', const='system', dest='mode', help=argparse.SUPPRESS)
    parser.add_argument('--cleanup', action='append_const', const='cleanup', dest='mode', help=argparse.SUPPRESS)

    parser.add_argument('--no-apm', action='store_true', default=False, help=argparse.SUPPRESS)
    parser.add_argument('--no-gem', action='store_true', default=False, help=argparse.SUPPRESS)
    parser.add_argument('--no-mas', action='store_true', default=False, help=argparse.SUPPRESS)
    parser.add_argument('--no-npm', action='store_true', default=False, help=argparse.SUPPRESS)
    parser.add_argument('--no-pip', action='store_true', default=False, help=argparse.SUPPRESS)
    parser.add_argument('--no-brew', action='store_true', default=False, help=argparse.SUPPRESS)
    parser.add_argument('--no-cask', action='store_true', default=False, help=argparse.SUPPRESS)
    parser.add_argument('--no-system', action='store_true', default=False, help=argparse.SUPPRESS)
    parser.add_argument('--no-cleanup', action='store_true', default=False, help=argparse.SUPPRESS)

    subparser = parser.add_subparsers(title='mode selection', metavar='MODE', dest='mode',
                                      help=('update outdated packages installed through a specified method, '
                                            'e.g.: apm, gem, mas, npm, pip, brew, cask, system, '
                                            'or alternatively and simply, cleanup'))

    parser_apm = subparser.add_parser('apm', description='Update Installed Atom Packages',
                                      usage='macdaily update apm [-h] [-qv] [-a] [-p PKG]')
    parser_apm.add_argument('-a', '--all', action='store_true', default=False, dest='all',
                            help='update all packages installed through apm')
    parser_apm.add_argument('-p', '--package', metavar='PKG', action='append', dest='package',
                            help='name of packages to be updated, default is all')
    parser_apm.add_argument('-q', '--quiet', action='store_true', default=False,
                            help='run in quiet mode, with no output information')
    parser_apm.add_argument('-v', '--verbose', action='store_true', default=False,
                            help='run in verbose mode, with detailed output information')
    parser_apm.add_argument('-Y', '--yes', action='store_true', default=False, dest='yes',
                            help='yes for all selections')
    parser_apm.add_argument('--show-log', action='store_true', default=False,
                            help='open log in Console upon completion of command')

    parser_gem = subparser.add_parser('gem', description='Update Installed Ruby Packages',
                                      usage='macdaily update gem [-h] [-qv] [-a] [-p PKG]')
    parser_gem.add_argument('-a', '--all', action='store_true', default=False, dest='all',
                            help='update all packages installed through gem')
    parser_gem.add_argument('-p', '--package', metavar='PKG', action='append', dest='package',
                            help='name of packages to be updated, default is all')
    parser_gem.add_argument('-q', '--quiet', action='store_true', default=False,
                            help='run in quiet mode, with no output information')
    parser_gem.add_argument('-v', '--verbose', action='store_true', default=False,
                            help='run in verbose mode, with detailed output information')
    parser_gem.add_argument('-Y', '--yes', action='store_true', default=False, dest='yes',
                            help='yes for all selections')
    parser_gem.add_argument('--show-log', action='store_true', default=False,
                            help='open log in Console upon completion of command')

    parser_mas = subparser.add_parser('mas', description='Update Installed Mac App Store Packages',
                                      usage='macdaily update mas [-h] [-qv] [-a] [-p PKG]')
    parser_mas.add_argument('-a', '--all', action='store_true', default=False, dest='all',
                            help='update all packages installed through Mac App Store')
    parser_mas.add_argument('-p', '--package', metavar='PKG', action='append', dest='package',
                            help='name of packages to be updated, default is all')
    parser_mas.add_argument('-q', '--quiet', action='store_true', default=False,
                            help='run in quiet mode, with no output information')
    parser_mas.add_argument('-v', '--verbose', action='store_true', default=False,
                            help='run in verbose mode, with detailed output information')
    parser_mas.add_argument('--show-log', action='store_true', default=False,
                            help='open log in Console upon completion of command')

    parser_npm = subparser.add_parser('npm', description='Update Installed Node.js Packages',
                                      usage='macdaily update npm [-h] [-qv] [-a] [-p PKG]')
    parser_npm.add_argument('-a', '--all', action='store_true', default=False, dest='all',
                            help='update all packages installed through npm')
    parser_npm.add_argument('-p', '--package', metavar='PKG', action='append', dest='package',
                            help='name of packages to be updated, default is all')
    parser_npm.add_argument('-q', '--quiet', action='store_true', default=False,
                            help='run in quiet mode, with no output information')
    parser_npm.add_argument('-v', '--verbose', action='store_true', default=False,
                            help='run in verbose mode, with detailed output information')
    parser_npm.add_argument('--show-log', action='store_true', default=False,
                            help='open log in Console upon completion of command')

    parser_pip = subparser.add_parser('pip', description='Update Installed Python Packages',
                                      usage='macdaily update pip [-h] [-qv] [-bcsy] [-V VER] [-a] [-p PKG]')
    parser_pip.add_argument('-a', '--all', action='store_true', default=False, dest='all',
                            help='update all packages installed through pip')
    parser_pip.add_argument('-V', '--python_version', action='store', metavar='VER', dest='version',
                            choices=[0, 1, 2, 20, 21, 22, 23, 24, 25, 26, 27, 3, 30, 31, 32, 33, 34, 35, 36, 37],
                            type=int, default=0, help='indicate which version of pip will be updated')
    parser_pip.add_argument('-s', '--system', action='store_true', default=False, dest='system',
                            help=('update pip packages on system level, '
                                  'i.e. Python installed through official installer'))
    parser_pip.add_argument('-b', '--brew', action='store_true', default=False, dest='brew',
                            help='update pip packages on Cellar level, i.e. Python installed through Homebrew')
    parser_pip.add_argument('-c', '--cpython', action='store_true', default=False, dest='cpython',
                            help='update pip packages on CPython environment')
    parser_pip.add_argument('-y', '--pypy', action='store_true', default=False, dest='pypy',
                            help='update pip packages on PyPy environment')
    parser_pip.add_argument('-p', '--package', metavar='PKG', action='append', dest='package',
                            help='name of packages to be updated, default is all')
    parser_pip.add_argument('-P', '--pre', action='store_true', default=False, dest='pre',
                            help='include pre-release and development versions')
    parser_pip.add_argument('-Y', '--yes', action='store_true', default=False, dest='yes',
                            help='yes for all selections')
    parser_pip.add_argument('-q', '--quiet', action='store_true', default=False,
                            help='run in quiet mode, with no output information')
    parser_pip.add_argument('-v', '--verbose', action='store_true', default=False,
                            help='run in verbose mode, with detailed output information')
    parser_pip.add_argument('--show-log', action='store_true', default=False,
                            help='open log in Console upon completion of command')

    parser_brew = subparser.add_parser('brew', description='Update Installed Homebrew Packages',
                                       usage='macdaily update brew [-h] [-qv] [-fm] [-a] [-p PKG] [--no-cleanup]')
    parser_brew.add_argument('-a', '--all', action='store_true', default=False, dest='all',
                             help='update all packages installed through Homebrew')
    parser_brew.add_argument('-p', '--package', metavar='PKG', action='append', dest='package',
                             help='name of packages to be updated, default is all')
    parser_brew.add_argument('-f', '--force', action='store_true', default=False,
                             help='use "--force" when running `brew update`')
    parser_brew.add_argument('-m', '--merge', action='store_true', default=False,
                             help='use "--merge" when running `brew update`')
    parser_brew.add_argument('-q', '--quiet', action='store_true', default=False,
                             help='run in quiet mode, with no output information')
    parser_brew.add_argument('-v', '--verbose', action='store_true', default=False,
                             help='run in verbose mode, with detailed output information')
    parser_brew.add_argument('--no-cleanup', action='store_false', default=True, dest='nocleanup',
                             help='do not remove caches & downloads')
    parser_brew.add_argument('--show-log', action='store_true', default=False,
                             help='open log in Console upon completion of command')

    parser_cask = subparser.add_parser('cask', description='Update Installed Caskroom Packages',
                                       usage='macdaily update cask [-h] [-qv] [-fg] [-a] [-p PKG] [--no-cleanup]')
    parser_cask.add_argument('-a', '--all', action='store_true', default=False, dest='all',
                             help='update all packages installed through Caskroom')
    parser_cask.add_argument('-p', '--package', metavar='PKG', action='append', dest='package',
                             help='name of packages to be updated, default is all')
    parser_cask.add_argument('-m', '--merge', action='store_true', default=False,
                             help='use "--merge" when running `brew update`')
    parser_cask.add_argument('-f', '--force', action='store_true', default=False,
                             help='use "--force" when running `brew cask upgrade`')
    parser_cask.add_argument('-g', '--greedy', action='store_true', default=False,
                             help=('use "--greedy" when running `brew cask outdated`, '
                                   'and directly run `brew cask upgrade --greedy`'))
    parser_cask.add_argument('-q', '--quiet', action='store_true', default=False,
                             help='run in quiet mode, with no output information')
    parser_cask.add_argument('-v', '--verbose', action='store_true', default=False,
                             help='run in verbose mode, with detailed output information')
    parser_cask.add_argument('--no-cleanup', action='store_false', default=True, dest='nocleanup',
                             help='do not remove caches & downloads')
    parser_cask.add_argument('--show-log', action='store_true', default=False,
                             help='open log in Console upon completion of command')

    parser_system = subparser.add_parser('system', description='Update Installed System Packages',
                                         usage='macdaily update system [-h] [-qv] [-r] [-a] [-p PKG]')
    parser_system.add_argument('-a', '--all', action='store_true', default=False, dest='all',
                               help='update all packages installed through softwareupdate')
    parser_system.add_argument('-p', '--package', metavar='PKG', action='append', dest='package',
                               help='name of packages to be updated, default is all')
    parser_system.add_argument('-r', '--restart', action='store_true', default=False, dest='restart',
                               help='automatically restart if necessary')
    parser_system.add_argument('-q', '--quiet', action='store_true', default=False,
                               help='run in quiet mode, with no output information')
    parser_system.add_argument('-v', '--verbose', action='store_true', default=False,
                               help='run in verbose mode, with detailed output information')
    parser_system.add_argument('--show-log', action='store_true', default=False,
                               help='open log in Console upon completion of command')

    parser_cleanup = subparser.add_parser('cleanup', description='Cleanup Caches & Downloads',
                                          usage='macdaily update cleanup [-h] [-q] [--no-brew] [--no-cask]')
    parser_cleanup.add_argument('--no-gem', dest='gem', action='store_false', default=True,
                                help='do not remove Ruby caches & downloads')
    parser_cleanup.add_argument('--no-npm', dest='npm', action='store_false', default=True,
                                help='do not remove Node.js caches & downloads')
    parser_cleanup.add_argument('--no-pip', dest='pip', action='store_false', default=True,
                                help='do not remove Python caches & downloads')
    parser_cleanup.add_argument('--no-brew', dest='brew', action='store_false', default=True,
                                help='do not remove Homebrew caches & downloads')
    parser_cleanup.add_argument('--no-cask', dest='cask', action='store_false', default=True,
                                help='do not remove Caskroom caches & downloads')
    parser_cleanup.add_argument('-q', '--quiet', action='store_true', default=False,
                                help='run in quiet mode, with no output information')
    parser_cleanup.add_argument('--show-log', action='store_true', default=False,
                                help='open log in Console upon completion of command')

    parser.add_argument('-f', '--force', action='store_true', default=False,
                        help='run in force mode, only for Homebrew or Caskroom')
    parser.add_argument('-m', '--merge', action='store_true', default=False,
                        help='run in merge mode, only for Homebrew')
    parser.add_argument('-g', '--greedy', action='store_true', default=False,
                        help='run in greedy mode, only for Caskroom')
    parser.add_argument('-r', '--restart', action='store_true', default=False,
                        dest='restart', help='automatically restart if necessary, only for System')
    parser.add_argument('-P', '--pre', action='store_true', default=False, dest='pre',
                        help='include pre-release and development versions, only for Python')
    parser.add_argument('-Y', '--yes', action='store_true', default=False,
                        dest='yes', help='yes for all selections, only for pip and apm')
    parser.add_argument('-q', '--quiet', action='store_true', default=False,
                        help='run in quiet mode, with no output information')
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help='run in verbose mode, with detailed output information')
    parser.add_argument('--show-log', action='store_true', default=False,
                        help='open log in Console upon completion of command')

    return parser


def update(argv, config, logdate, logtime, today):
    parser = get_parser()
    args = parser.parse_args(argv)

    if args.mode is None:
        parser.print_help()
        exit(1)

    tmppath, logpath, arcpath, tarpath = make_path(config, mode='update', logdate=logdate)
    tmpfile = tempfile.NamedTemporaryFile(dir=tmppath, prefix='update-', suffix='.log')
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

    arcdir = config['Path']['arcdir']
    bash_timeout = config['Environment'].getint('bash-timeout', fallback=1_000)
    sudo_timeout = str(config['Environment'].getint('sudo-timeout', fallback=300) // 2)

    for mode in set(args.mode):
        update = MODE.get(mode)
        log = aftermath(logfile=logname, tmpfile=tmpname, command='update')(
                update)(args, file=logname, temp=tmpname, disk=arcdir, password=PASS,
                        bash_timeout=bash_timeout, sudo_timeout=sudo_timeout)

    if log != dict():
        if not args.quiet:
            print('-*- {}Update Logs{} -*-'.format(blue, reset).center(length, ' '), '\n', sep='')
        mode = '-*- Update Logs -*-'.center(80, ' ')
        with open(logname, 'a') as logfile:
            logfile.write('\n\n{}\n\n'.format(mode))
            for mode in log:
                name = NAME.get(mode)
                if log[mode] and all(log[mode]):
                    pkgs = ', '.format().join(log[mode])
                    logfile.write('LOG: updated following {} packages: {}\n'.format(name, pkgs))
                    if not args.quiet:
                        pkgs_coloured = '{}, {}'.format(reset, red).join(log[mode])
                        print('update: {}{}{}: '
                              'updated following {}{}{} packages: {}{}{}'.format(green, mode, reset, bold, name, reset, red, pkgs_coloured, reset))
                else:
                    logfile.write("LOG: no package updated in {}\n".format(name))
                    if not args.quiet:
                        print('update: {}{}{}: no package updated in {}{}{}'.format(green, mode, reset, bold, name, reset))

            filelist = archive(config, logpath, arcpath, tarpath, logdate, today)
            if filelist:
                files = ', '.join(filelist)
                logfile.write('LOG: archived following ancient logs: {}\n'.format(files))
                if not args.quiet:
                    print('update: {}cleanup{}: ancient logs archived into {}{}{}'.format(green, reset, under, arcpath, reset))
            else:
                logfile.write('LOG: no ancient logs archived\n'.format())
                if not args.quiet:
                    print('update: {}cleanup{}: no ancient logs archived'.format(green, reset))

            if reload_flag.value:
                proc = subprocess.run(['sudo', '--set-home', sys.executable, '-m',
                                       'pip', 'install', '--upgrade', '--no-cache-dir', '--pre', 'macdaily'],
                                      stdin=PIPE.stdout, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                      timeout=config['Environment'].getint('bash-timeout', fallback=1_000))
                try:
                    proc.check_returncode()
                except subprocess.CalledProcessError:
                    if not args.quiet:
                        print('update: {}macdaily{}: process failed, please try manually'.format(red, reset))
                    logfile.write('ERR: please try manually update macdaily\n')
                else:
                    if not args.quiet:
                        print('update: {}macdaily{}: package is now up-to-date'.format(green, reset))
                    logfile.write('LOG: macdaily is now up-to-date\n')

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
    update(argv, config, logdate, logtime, today)


if __name__ == '__main__':
    sys.tracebacklimit = 0
    sys.exit(main())
