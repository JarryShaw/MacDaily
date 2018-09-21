# -*- coding: utf-8 -*-

import base64
import calendar
import datetime
import functools
import glob
import os
import pathlib
import shlex
import shutil
import subprocess
import sys
import tarfile
import zipfile

# terminal display
reset = '\033[0m'       # reset
bold = '\033[1m'        # bold
under = '\033[4m'       # underline
flash = '\033[5m'       # flash
red = '\033[91m'        # bright red foreground
green = '\033[92m'      # bright green foreground
blue = '\033[96m'       # bright blue foreground
blush = '\033[101m'     # bright red background
purple = '\033[104m'    # bright purple background
length = shutil.get_terminal_size().columns         # terminal length

# terminal commands
python = sys.executable         # Python version
program = ' '.join(sys.argv)    # arguments

# root path
ROOT = os.path.dirname(os.path.abspath(__file__))


class PasswordError(PermissionError):
    def __init__(self, *args, **kwargs):
        sys.tracebacklimit = 0
        super().__init__(*args, **kwargs)


def check(parse):
    @functools.wraps(parse)
    def wrapper():
        config = parse()
        subprocess.run(['sudo', '--reset-timestamp'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        PIPE = make_pipe(config)
        SUDO = subprocess.run(['sudo', '--stdin', '--validate'],
                              stdin=PIPE.stdout, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            SUDO.check_returncode()
        except subprocess.CalledProcessError:
            raise PasswordError(1, f"Invalid password for {config['Account']['username']!r}") from None
        return config
    return wrapper


def beholder(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            print(f'\nmacdaily: {red}error{reset}: operation interrupted', file=sys.stderr)
            exit(130)
        except BaseException as error:
            sys.tracebacklimit = 0
            raise error from None
    return wrapper


def aftermath(logfile, tmpfile=None, command='null', logmode=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except subprocess.TimeoutExpired as error:
                with open(logfile, 'a') as file:
                    file.write(f'\nERR: {error}\n')
                print(f'macdaily: {red}{command}{reset}: operation timeout', file=sys.stderr)
                exit(32)
            except BaseException as error:
                if logmode is not None:
                    subprocess.run(['bash', os.path.join(ROOT, f'lib{command}/aftermath.sh'),
                                    shlex.quote(logfile), shlex.quote(tmpfile), 'true', logmode],
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                sys.tracebacklimit = 0
                raise error from None
        return wrapper
    return decorator


def make_mode(args, file, mode, *, flag=True):
    with open(file, 'a') as logfile:
        logfile.writelines(['\n\n', f'-*- {mode} -*-'.center(80, ' '), '\n\n'])
    if (not args.quiet) and flag:
        print(f'-*- {blue}{mode}{reset} -*-'.center(length, ' '), '\n', sep='')


def sudo_timeout(password):
    yes = make_pipe(password=password)
    grep = subprocess.Popen(['sudo', '--stdin', 'grep', 'timestamp_timeout', '/etc/sudoers'],
                            stdin=yes.stdout, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    sed = subprocess.run(['sed', r's/timestamp_timeout=\([-0-9.]*\)*/\1/'],
                         stdin=grep.stdout, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    return (sed.stdout.strip().decode() or '300')


def make_pipe(config=None, password=None):
    if password is None:
        password = base64.b85decode(config['Account']['password']).decode()
    return subprocess.Popen(['yes', password], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)


def make_path(config, mode, logdate):
    tmppath = os.path.expanduser(config['Path']['tmpdir'])
    logpath = os.path.expanduser(config['Path']['logdir']) + f'/{mode}'
    arcpath = os.path.expanduser(config['Path']['logdir']) + f'/archive/{mode}'
    tarpath = os.path.expanduser(config['Path']['logdir']) + f'/tarfile/{mode}'

    pathlib.Path(arcpath).mkdir(parents=True, exist_ok=True)
    pathlib.Path(tarpath).mkdir(parents=True, exist_ok=True)
    pathlib.Path(tmppath).mkdir(parents=True, exist_ok=True)
    pathlib.Path(f'{logpath}/{logdate}').expanduser().mkdir(parents=True, exist_ok=True)

    dskpath = pathlib.Path(config['Path']['dskdir'])
    if dskpath.exists() and dskpath.is_dir():
        pathlib.Path(config['Path']['arcdir']).mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ['sudo', '--stdin', 'chown', '-R', config['Account']['username'],
         tmppath, os.path.expanduser(config['Path']['logdir'])],
        stdin=make_pipe(config).stdout, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    return tmppath, logpath, arcpath, tarpath


def archive(config, logpath, arcpath, tarpath, logdate, today, mvflag=True):
    filelist = list()
    for subdir in os.listdir(logpath):
        if subdir == '.DS_Store':
            continue
        absdir = os.path.join(logpath, subdir)
        if not os.path.isdir(absdir):
            continue
        if subdir != logdate:
            tarname = f'{arcpath}/{subdir}.tar.gz'
            with tarfile.open(tarname, 'w:gz') as tf:
                abs_src = os.path.abspath(absdir)
                for dirname, _, files in os.walk(absdir):
                    for filename in filter(lambda x: x.endswith('.log'), files):
                        absname = os.path.abspath(os.path.join(dirname, filename))
                        arcname = absname[len(abs_src) + 1:]
                        tf.add(absname, arcname)
                        filelist.append(absname)
                shutil.rmtree(absdir)

    ctime = datetime.datetime.fromtimestamp(os.stat(arcpath).st_birthtime)
    if (today - ctime) > datetime.timedelta(7):
        arcdate = datetime.date.strftime(ctime, '%y%m%d')
        tarname = f'{tarpath}/{arcdate}-{logdate}.tar.bz'
        with tarfile.open(tarname, 'w:bz2') as tf:
            abs_src = os.path.abspath(arcpath)
            for dirname, _, files in os.walk(arcpath):
                for filename in filter(lambda x: x.endswith('.gz'), files):
                    absname = os.path.abspath(os.path.join(dirname, filename))
                    arcname = absname[len(abs_src) + 1:]
                    tf.add(absname, arcname)
                    filelist.append(absname)
            shutil.rmtree(arcpath)

    if mvflag:
        filelist.extend(storage(config, logdate, today))
    return filelist


def storage(config, logdate, today):
    filelist = list()
    tmppath = os.path.expanduser(config['Path']['tmpdir'])
    tarpath = os.path.expanduser(config['Path']['logdir']) + '/tarfile'
    dskpath = pathlib.Path(config['Path']['dskdir'])
    if dskpath.exists() and dskpath.is_dir():
        ctime = datetime.datetime.fromtimestamp(os.stat(tarpath).st_birthtime)
        delta = today - ctime
        if delta > datetime.timedelta(calendar.monthrange(today.year, today.month)[1]):
            arcdate = datetime.date.strftime(ctime, '%y%m%d')
            tarname = f'{tmppath}/{arcdate}-{logdate}.tar.xz'
            with tarfile.open(tarname, 'w:xz') as tf:
                abs_src = os.path.abspath(tarpath)
                for dirname, _, files in os.walk(tarpath):
                    for filename in filter(lambda x: x.endswith('.bz'), files):
                        absname = os.path.abspath(os.path.join(dirname, filename))
                        arcname = absname[len(abs_src) + 1:]
                        tf.add(absname, arcname)
                        filelist.append(absname)
                shutil.rmtree(tarpath)

            arcfile = os.path.expanduser(config['Path']['arcdir']) + '/archive.zip'
            with zipfile.ZipFile(arcfile, 'a', zipfile.ZIP_DEFLATED) as zf:
                arcname = os.path.split(tarname)[1]
                zf.write(tarname, arcname)
                filelist.append(tarname)
                os.remove(tarname)
    return filelist
