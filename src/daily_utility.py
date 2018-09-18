# -*- coding: utf-8 -*-


import base64
import calendar
import datetime
import functools
import os
import pathlib
import shlex
import shutil
import subprocess
import sys
import tarfile
import zipfile


__all__ = ['beholder', 'aftermath', 'make_pipe', 'make_path', 'archive', 'storage']


# terminal display
reset  = '\033[0m'      # reset
red    = '\033[91m'     # bright red foreground


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
        subprocess.run(['sudo', '--reset-timestamp'],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        PIPE = make_pipe(config)
        SUDO = subprocess.run(['sudo', '--stdin', '--validate'],
                              stdin=PIPE.stdout, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if SUDO.returncode == 0:    return config
        raise PasswordError(1, "Invalid password for {!r}".format(config['Account']['username']))
    return wrapper


def beholder(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            print('\nmacdaily: {}error{}: operation interrupted'.format(red, reset), file=sys.stderr)
            sys.exit(130)
        except BaseException as error:
            sys.tracebacklimit = 0
            raise error from None
    return wrapper


def aftermath(*, logfile, tmpfile, command, logmode='null'):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except subprocess.TimeoutExpired as error:
                with open(logfile, 'a') as file:
                    file.write('\nERR: {}\n'.format(error))
                print('macdaily: {}{}{}: operation timeout'.format(red, command, reset), file=sys.stderr)
                sys.exit(32)
            except BaseException as error:
                subprocess.run(['bash', os.path.join(ROOT, 'lib{}/aftermath.sh'.format(command)), shlex.quote(logfile), shlex.quote(tmpfile), 'true', logmode],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                sys.tracebacklimit = 0
                raise error from None
        return wrapper
    return decorator


def sudo_timeout(password):
    yes = make_pipe(password=password)
    grep = subprocess.Popen(['sudo', '--stdin', 'grep', 'timestamp_timeout', '/etc/sudoers'], stdin=yes.stdout, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    sed = subprocess.run(['sed', r's/timestamp_timeout=\([-0-9.]*\)*/\1/'], stdin=grep.stdout, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    return (sed.stdout.strip().decode() or '5m')


def make_pipe(config=None, *, password=None):
    if password is None:
        password = base64.b85decode(config['Account']['password']).decode()
    return subprocess.Popen(['yes', password], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)


def make_path(config, *, mode, logdate):
    tmppath = os.path.expanduser(config['Path']['tmpdir'])
    logpath = os.path.expanduser(config['Path']['logdir']) + '/{}'.format(mode)
    arcpath = os.path.expanduser(config['Path']['logdir']) + '/archive/{}'.format(mode)
    tarpath = os.path.expanduser(config['Path']['logdir']) + '/tarfile/{}'.format(mode)

    pathlib.Path(arcpath).mkdir(parents=True, exist_ok=True)
    pathlib.Path(tarpath).mkdir(parents=True, exist_ok=True)
    pathlib.Path(tmppath).mkdir(parents=True, exist_ok=True)
    pathlib.Path('{}/{}'.format(logpath, logdate)).expanduser().mkdir(parents=True, exist_ok=True)

    dskpath = pathlib.Path(config['Path']['dskdir'])
    if dskpath.exists() and dskpath.is_dir():
        pathlib.Path(config['Path']['arcdir']).mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ['sudo', '--stdin', 'chown', '-R', config['Account']['username'], tmppath, os.path.expanduser(config['Path']['logdir'])],
        stdin=make_pipe(config).stdout, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    return tmppath, logpath, arcpath, tarpath


def archive(config, *, logpath, arcpath, tarpath, logdate, today, mvflag=True):
    filelist = list()
    for subdir in os.listdir(logpath):
        if subdir == '.DS_Store':
            continue
        absdir = os.path.join(logpath, subdir)
        if not os.path.isdir(absdir):
            continue
        if subdir != logdate:
            tarname = '{}/{}.tar.gz'.format(arcpath, subdir)
            with tarfile.open(tarname, 'w:gz') as tf:
                abs_src = os.path.abspath(absdir)
                for dirname, subdirs, files in os.walk(absdir):
                    for filename in files:
                        if filename == '.DS_Store': continue
                        name, ext = os.path.splitext(filename)
                        if ext != '.log':           continue
                        absname = os.path.abspath(os.path.join(dirname, filename))
                        arcname = absname[len(abs_src) + 1:]
                        tf.add(absname, arcname)
                        filelist.append(absname)
                shutil.rmtree(absdir)

    ctime = datetime.datetime.fromtimestamp(os.stat(arcpath).st_birthtime)
    delta = today - ctime
    if delta > datetime.timedelta(7):
        arcdate = datetime.date.strftime(ctime, '%y%m%d')
        tarname = '{}/{}-{}.tar.bz'.format(tarpath, arcdate, logdate)
        with tarfile.open(tarname, 'w:bz2') as tf:
            abs_src = os.path.abspath(arcpath)
            for dirname, subdirs, files in os.walk(arcpath):
                for filename in files:
                    if filename == '.DS_Store': continue
                    name, ext = os.path.splitext(filename)
                    if ext != '.gz':            continue
                    absname = os.path.abspath(os.path.join(dirname, filename))
                    arcname = absname[len(abs_src) + 1:]
                    tf.add(absname, arcname)
                    filelist.append(absname)
            shutil.rmtree(arcpath)

    if mvflag:
        filelist.extend(storage(config, logdate=logdate, today=today))
    return filelist


def storage(config, *, logdate, today):
    filelist = list()
    tmppath = os.path.expanduser(config['Path']['tmpdir'])
    tarpath = os.path.expanduser(config['Path']['logdir']) + '/tarfile'
    dskpath = pathlib.Path(config['Path']['dskdir'])
    if dskpath.exists() and dskpath.is_dir():
        ctime = datetime.datetime.fromtimestamp(os.stat(tarpath).st_birthtime)
        delta = today - ctime
        if delta > datetime.timedelta(calendar.monthrange(today.year, today.month)[1]):
            arcdate = datetime.date.strftime(ctime, '%y%m%d')
            tarname = '{}/{}-{}.tar.xz'.format(tmppath, arcdate, logdate)
            with tarfile.open(tarname, 'w:xz') as tf:
                abs_src = os.path.abspath(tarpath)
                for dirname, subdirs, files in os.walk(tarpath):
                    for filename in files:
                        if filename == '.DS_Store': continue
                        name, ext = os.path.splitext(filename)
                        if ext != '.bz':            continue
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
