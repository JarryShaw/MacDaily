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


def archive(config, mode, today, mvflag=True):
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
        absdir = os.path.abspath(os.path.join(logpath, subdir))
        tarname = os.path.join(arcpath, f'{subdir}.tar.gz')
        with tarfile.open(tarname, 'w:gz') as gz:
            for absname in glob.glob(os.path.join(absdir, '*.log')):
                arcname = os.path.split(absname)[1]
                gz.add(absname, arcname)
                filelist.append(absname)
        shutil.rmtree(absdir)

    ctime = datetime.datetime.fromtimestamp(os.stat(arcpath).st_birthtime)
    if (today - ctime) > datetime.timedelta(days=7):
        arcdate = datetime.date.strftime(ctime, r'%y%m%d')
        tarname = os.path.join(tarpath, f'{arcdate}-{logdate}.tar.xz')
        with tarfile.open(tarname, 'w:xz') as xz:
            for absname in glob.glob(os.path.join(arcpath, '*.tar.gz')):
                arcname = os.path.split(absname)[1]
                xz.add(absname, arcname)
                filelist.append(absname)
        shutil.rmtree(arcpath)

    if mvflag:
        filelist.extend(storage(config, today))
    return filelist


def storage(config, today):
    filelist = list()
    logdate = datetime.date.strftime(today, r'%y%m%d')
    tarpath = os.path.join(config['Path']['logdir'], 'tarfile')

    if not os.path.isdir(config['Path']['dskdir']):
        return filelist
    if not os.path.isdir(tarpath):
        return filelist

    days = calendar.monthrange(year=today.year, month=today.month)[1]
    ctime = datetime.datetime.fromtimestamp(os.stat(tarpath).st_birthtime)
    if (today - ctime) > datetime.timedelta(days=days):
        with tempfile.TemporaryDirectory() as tmppath:
            arcdate = datetime.date.strftime(ctime, r'%y%m%d')
            tarname = os.path.join(tmppath, f'{arcdate}-{logdate}.tar.bz')
            with tarfile.open(tarname, 'w:bz2') as bz:
                for absname in glob.glob(os.path.join(tarpath, '*/*.tar.xz')):
                    arcname = pathlib.Path(absname).relative_to(tarpath)
                    bz.add(absname, arcname)
                    filelist.append(absname)

            arcfile = os.path.join(config['Path']['arcdir'], 'archive.zip')
            with zipfile.ZipFile(arcfile, 'a', zipfile.ZIP_DEFLATED) as zf:
                arcname = os.path.split(tarname)[1]
                zf.write(tarname, arcname)
                filelist.append(tarname)
        shutil.rmtree(tarpath)
    return filelist
