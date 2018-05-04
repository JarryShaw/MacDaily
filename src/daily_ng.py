# -*- coding: utf-8 -*-


import calendar
import datetime
import functools
import os
import pathlib
import shlex
import shutil
import subprocess
import tarfile
import zipfile


__all__ = ['make_path', 'aftermath', 'archive', 'storage']


def make_path(config, *, mode, logdate):
    tmppath = config['Path']['tmpdir']
    logpath = config['Path']['logdir'] + f'/{mode}'
    arcpath = config['Path']['logdir'] + f'/archive/{mode}'
    tarpath = config['Path']['logdir'] + f'/tarfile/{mode}'

    pathlib.Path(arcpath).mkdir(parents=True, exist_ok=True)
    pathlib.Path(tarpath).mkdir(parents=True, exist_ok=True)
    pathlib.Path(tmppath).mkdir(parents=True, exist_ok=True)
    pathlib.Path(f'{logpath}/{logdate}').mkdir(parents=True, exist_ok=True)

    dskpath = pathlib.Path(config['Path']['dskdir'])
    if dskpath.exists() and dskpath.is_dir():
        pathlib.Path(config['Path']['arcdir']).mkdir(parents=True, exist_ok=True)

    return tmppath, logpath, arcpath, tarpath


def aftermath(*, logfile, tmpfile, command):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except BaseException as error:
                subprocess.run(['bash', 'lib{command}/aftermath.sh', shlex.quote(logfile), shlex.quote(tmpfile), 'true'])
                raise error from None
        return wrapper
    return decorator


def archive(*, logpath, arcpath, tarpath, logdate, today, storage=True):
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
                for dirname, subdirs, files in os.walk(absdir):
                    for filename in files:
                        if filename == '.DS_Store': continue
                        name, ext = os.path.splitext(filename)
                        if ext != '.log':           continue
                        absname = os.path.abspath(os.path.join(dirname, filename))
                        arcname = absname[len(abs_src) + 1:]
                        tf.add(absname, arcname)
                        filelist.append(arcname)
                shutil.rmtree(absdir)

    ctime = datetime.datetime.fromtimestamp(os.stat(arcpath).st_birthtime)
    delta = today - ctime
    if delta > datetime.timedelta(7):
        arcdate = datetime.date.strftime(ctime, '%y%m%d')
        tarname = f'{tarpath}/{arcdate}-{logdate}.tar.bz'
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
                    filelist.append(arcname)
            shutil.rmtree(arcpath)

    if storage:
        filelist += storage(logdate=logdate, today=today)
    return filelist


def storage(*, logdate, today):
    filelist = list()
    tmppath = config['Path']['tmpdir']
    tarpath = config['Path']['logdir'] + '/tarfile'
    dskpath = pathlib.Path(config['Path']['dskdir'])
    if dskpath.exists() and dskpath.is_dir():
        ctime = datetime.datetime.fromtimestamp(os.stat(tarpath).st_birthtime)
        delta = today - ctime
        if delta > datetime.timedelta(calendar.monthrange(today.year, today.month)[1]):
            arcdate = datetime.date.strftime(ctime, '%y%m%d')
            tarname = f'{tmppath}/{arcdate}-{logdate}.tar.xz'
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
                        filelist.append(arcname)
                shutil.rmtree(tarpath)

            arcfile = config['Path']['arcdir'] + '/archive.zip'
            with zipfile.ZipFile(arcfile, 'a', zipfile.ZIP_DEFLATED) as zf:
                arcname = os.path.split(tarname)[1]
                zf.write(tarname, arcname)
                filelist.append(arcname)
                os.remove(tarname)
    return filelist
