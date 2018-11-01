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
            print(f'macdaily: {red}error{reset}: operation interrupted', file=sys.stderr)
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
        print(f'{bold}{blue}|💼|{reset} {bold}{text}{reset}', end=end)
    with open(file, 'a') as fd:
        context = re.sub(r'(\033\[[0-9][0-9;]*m)|(\^D\x08\x08)', r'',
                         (text if flag else f'{text}{os.linesep}'), flags=re.IGNORECASE)
        fd.write(f'|💼| {context}')


def print_misc(text, file, redirect=False):
    flag = text.endswith(os.linesep)
    if not redirect:
        end = str() if flag else os.linesep
        print(f'{bold}{grey}|📌|{reset} {bold}{text}{reset}', end=end)
    with open(file, 'a') as fd:
        context = re.sub(r'(\033\[[0-9][0-9;]*m)|(\^D\x08\x08)', r'',
                         (text if flag else f'{text}{os.linesep}'), flags=re.IGNORECASE)
        fd.write(f'|📌| {context}')


def print_scpt(text, file, redirect=False):
    if not isinstance(text, str):
        text = ' '.join(text)
    flag = text.endswith(os.linesep)
    if not redirect:
        end = str() if flag else os.linesep
        print(f'{bold}{purple}|📜|{reset} {bold}{text}{reset}', end=end)
    with open(file, 'a') as fd:
        context = re.sub(r'(\033\[[0-9][0-9;]*m)|(\^D\x08\x08)', r'',
                         (text if flag else f'{text}{os.linesep}'), flags=re.IGNORECASE)
        fd.write(f'|📜| {context}')


def print_term(text, file, redirect=False):
    flag = text.endswith(os.linesep)
    if not redirect:
        end = str() if flag else os.linesep
        print(text, end=end)
    with open(file, 'a') as fd:
        context = re.sub(r'(\033\[[0-9][0-9;]*m)|(\^D\x08\x08)', r'',
                         (text if flag else f'{text}{os.linesep}'), flags=re.IGNORECASE)
        fd.write(context)


def print_text(text, file, redirect=False):
    flag = text.endswith(os.linesep)
    if not redirect:
        end = str() if flag else os.linesep
        print(f'{dim}{text}{reset}', end=end)
    with open(file, 'a') as fd:
        context = re.sub(r'(\033\[[0-9][0-9;]*m)|(\^D\x08\x08)', r'',
                         (text if flag else f'{text}{os.linesep}'), flags=re.IGNORECASE)
        fd.write(context)


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


def run(argv, file, *, redirect=False, timeout=None, shell=False, executable=None):
    if redirect:
        if isinstance(argv, str):
            argv = f'{argv} >/dev/null'
        else:
            argv = f"{' '.join(argv)} >/dev/null"
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

    def master_read(fd):
        data = os.read(fd, 1024)
        text = re.sub(rb'(\033\[[0-9][0-9;]*m)|(\^D\x08\x08)', rb'', data, flags=re.IGNORECASE)
        typescript.write(text)
        return dim.encode()+data

    with open(file, 'a') as typescript:
        typescript.write(f'Script started on {date()}\n')
        typescript.write(f'command: {" ".join(argv)!r}\n')
    with open(file, 'ab') as typescript:
        returncode = ptyng.spawn(argv, master_read, timeout=timeout)
        sys.stdout.write(reset)
    with open(file, 'a') as typescript:
        typescript.write(f'Script done on {date()}\n')
    return returncode


def sudo(argv, file, *, askpass=None, sethome=False, redirect=False, timeout=None, executable=None):
    def make_command(argv, askpass, sethome):
        if not isinstance(argv, str):
            argv = ' '.join(argv)
        if getpass.getuser() == 'root':
            return argv
        sudo_askpass = '' if askpass is None else f'SUDO_ASKPASS={askpass!r} '
        set_home = ' --set-home' if sethome else ''
        return f'{sudo_askpass}sudo --askpass{set_home} {argv}'
    return run(make_command(argv, askpass, sethome), file,
               redirect=redirect, timeout=timeout, shell=True, executable=executable)
