# -*- coding: utf-8 -*-

import contextlib
import datetime
import functools
import getpass
import os
import platform
import re
import sys

import ptyng

from macdaily.util.const import (SHELL, blue, bold, dim, grey, program, purple,
                                 python, red, reset)
from macdaily.util.error import UnsupportedOS


def beholder(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if platform.system() != 'Darwin':
            raise UnsupportedOS('macdaily: error: script runs only on macOS')
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            print('macdaily: {}error{}: operation interrupted'.format(red, reset), file=sys.stderr)
            sys.tracebacklimit = 0
            raise
    return wrapper


def date():
    now = datetime.datetime.now()
    txt = datetime.datetime.strftime(now, '%+')
    return txt


def make_context(devnull, redirect=False):
    if redirect:
        return contextlib.redirect_stdout(devnull)
    return contextlib.nullcontext()


def make_description(command):
    def desc(singular):
        if singular:
            return command.desc[0]
        else:
            return command.desc[1]
    return desc


def print_info(text, file, redirect=False):
    flag = text.endswith(os.linesep)
    if not redirect:
        end = str() if flag else os.linesep
        print('{}{}|💼|{} {}{}{}'.format(bold, blue, reset, bold, text, reset), end=end)
    with open(file, 'a') as fd:
        context = re.sub(r'(\033\[[0-9][0-9;]*m)|(\^D\x08\x08)', r'',
                         (text if flag else '{}{}'.format(text, os.linesep)), flags=re.IGNORECASE)
        fd.write('|💼| {}'.format(context))


def print_misc(text, file, redirect=False):
    flag = text.endswith(os.linesep)
    if not redirect:
        end = str() if flag else os.linesep
        print('{}{}|📌|{} {}{}{}'.format(bold, grey, reset, bold, text, reset), end=end)
    with open(file, 'a') as fd:
        context = re.sub(r'(\033\[[0-9][0-9;]*m)|(\^D\x08\x08)', r'',
                         (text if flag else '{}{}'.format(text, os.linesep)), flags=re.IGNORECASE)
        fd.write('|📌| {}'.format(context))


def print_scpt(text, file, redirect=False):
    if not isinstance(text, str):
        text = ' '.join(text)
    flag = text.endswith(os.linesep)
    if not redirect:
        end = str() if flag else os.linesep
        print('{}{}|📜|{} {}{}{}'.format(bold, purple, reset, bold, text, reset), end=end)
    with open(file, 'a') as fd:
        context = re.sub(r'(\033\[[0-9][0-9;]*m)|(\^D\x08\x08)', r'',
                         (text if flag else '{}{}'.format(text, os.linesep)), flags=re.IGNORECASE)
        fd.write('|📜| {}'.format(context))


def print_term(text, file, redirect=False):
    flag = text.endswith(os.linesep)
    if not redirect:
        end = str() if flag else os.linesep
        print(text, end=end)
    with open(file, 'a') as fd:
        context = re.sub(r'(\033\[[0-9][0-9;]*m)|(\^D\x08\x08)', r'',
                         (text if flag else '{}{}'.format(text, os.linesep)), flags=re.IGNORECASE)
        fd.write(context)


def print_text(text, file, redirect=False):
    flag = text.endswith(os.linesep)
    if not redirect:
        end = str() if flag else os.linesep
        print('{}{}{}'.format(dim, text, reset), end=end)
    with open(file, 'a') as fd:
        context = re.sub(r'(\033\[[0-9][0-9;]*m)|(\^D\x08\x08)', r'',
                         (text if flag else '{}{}'.format(text, os.linesep)), flags=re.IGNORECASE)
        fd.write(context)


def record(file, args, today, config, redirect=False):
    # record program arguments
    print_misc('{} {}'.format(python, program), file, redirect)
    with open(file, 'a') as log:
        log.writelines(['TIME: {!s}\n'.format(today), 'FILE: {}\n'.format(file)])

    # record parsed arguments
    print_misc('Parsing command line arguments'.format(), file, redirect)
    with open(file, 'a') as log:
        for key, value in vars(args).items():
            if isinstance(value, dict):
                for k, v, in value.items():
                    log.write('ARG: {} -> {} = {}\n'.format(key, k, v))
            else:
                log.write('ARG: {} = {}\n'.format(key, value))

    # record parsed configuration
    print_misc('Parsing configuration file '
               '{!r}'.format(os.path.expanduser("~/.dailyrc")), file, redirect)
    with open(file, 'a') as log:
        for key, value in config.items():
            for k, v, in value.items():
                log.write('CFG: {} -> {} = {}\n'.format(key, k, v))


def run(argv, file, *, redirect=False, timeout=None, shell=False, executable=None):
    if redirect:
        if isinstance(argv, str):
            argv = '{} >/dev/null'.format(argv)
        else:
            argv = "{} >/dev/null".format(' '.join(argv))
        return script(argv, file, timeout=timeout, shell=True, executable=executable)
    return script(argv, file, timeout=timeout, shell=shell, executable=executable)


def script(argv=SHELL, file='typescript', *, timeout=None, shell=False, executable=None):
    if isinstance(argv, str):
        argv = [argv]
    else:
        argv = list(argv)
    if shell:
        argv = [SHELL, '-c'] + argv
    if executable:
        argv[0] = executable

    dim_bytes = dim.encode()
    repl = rb'\1' + dim_bytes

    def master_read(fd):
        data = os.read(fd, 1024)
        text = re.sub(rb'(\033\[[0-9][0-9;]*m)|(\^D\x08\x08)', rb'', data, flags=re.IGNORECASE)
        typescript.write(text)
        return dim_bytes + re.sub(rb'(\033\[[0-9][0-9;]*m)', repl, data, flags=re.IGNORECASE)

    with open(file, 'a') as typescript:
        typescript.write('Script started on {}\n'.format(date()))
        typescript.write('command: {!r}\n'.format(" ".join(argv)))
    with open(file, 'ab') as typescript:
        returncode = ptyng.spawn(argv, master_read, timeout=timeout)
        sys.stdout.write(reset)
    with open(file, 'a') as typescript:
        typescript.write('Script done on {}\n'.format(date()))
    return returncode


def sudo(argv, file, *, askpass=None, sethome=False, redirect=False, timeout=None, executable=None):
    def make_command(argv, askpass, sethome):
        if not isinstance(argv, str):
            argv = ' '.join(argv)
        if getpass.getuser() == 'root':
            return argv
        sudo_askpass = '' if askpass is None else 'SUDO_ASKPASS={!r} '.format(askpass)
        set_home = ' --set-home' if sethome else ''
        return '{}sudo --askpass{} {}'.format(sudo_askpass, set_home, argv)
    return run(make_command(argv, askpass, sethome), file,
               redirect=redirect, timeout=timeout, shell=True, executable=executable)
