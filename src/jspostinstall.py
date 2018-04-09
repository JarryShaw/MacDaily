#!/usr/bin/python3
# -*- coding: utf-8 -*-


import argparse
import datetime
import os
import pathlib
import platform
import sys
import zipfile


from jsdaily.libprinstall import postinstall


# version string
__version__ = '0.7.0'


# today
today = datetime.datetime.today()


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


# error handling class
class UnsupoortedOS(RuntimeError):
    def __init__(self, message, *args, **kwargs):
        sys.tracebacklimit = 0
        super().__init__(message, *args, **kwargs)


def get_parser():
    parser = argparse.ArgumentParser(prog='jspostinstall', description=(
        'Homebrew Package Postinstall Manager'
    ), usage=(
        'jspostinstall [-hV] [-qv] [-eps PKG] [-a] [--no-cleanup] '
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

    return parser


def main():
    if platform.system() != 'Darwin':
        raise UnsupoortedOS('postinstall: script runs only on macOS')

    parser = get_parser()
    args = parser.parse_args()

    if args.package is None:
        parser.print_help()
        return

    pathlib.Path('/tmp/log').mkdir(parents=True, exist_ok=True)
    pathlib.Path('/Library/Logs/Scripts/postinstall').mkdir(parents=True, exist_ok=True)

    logdate = datetime.date.strftime(today, '%y%m%d')
    logname = f'/Library/Logs/Scripts/postinstall/{logdate}.log'

    mode = '-*- Arguments -*-'.center(80, ' ')
    with open(logname, 'a') as logfile:
        logfile.write(datetime.date.strftime(today, '%+').center(80, '—'))
        logfile.write(f'\n\nCMD: {python} {program}')
        logfile.write(f'\n\n{mode}\n\n')
        for key, value in args.__dict__.items():
            logfile.write(f'ARG: {key} = {value}\n')

    log = postinstall(args, file=logname, date=logdate)

    arcfile = '/Library/Logs/Scripts/archive.zip'
    filelist = list()
    with zipfile.ZipFile(arcfile, 'a', zipfile.ZIP_DEFLATED) as zf:
        abs_src = os.path.abspath('/Library/Logs/Scripts')
        for dirname, subdirs, files in os.walk('/Library/Logs/Scripts/postinstall'):
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

    mode = '-*- Postinstall Logs -*-'.center(80, ' ')
    with open(logname, 'a') as logfile:
        logfile.write(f'\n\n{mode}\n\n')
        if not args.quiet:
            os.system(f'echo "-*- $({blue})Postinstall Logs$({reset}) -*-"; echo ;')

        name = 'Homebrew'
        if log and all(log):
            pkgs = f', '.join(log[mode])
            logfile.write(f'LOG: Postinstalled following {name} packages: {pkgs}.\n')
            if not args.quiet:
                pkgs_coloured = f'$({reset}), $({red})'.join(log[mode])
                os.system(f'echo "postinstall: $({green}){mode}$({reset}): '
                          f'postinstalled following $({bold}){name}$({reset}) packages: $({red}){pkgs_coloured}$({reset})"')
        else:
            logfile.write(f"LOG: No package postinstalled in {name}.\n")
            if not args.quiet:
                os.system(f'echo "postinstall: $({green}){mode}$({reset}): '
                          f'no package postinstalled in $({bold}){name}$({reset})"')

        if filelist:
            files = ', '.join(filelist)
            logfile.write(f'LOG: Archived following old logs: {files}\n')
            if not args.quiet:
                os.system(f'echo "postinstall: $({green})cleanup$({reset}): '
                          f'ancient logs archived into $({under}){arcfile}$({reset})"')
        logfile.write('\n\n\n\n')


if __name__ == '__main__':
    sys.exit(main())
