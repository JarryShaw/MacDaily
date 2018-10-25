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

from macdaily.util.const import (SHELL, blue, bold, grey, program, purple,
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
            print(f'macdaily: {red}error{reset}: operation interrupted', file=sys.stderr)
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
    with open(os.devnull, 'w') as devnull:
        with make_context(devnull, redirect):
            script(['echo', f'{bold}{blue}|💼|{reset} {bold}{text}{reset}'], file)


def print_misc(text, file, redirect=False):
    with open(os.devnull, 'w') as devnull:
        with make_context(devnull, redirect):
            script(['echo', f'{bold}{grey}|📌|{reset} {bold}{text}{reset}'], file)


def print_scpt(text, file, redirect=False):
    with open(os.devnull, 'w') as devnull:
        with make_context(devnull, redirect):
            script(['echo', f'{bold}{purple}|📜|{reset} {bold}{text}{reset}'], file)


def print_text(text, file, redirect=False):
    with open(os.devnull, 'w') as devnull:
        with make_context(devnull, redirect):
            script(['echo', text], file)


def record(file, args, today, config, redirect=False):
    # record program arguments
    print_misc(f'{python} {program}', file, redirect)
    with open(file, 'a') as log:
        log.writelines([f'TIME: {today!s}\n', f'FILE: {file}\n'])

    # record parsed arguments
    print_misc(f'Parsing command line arguments', file, redirect)
    with open(file, 'a') as log:
        for key, value in vars(args).items():
            if isinstance(value, dict):
                for k, v, in value.items():
                    log.write(f'ARG: {key} -> {k} = {v}\n')
            else:
                log.write(f'ARG: {key} = {value}\n')

    # record parsed configuration
    print_misc(f'Parsing configuration file '
               f'{os.path.expanduser("~/.dailyrc")!r}', file, redirect)
    with open(file, 'a') as log:
        for key, value in config.items():
            for k, v, in value.items():
                log.write(f'CFG: {key} -> {k} = {v}\n')


def script(argv=SHELL, file='typescript', *, timeout=None, shell=False, executable=None):
    if isinstance(argv, str):
        argv = [argv]
    else:
        argv = list(argv)
    if shell:
        argv = [SHELL, '-c'] + argv
    if executable:
        argv[0] = executable

    def master_read(fd):
        data = os.read(fd, 1024)
        text = re.sub(rb'(\033\[[0-9][0-9;]*m)|(\^D\x08\x08)', rb'', data, flags=re.IGNORECASE)
        typescript.write(text)
        return data

    with open(file, 'a') as typescript:
        typescript.write(f'Script started on {date()}\n')
        typescript.write(f'command: {" ".join(argv)!r}\n')
    with open(file, 'ab') as typescript:
        returncode = ptyng.spawn(argv, master_read, timeout=timeout)
    with open(file, 'a') as typescript:
        typescript.write(f'Script done on {date()}\n')
    return returncode


def sudo(args, file='typescript', *, askpass=None, sethome=False, redirect=False, timeout=None, executable=None):
    def make_command():
        if not isinstance(args, str):
            args = ' '.join(args)
        if getpass.getuser() == 'root':
            return args
        sudo_askpass = '' if askpass is None else f'SUDO_ASKPASS={askpass!r}'
        set_home = '--set-home' if sethome else ''
        return f'{sudo_askpass} sudo --askpass {set_home} {args}'

    with open(os.devnull, 'w') as devnull:
        with make_context(devnull, redirect):
            return script(make_command(), file, timeout=timeout, shell=True, executable=executable)


def write(text, file, linesep=False):
    with open(file, 'a') as log:
        fp = log.write(text)
        if linesep:
            fp = log.write(os.linesep)
    return fp


def writelines(lines, file, linesep=False):
    with open(file, 'a') as log:
        if linesep:
            return log.writelines(f'{line}{os.linesep}' for line in lines)
        return log.writelines(lines)
