# -*- coding: utf-8 -*-

import calendar
import datetime
import glob
import os
import shutil
import tarfile
import tempfile
import zipfile

try:
    import pathlib2 as pathlib
except ImportError:
    import pathlib


def archive(config, mode, today, zipfile=True):
    logdir = config['Path']['logdir']
    logdate = datetime.date.strftime(today, r'%y%m%d')

    logpath = pathlib.Path(os.path.join(logdir, mode))
    arcpath = pathlib.Path(os.path.join(logdir, 'archive', mode))
    tarpath = pathlib.Path(os.path.join(logdir, 'tarfile', mode))

    logpath.mkdir(parents=True, exist_ok=True)
    arcpath.mkdir(parents=True, exist_ok=True)
    tarpath.mkdir(parents=True, exist_ok=True)

    filelist = list()
    for subdir in filter(lambda subdir: os.path.isdir(
            os.path.join(logpath, subdir)), os.listdir(logpath)):
        if subdir == logdate:
            continue
        glob_list = glob.glob(os.path.join(absdir, '*.log'))
        if glob_list:
            absdir = os.path.abspath(os.path.join(logpath, subdir))
            tarname = os.path.join(arcpath, f'{subdir}.tar.gz')
            with tarfile.open(tarname, 'w:gz') as gz:
                for absname in glob_list:
                    arcname = os.path.split(absname)[1]
                    gz.add(absname, arcname)
                    filelist.append(absname)
        shutil.rmtree(absdir)

    ctime = datetime.datetime.fromtimestamp(os.stat(arcpath).st_birthtime)
    if (today - ctime) > datetime.timedelta(days=7):
        glob_list = glob.glob(os.path.join(arcpath, '*.tar.gz'))
        if glob_list:
            arcdate = datetime.date.strftime(ctime, r'%y%m%d')
            tarname = os.path.join(tarpath, f'{arcdate}-{logdate}.tar.xz')
            with tarfile.open(tarname, 'w:xz') as xz:
                for absname in glob_list:
                    arcname = os.path.split(absname)[1]
                    xz.add(absname, arcname)
                    filelist.append(absname)
        shutil.rmtree(arcpath)

    if zipfile:
        filelist.extend(storage(config, today))
    return filelist


def storage(config, today):
    arclist = list()
    logdate = datetime.date.strftime(today, r'%y%m%d')
    tarpath = os.path.join(config['Path']['logdir'], 'tarfile')

    if not os.path.isdir(config['Path']['dskdir']):
        return arclist
    if not os.path.isdir(tarpath):
        return arclist

    days = calendar.monthrange(year=today.year, month=today.month)[1]
    ctime = datetime.datetime.fromtimestamp(os.stat(tarpath).st_birthtime)
    if (today - ctime) > datetime.timedelta(days=days):
        glob_list = glob.glob(os.path.join(tarpath, '*/*.tar.xz'))
        if glob_list:
            with tempfile.TemporaryDirectory() as tmppath:
                arcdate = datetime.date.strftime(ctime, r'%y%m%d')
                tarname = os.path.join(tmppath, f'{arcdate}-{logdate}.tar.bz')
                with tarfile.open(tarname, 'w:bz2') as bz:
                    for absname in glob_list:
                        arcname = pathlib.Path(absname).relative_to(tarpath)
                        bz.add(absname, arcname)
                        arclist.append(absname)

                arcfile = os.path.join(config['Path']['arcdir'], 'archive.zip')
                with zipfile.ZipFile(arcfile, 'a', zipfile.ZIP_DEFLATED) as zf:
                    arcname = os.path.split(tarname)[1]
                    zf.write(tarname, arcname)
        shutil.rmtree(tarpath)
    return arclist
