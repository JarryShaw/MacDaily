# -*- coding: utf-8 -*-

import calendar
import datetime
import distutils.version  # pylint: disable=no-name-in-module,import-error
import glob
import os
import shutil
import tarfile
import tempfile
import zipfile

from macdaily.util.compat import pathlib
from macdaily.util.const.macro import VERSION
from macdaily.util.const.term import reset, under
from macdaily.util.tools.get import get_logdir
from macdaily.util.tools.print import print_info, print_scpt, print_text


def make_archive(config, mode, today, zipfile=True, quiet=False, verbose=False, logfile=os.devnull):  # pylint: disable=redefined-outer-name
    logdir = config['Path']['logdir']
    logdate = datetime.date.strftime(today, r'%y%m%d')

    logpath = pathlib.Path(os.path.join(logdir, mode))
    arcpath = pathlib.Path(os.path.join(logdir, 'arcfile', mode))
    tarpath = pathlib.Path(os.path.join(logdir, 'tarfile', mode))

    logpath.mkdir(parents=True, exist_ok=True)
    arcpath.mkdir(parents=True, exist_ok=True)
    tarpath.mkdir(parents=True, exist_ok=True)

    text = f'Moving ancient logs into {under}GNU Zip Archives{reset}'
    print_info(text, logfile, redirect=quiet)

    filelist = list()
    for subdir in filter(lambda subdir: os.path.isdir(os.path.join(logpath, subdir)), os.listdir(logpath)):
        if subdir == logdate:
            continue
        absdir = os.path.abspath(os.path.join(logpath, subdir))
        glob_list = glob.glob(os.path.join(absdir, '*.log'))
        if glob_list:
            tarname = os.path.join(arcpath, f'{subdir}.tar.gz')
            if verbose:
                print_scpt(f'tar -czf {tarname} {absdir}', logfile, redirect=quiet)
            else:
                print_scpt(f'tar -czvf {tarname} {absdir}', logfile, redirect=verbose)
            with tarfile.open(tarname, 'w:gz') as gz:
                for absname in glob_list:
                    arcname = os.path.split(absname)[1]
                    gz.add(absname, arcname)
                    filelist.append(absname)
                    print_text(absname, logfile, redirect=verbose)
        shutil.rmtree(absdir)

    misc_path = os.path.join(get_logdir(), 'misc')
    if os.path.isdir(misc_path):
        this_version = distutils.version.StrictVersion(VERSION)  # pylint: disable=no-member
        for entry in os.scandir(misc_path):
            if not entry.is_dir:
                continue
            try:
                that_version = distutils.version.StrictVersion(entry.name)  # pylint: disable=no-member
                if this_version <= that_version:
                    continue
            except ValueError:
                pass
            glob_list = glob.glob(os.path.join(entry.path, '*.log'))
            if glob_list:
                tarname = os.path.join(arcpath, f'{entry.name}.tar.gz')
                with tarfile.open(tarname, 'w:gz') as gz:
                    for absname in glob_list:
                        arcname = os.path.split(absname)[1]
                        gz.add(absname, arcname)
            shutil.rmtree(entry.path)

    text = f'Moving ancient archives into {under}XZ Compressed Archives{reset}'
    print_info(text, logfile, redirect=quiet)

    ctime = datetime.datetime.fromtimestamp(os.stat(arcpath).st_birthtime)
    if (today - ctime) > datetime.timedelta(days=7):
        glob_list = glob.glob(os.path.join(arcpath, '*.tar.gz'))
        if glob_list:
            arcdate = datetime.date.strftime(ctime, r'%y%m%d')
            tarname = os.path.join(tarpath, f'{arcdate}-{logdate}.tar.xz')
            if verbose:
                print_scpt(f'tar -cJf {tarname} {arcpath}', logfile, redirect=quiet)
            else:
                print_scpt(f'tar -cJvf {tarname} {arcpath}', logfile, redirect=verbose)
            with tarfile.open(tarname, 'w:xz') as xz:
                for absname in glob_list:
                    arcname = os.path.split(absname)[1]
                    xz.add(absname, arcname)
                    filelist.append(absname)
                    print_text(absname, logfile, redirect=verbose)
        shutil.rmtree(arcpath)

    if zipfile:  # pylint:disable=redefined-outer-name
        filelist.extend(make_storage(config, today, quiet, verbose, logfile))
    return filelist


def make_storage(config, today, quiet=False, verbose=False, logfile=os.devnull):
    arclist = list()
    logdate = datetime.date.strftime(today, r'%y%m%d')

    dskpath = config['Path']['dskdir']
    tarpath = os.path.join(config['Path']['logdir'], 'tarfile')

    if not os.path.isdir(dskpath):
        return arclist
    if not os.path.isdir(tarpath):
        return arclist

    text = f'Storing ancient archives at external hard disk {under}{dskpath}{reset}'
    print_info(text, logfile, redirect=quiet)

    days = calendar.monthrange(year=today.year, month=today.month)[1]
    ctime = datetime.datetime.fromtimestamp(os.stat(tarpath).st_birthtime)
    if (today - ctime) > datetime.timedelta(days=days):
        glob_list = glob.glob(os.path.join(tarpath, '*/*.tar.xz'))
        if glob_list:
            with tempfile.TemporaryDirectory() as tmppath:
                arcdate = datetime.date.strftime(ctime, r'%y%m%d')
                tarname = os.path.join(tmppath, f'{arcdate}-{logdate}.tar.bz')
                if verbose:
                    print_scpt(f'tar -cjf {tarname} {tarpath}', logfile, redirect=quiet)
                else:
                    print_scpt(f'tar -cjvf {tarname} {tarpath}', logfile, redirect=verbose)
                with tarfile.open(tarname, 'w:bz2') as bz:
                    for absname in glob_list:
                        arcname = pathlib.Path(absname).relative_to(tarpath)
                        bz.add(absname, arcname)
                        arclist.append(absname)
                        print_text(absname, logfile, redirect=verbose)

                arcfile = os.path.join(config['Path']['arcdir'], 'archive.zip')
                if verbose:
                    print_scpt(f'tar -cZf {arcfile} {tarname}', logfile, redirect=quiet)
                else:
                    print_scpt(f'tar -cZvf {arcfile} {tarname}', logfile, redirect=verbose)
                with zipfile.ZipFile(arcfile, 'a', zipfile.ZIP_DEFLATED) as zf:
                    arcname = os.path.split(tarname)[1]
                    zf.write(tarname, arcname)
                    print_text(tarname, logfile, redirect=verbose)
        shutil.rmtree(tarpath)
    return arclist
