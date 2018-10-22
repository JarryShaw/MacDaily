# -*- coding: utf-8 -*-

import calendar
import datetime
import os
import shutil
import tarfile
import zipfile

try:
    import pathlib2 as pathlib
except ImportError:
    import pathlib


def archive(config, logpath, arcpath, tarpath, logdate, today, *, mvflag=True):
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
        arcdate = datetime.date.strftime(ctime, r'%y%m%d')
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
    tarpath = os.path.expanduser(os.path.join(config['Path']['logdir'], 'tarfile'))

    dskpath = pathlib.Path(config['Path']['dskdir'])
    if dskpath.exists() and dskpath.is_dir():
        ctime = datetime.datetime.fromtimestamp(os.stat(tarpath).st_birthtime)
        if (today - ctime) > datetime.timedelta(calendar.monthrange(today.year, today.month)[1]):
            arcdate = datetime.date.strftime(ctime, r'%y%m%d')
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

            arcfile = os.path.expanduser(os.path.join(config['Path']['arcdir'], 'archive.zip'))
            with zipfile.ZipFile(arcfile, 'a', zipfile.ZIP_DEFLATED) as zf:
                arcname = os.path.split(tarname)[1]
                zf.write(tarname, arcname)
                filelist.append(tarname)
                os.remove(tarname)
    return filelist
