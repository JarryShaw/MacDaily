# -*- coding: utf-8 -*-

import base64
import calendar
import contextlib
import copy
import datetime
import functools
import glob
import os
import platform
import pwd
import re
import shlex
import shutil
import sys
import tarfile
import traceback
import zipfile

import ptyng

try:
    import pathlib2 as pathlib
except ImportError:
    import pathlib

try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess

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

# environment macros
ROOT = os.path.dirname(os.path.abspath(__file__))
SHELL = os.environ.get('SHELL', shutil.which('sh'))


class ModeError(NameError):
    pass


class UnsupportedOS(RuntimeError):
    pass


class PasswordError(PermissionError):
    pass


class ConfigNotFoundError(FileNotFoundError):
    pass


def check(parse):
    @functools.wraps(parse)
    def wrapper():
        config = parse()
        subprocess.run(['sudo', '--reset-timestamp'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            with make_pipe(config) as PIPE:
                subprocess.check_call(['sudo', '--stdin', '--validate'],
                                      stdin=PIPE.stdout, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            raise PasswordError(1, "Invalid password for {!r}".format(config['Account']['username'])) from None
        return config
    return wrapper


def beholder(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if platform.system() != 'Darwin':
            raise UnsupportedOS('macdaily: script runs only on macOS')
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            print('\nmacdaily: {}error{}: operation interrupted\n'.format(red, reset), file=sys.stderr)
            raise
    return wrapper


def aftermath(logfile, tmpfile=None, command=None, logmode='null'):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except subprocess.TimeoutExpired:
                with open(logfile, 'a') as file:
                    file.write('\nERR: {}\n'.format(traceback.format_exc().splitlines()[-1]))
                if command is not None:
                    print('\nmacdaily: {}{}{}: operation timeout\n'.format(red, command, reset), file=sys.stderr)
                raise
            except BaseException:
                path = os.path.join(ROOT, 'lib{}/aftermath.sh'.format(command))
                if os.path.isfile(path):
                    subprocess.run(['bash', path, shlex.quote(logfile), shlex.quote(tmpfile), 'true', logmode],
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                raise
        return wrapper
    return decorator


def script(argv=SHELL, file='typescript', *, timeout=None, shell=False, executable=None):
    def stdin_read(fd):
        text = '\x00'
        data = list()
        while text and text != '\n':
            text = os.read(fd, 1)
            data.append(text)
        return ''.join(filter(None, data))

    if shell:
        argv = [SHELL, '-c'] + argv
    if executable:
        argv[0] = executable

    with open(file, 'a') as script:
        def master_read(fd):
            data = os.read(fd, 1024)
            text = re.sub(r'(\x1b\[[0-9][0-9;]*m)|(\^D\x08\x08)', r'', data, flags=re.IGNORECASE)
            script.write(text)
            return data
        ptyng.spawn(argv, master_read, stdin_read, timeout)


def sudo_timeout(password):
    with make_pipe(password=password) as yes:
        grep = subprocess.Popen(['sudo', '--stdin', 'grep', 'timestamp_timeout', '/etc/sudoers'],
                                stdin=yes.stdout, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        sed = subprocess.run(['sed', r's/timestamp_timeout=\([-0-9.]*\)*/\1/'],
                             stdin=grep.stdout, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    return (sed.stdout.strip().decode() or '300')


def record_args(args, today, logfile):
    logfile.write(datetime.date.strftime(today, ' %+ ').center(80, '—'))
    logfile.write('\n\nCMD: {} {}'.format(python, program))
    logfile.write("\n\n{}\n\n".format('-*- Arguments - *-'.center(80, ' ')))
    for key, value in vars(args).items():
        logfile.write('ARG: {} = {}\n'.format(key, value))


def get_pass(config, logname):
    with make_pipe(config) as PIPE:
        USER = config['Account']['username']
        PASS = base64.b64encode(PIPE.stdout.readline().strip()).decode()
        if pwd.getpwuid(os.stat(logname).st_uid) != USER:
            subprocess.run(['sudo', 'chown', '-R', USER, config['Path']['tmpdir'], config['Path']['logdir']],
                           stdin=PIPE.stdout, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return PASS


def parse_mode(args, config):
    temp = copy.deepcopy(args)
    for mode in config['Mode'].keys():
        if (not config['Mode'].getboolean(mode, fallback=False)):
            setattr(temp, 'no_{}'.format(mode), True)
    if isinstance(args.mode, str):
        temp.mode = [args.mode]
    if 'all' in args.mode:
        temp.mode = ['all']
    return temp


def make_mode(args, file, mode, *, flag=True):
    with open(file, 'a') as logfile:
        logfile.writelines(['\n\n', '-*- {} -*-'.format(mode).center(80, ' '), '\n\n'])
    if flag:
        print('-*- {}{}{} -*-'.format(blue, mode, reset).center(length, ' '), '\n', sep='')


def make_pipe(config=None, password=None):
    if password is None:
        password = base64.b85decode(config['Account']['password']).decode()
    return subprocess.Popen(['yes', password], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)


def make_context(args, devnull):
    if args.quiet:
        return contextlib.redirect_stdout(devnull)
    return contextlib.nullcontext()


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
        subprocess.run(['sudo', '--stdin', 'chown', '-R', config['Account']['username'], tmppath, logdir],
                       stdin=PIPE.stdout, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return tmppath, logpath, arcpath, tarpath


def archive(config, logpath, arcpath, tarpath, logdate, today, *, mvflag=True):
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
        tarname = '{}/{}-{}.tar.bz'.format(tarpath, arcdate, logdate)
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
            tarname = '{}/{}-{}.tar.xz'.format(tmppath, arcdate, logdate)
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
