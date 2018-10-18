# -*- coding: utf-8 -*-

import base64
import contextlib
import copy
import os
import pwd
import shutil
import sys

from macdaily.util.colours import blue, reset, length

try:
    import pathlib2 as pathlib
except ImportError:
    import pathlib

try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess

# version string
__version__ = '2018.10.18.dev1'

# terminal commands
python = sys.executable         # Python version
program = ' '.join(sys.argv)    # arguments

# environment macros
ROOT = os.path.dirname(os.path.abspath(__file__))
SHELL = os.environ.get('SHELL', shutil.which('sh'))


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
    pathlib.Path(os.path.join(logpath, logdate)).mkdir(
        parents=True, exist_ok=True)

    dskpath = pathlib.Path(dskdir)
    if dskpath.exists() and dskpath.is_dir():
        pathlib.Path(arcdir).mkdir(parents=True, exist_ok=True)

    with make_pipe(config) as PIPE:
        subprocess.run(['sudo', '--stdin', 'chown', '-R', config['Account']['username'], tmppath, logdir],
                       stdin=PIPE.stdout, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return tmppath, logpath, arcpath, tarpath


def make_pipe(config=None, password=None):
    if password is None:
        password = base64.b85decode(config['Account']['password']).decode()
    return subprocess.Popen(['yes', password], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)


def parse_mode(args, config):
    temp = copy.deepcopy(args)
    for mode in config['Mode'].keys():
        if (not config['Mode'].getboolean(mode, fallback=False)):
            setattr(temp, f'no_{mode}', True)
    if isinstance(args.mode, str):
        temp.mode = [args.mode]
    if 'all' in args.mode:
        temp.mode = ['all']
    return temp


def sudo_timeout(password):
    with make_pipe(password=password) as yes:
        grep = subprocess.Popen(['sudo', '--stdin', 'grep', 'timestamp_timeout', '/etc/sudoers'],
                                stdin=yes.stdout, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        sed = subprocess.run(['sed', r's/timestamp_timeout=\([-0-9.]*\)*/\1/'],
                             stdin=grep.stdout, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    return (sed.stdout.strip().decode() or '300')
