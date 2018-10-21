# -*- coding: utf-8 -*-

import base64
import contextlib
import os
import pwd

from macdaily.util.colour import blue, length, reset

try:
    import pathlib2 as pathlib
except ImportError:
    import pathlib

try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess


def get_pass(config, logname):
    with make_pipe(config) as PIPE:
        USER = config['Account']['username']
        PASS = base64.b64encode(PIPE.stdout.readline().strip()).decode()
        if pwd.getpwuid(os.stat(logname).st_uid) != USER:
            subprocess.run(['sudo', 'chown', '-R', USER, config['Path']['tmpdir'], config['Path']['logdir']],
                           stdin=PIPE.stdout, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return PASS


def make_context(args, devnull):
    if args.quiet:
        return contextlib.redirect_stdout(devnull)
    return contextlib.nullcontext()


def make_mode(args, file, mode, *, flag=True):
    with open(file, 'a') as logfile:
        logfile.writelines(['\n\n', f'-*- {mode} -*-'.center(80, ' '), '\n\n'])
    if flag:
        print(f'-*- {blue}{mode}{reset} -*-'.center(length, ' '), '\n', sep='')


def make_path(config, mode, logdate):
    tmpdir = os.path.expanduser(config['Path']['tmpdir'])
    logdir = os.path.expanduser(config['Path']['logdir'])
    dskdir = os.path.expanduser(config['Path']['dskdir'])
    arcdir = os.path.expanduser(config['Path']['arcdir'])

    tmppath = tmpdir
    logpath = os.path.join(logdir, mode)
    arcpath = os.path.join(logdir, 'archive', mode)
    tarpath = os.path.join(logdir, 'tarfile', mode)

    pathlib.Path(arcpath).mkdir(parents=True, exist_ok=True)
    pathlib.Path(tarpath).mkdir(parents=True, exist_ok=True)
    pathlib.Path(tmppath).mkdir(parents=True, exist_ok=True)
    pathlib.Path(os.path.join(logpath, logdate)).mkdir(parents=True, exist_ok=True)

    dskpath = pathlib.Path(dskdir)
    if dskpath.exists() and dskpath.is_dir():
        pathlib.Path(arcdir).mkdir(parents=True, exist_ok=True)

    with make_pipe(config) as PIPE:
        subprocess.check_call(['sudo', '--stdin', '--prompt=""',
                               'chown', '-R', config['Account']['username'], tmppath, logdir],
                              stdin=PIPE.stdout, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return tmppath, logpath, arcpath, tarpath


def make_pipe(config=None, password=None):
    if password is None:
        password = base64.b85decode(config['Account']['password']).decode()
    return subprocess.Popen(['yes', password], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
