# -*- coding: utf-8 -*-


import argparse
import datetime
import os
import pathlib
import platform
import sys
import zipfile

from jsdaily.libprinstall import *


# version string
__version__ = '0.7.2'


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
red = 'tput setaf 1'    # blush / red
green = 'tput setaf 2'  # green
blue = 'tput setaf 14'  # blue
bold = 'tput bold'      # bold
under = 'tput smul'     # underline
reset = 'tput sgr0'     # reset


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
    parser = get_parser()
    args = parser.parse_args(argv)

    if args.mode is None:
        parser.print_help()
        return

    pathlib.Path('/tmp/log').mkdir(parents=True, exist_ok=True)
    pathlib.Path('/Library/Logs/Scripts/reinstall').mkdir(parents=True, exist_ok=True)

    logdate = datetime.date.strftime(today, '%y%m%d')
    logname = f'/Library/Logs/Scripts/reinstall/{logdate}.log'

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

    arcfile = '/Library/Logs/Scripts/archive.zip'
    filelist = list()
    with zipfile.ZipFile(arcfile, 'a', zipfile.ZIP_DEFLATED) as zf:
        abs_src = os.path.abspath('/Library/Logs/Scripts')
        for dirname, subdirs, files in os.walk('/Library/Logs/Scripts/reinstall'):
            for filename in files:
                if filename == '.DS_Store':
                    continue
                name, ext = os.path.splitext(filename)
                if ext != '.log':
                    continue
                ctime = datetime.datetime.strptime(name, '%y%m%d')
                delta = today - ctime
                if delta > datetime.timedelta(7):
                    absname = os.path.abspath(os.path.join(dirname, filename))
                    arcname = absname[len(abs_src) + 1:]
                    zf.write(absname, arcname)
                    filelist.append(arcname)
                    os.remove(absname)

    mode = '-*- Reinstall Logs -*-'.center(80, ' ')
    with open(logname, 'a') as logfile:
        logfile.write(f'\n\n{mode}\n\n')
        if not args.quiet:
            os.system(f'echo "-*- $({blue})Reinstall Logs$({reset}) -*-"; echo ;')

        for mode in log:
            name = NAME.get(mode, mode)
            if log[mode] and all(log[mode]):
                pkgs = f', '.join(log[mode])
                logfile.write(f'LOG: Reinstalled following {name} packages: {pkgs}.\n')
                if not args.quiet:
                    pkgs_coloured = f'$({reset}), $({red})'.join(log[mode])
                    os.system(f'echo "reinstall: $({green}){mode}$({reset}): '
                              f'reinstalled following $({bold}){name}$({reset}) packages: $({red}){pkgs_coloured}$({reset})"')
            else:
                logfile.write(f"LOG: No package reinstalled in {name}.\n")
                if not args.quiet:
                    os.system(f'echo "reinstall: $({green}){mode}$({reset}): '
                              f'no package reinstalled in $({bold}){name}$({reset})"')
        if filelist:
            files = ', '.join(filelist)
            logfile.write(f'LOG: Archived following old logs: {files}\n')
            if not args.quiet:
                os.system(f'echo "reinstall: $({green})cleanup$({reset}): '
                          f'ancient logs archived into $({under}){arcfile}$({reset})"')
        logfile.write('\n\n\n\n')


if __name__ == '__main__':
    sys.exit(main())
