# -*- coding: utf-8 -*-


import argparse
import calendar
import datetime
import os
import pathlib
import platform
import shlex
import shutil
import subprocess
import sys
import tarfile
import zipfile

from jsdaily.libprinstall import postinstall


# version string
__version__ = '1.1.0'


# today
today = datetime.datetime.today()


# terminal commands
python = sys.prefix             # Python version
program = ' '.join(sys.argv)    # arguments


# terminal display
reset  = '\033[0m'      # reset
bold   = '\033[1m'      # bold
under  = '\033[4m'      # underline
red    = '\033[91m'     # bright red foreground
green  = '\033[92m'     # bright green foreground
blue   = '\033[96m'     # bright blue foreground


def get_parser():
    parser = argparse.ArgumentParser(prog='postinstall', description=(
        'Homebrew Package Postinstall Manager'
    ), usage=(
        'jsdaily postinstall [-hV] [-qv] [-eps PKG] [-a] [--no-cleanup] '
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

    return parser


def main(argv, config):
    try:
        parser = get_parser()
        args = parser.parse_args(argv)

        if args.package is None:
            parser.print_help()
            return

        tmpdir = config['Path']['tmpdir']
        logdir = config['Path']['logdir'] + '/postinstall'
        arcdir = config['Path']['logdir'] + '/archive/postinstall'
        tardir = config['Path']['logdir'] + '/tarfile/postinstall'

        logdate = datetime.date.strftime(today, '%y%m%d')
        logtime = datetime.date.strftime(today, '%H%M%S')
        logname = f'{logdir}/{logdate}/{logtime}.log'
        tmpname = f'{tmpdir}/postinstall.log'

        pathlib.Path(arcdir).mkdir(parents=True, exist_ok=True)
        pathlib.Path(tardir).mkdir(parents=True, exist_ok=True)
        pathlib.Path(tmpdir).mkdir(parents=True, exist_ok=True)
        pathlib.Path(f'{logdir}/{logdate}').mkdir(parents=True, exist_ok=True)

        dskpath = pathlib.Path(config['Path']['dskdir'])
        if dskpath.exists() and dskpath.is_dir():
            pathlib.Path(config['Path']['arcdir']).mkdir(parents=True, exist_ok=True)

        mode = '-*- Arguments -*-'.center(80, ' ')
        with open(logname, 'a') as logfile:
            logfile.write(datetime.date.strftime(today, ' %+ ').center(80, '—'))
            logfile.write(f'\n\nCMD: {python} {program}')
            logfile.write(f'\n\n{mode}\n\n')
            for key, value in args.__dict__.items():
                logfile.write(f'ARG: {key} = {value}\n')

        log = postinstall(args, file=logname, temp=tmpname, disk=config['Path']['arcdir'])

        filelist = list()
        for subdir in os.listdir(logdir):
            if subdir == '.DS_Store':
                continue
            absdir = os.path.join(logdir, subdir)
            if not os.path.isdir(absdir):
                continue
            if subdir != logdate:
                tarname = f'{arcdir}/{subdir}.tar.gz'
                with tarfile.open(tarname, 'w:gz') as tf:
                    abs_src = os.path.abspath(absdir)
                    for dirname, subdirs, files in os.walk(absdir):
                        for filename in files:
                            if filename == '.DS_Store':
                                continue
                            name, ext = os.path.splitext(filename)
                            if ext != '.log':
                                continue
                            absname = os.path.abspath(os.path.join(dirname, filename))
                            arcname = absname[len(abs_src) + 1:]
                            tf.add(absname, arcname)
                            filelist.append(arcname)
                    shutil.rmtree(absdir)

        ctime = datetime.datetime.fromtimestamp(os.stat(arcdir).st_birthtime)
        delta = today - ctime
        if delta > datetime.timedelta(7):
            arcdate = datetime.date.strftime(ctime, '%y%m%d')
            tarname = f'{tardir}/{arcdate}-{logdate}.tar.bz'
            with tarfile.open(tarname, 'w:bz2') as tf:
                abs_src = os.path.abspath(arcdir)
                for dirname, subdirs, files in os.walk(arcdir):
                    for filename in files:
                        if filename == '.DS_Store':
                            continue
                        name, ext = os.path.splitext(filename)
                        if ext != '.gz':
                            continue
                        absname = os.path.abspath(os.path.join(dirname, filename))
                        arcname = absname[len(abs_src) + 1:]
                        tf.add(absname, arcname)
                        filelist.append(arcname)
                shutil.rmtree(arcdir)

        if dskpath.exists() and dskpath.is_dir():
            ctime = datetime.datetime.fromtimestamp(os.stat(config['Path']['logdir'] + '/tarfile').st_birthtime)
            delta = today - ctime
            if delta > datetime.timedelta(calendar.monthrange(today.year, today.month)[1]):
                arcdate = datetime.date.strftime(ctime, '%y%m%d')
                tarname = f'{tmpdir}/{arcdate}-{logdate}.tar.xz'
                with tarfile.open(tarname, 'w:xz') as tf:
                    abs_src = os.path.abspath(config['Path']['logdir'] + '/tarfile')
                    for dirname, subdirs, files in os.walk(config['Path']['logdir'] + '/tarfile'):
                        for filename in files:
                            if filename == '.DS_Store':
                                continue
                            name, ext = os.path.splitext(filename)
                            if ext != '.bz':
                                continue
                            absname = os.path.abspath(os.path.join(dirname, filename))
                            arcname = absname[len(abs_src) + 1:]
                            tf.add(absname, arcname)
                            filelist.append(arcname)
                    shutil.rmtree(config['Path']['logdir'] + '/tarfile')

                arcfile = config['Path']['arcdir'] + '/archive.zip'
                with zipfile.ZipFile(arcfile, 'a', zipfile.ZIP_DEFLATED) as zf:
                    arcname = os.path.split(tarname)[1]
                    zf.write(tarname, arcname)
                    filelist.append(arcname)
                    os.remove(tarname)

        mode = '-*- Postinstall Logs -*-'.center(80, ' ')
        with open(logname, 'a') as logfile:
            logfile.write(f'\n\n{mode}\n\n')
            if not args.quiet:
                print(f'-*- {blue}Postinstall Logs{reset} -*-\n')

            mode = 'brew'
            name = 'Homebrew'
            if log and all(log):
                pkgs = f', '.join(log)
                logfile.write(f'LOG: postinstalled following {name} packages: {pkgs}\n')
                if not args.quiet:
                    pkgs_coloured = f'{reset}, {red}'.join(log)
                    print(
                        f'postinstall: {green}{mode}{reset}: '
                        f'postinstalled following {bold}{name}{reset} packages: {red}{pkgs_coloured}{reset}'
                    )
            else:
                logfile.write(f"LOG: no package postinstalled in {name}\n")
                if not args.quiet:
                    print(f'postinstall: {green}{mode}{reset}: no package postinstalled in {bold}{name}{reset}')

            if filelist:
                files = ', '.join(filelist)
                logfile.write(f'LOG: archived following old logs: {files}\n')
                if not args.quiet:
                    print(f'postinstall: {green}cleanup{reset}: ancient logs archived into {under}{arcdir}{reset}')
    except (KeyboardInterrupt, PermissionError):
        logdate = datetime.date.strftime(today, '%y%m%d')
        logtime = datetime.date.strftime(today, '%H%M%S')
        logfile = shlex.quote(config['Path']['logdir'] + f'/postinstall/{logdate}/{logtime}.log')
        tmpfile = shlex.quote(config['Path']['tmpdir'] + '/postinstall.log')
        subprocess.run(['bash', 'libprinstall/aftermath.sh', logfile, tmpfile, 'postinstall', 'true'])


if __name__ == '__main__':
    sys.exit(main())
