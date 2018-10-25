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
from macdaily.util.const import (SHELL, bold, grey_bg, program, purple_bg,
                                 python, red, reset)
from macdaily.util.error import UnsupportedOS


def make_context(devnull, redirect=False):
    if redirect:
        return contextlib.redirect_stdout(devnull)
    return contextlib.nullcontext()


def write(text, file, linesep=False):
    with open(file, 'a') as context:
        fp = context.write(text)
        if linesep:
            fp = context.write(os.linesep)
    return fp


def writelines(lines, file, linesep=False):
    with open(file, 'a') as context:
        for line in lines:
            fp = context.write(line)
            if linesep:
                fp = context.write(os.linesep)
    return fp


def print_text(text, file, redirect=False):
    with open(os.devnull, 'w') as devnull:
        with make_context(devnull, redirect):
            script(['echo', f'{bold}{text}{reset}'], file)


def print_info(text, file, redirect=False):
    with open(os.devnull, 'w') as devnull:
        with make_context(devnull, redirect):
            script(['echo', f'{bold}{purple_bg}||{reset} {bold}{text}{reset}'], file)


def print_command(text, file, redirect=False):
    with open(os.devnull, 'w') as devnull:
        with make_context(devnull, redirect):
            script(['echo', f'{bold}{grey_bg}||{reset} {bold}{text}{reset}'], file)


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


def sudo(args, askpass, sethome=False):
    if getpass.getuser() == 'root':
        return args
    if sethome:
        return f'SUDO_ASKPASS={askpass} sudo --askpass --set-home {args}'
    return f'SUDO_ASKPASS={askpass} sudo --askpass {args}'


def record(file, args, today, config):
    # record program arguments
    script(['echo', f'|ℹ️| {bold}{python} {program}{reset}'], file)
    writelines([f'TIME: {today!s}', f'FILE: {file}'], file, linesep=True)

    # record parsed arguments
    script(['echo', f'|ℹ️| {bold}Parsing command line arguments{reset}'], file)
    for key, value in vars(args).items():
        if isinstance(value, dict):
            for k, v, in value.items():
                write(f'ARG: {key} -> {k} = {v}', file, linesep=True)
        else:
            write(f'ARG: {key} = {value}', file, linesep=True)

    # record parsed configuration
    script(['echo', f'|ℹ️| {bold}Parsing configuration file '
            f'{os.path.expanduser("~/.dailyrc")!r}{reset}'], file)
    for key, value in config.items():
        for k, v, in value.items():
            write(f'CFG: {key} -> {k} = {v}', file, linesep=True)


def script(argv=SHELL, file='typescript', *, timeout=None, shell=False, executable=None):
    if isinstance(argv, str):
        argv = [argv]
    else:
        argv = list(argv)
    if shell:
        argv = [SHELL, '-c'] + argv
    if executable:
        argv[0] = executable

    def date():
        now = datetime.datetime.now()
        txt = datetime.datetime.strftime(now, '%+')
        return txt

    def master_read(fd):
        data = os.read(fd, 1024)
        text = re.sub(rb'(\x1b\[[0-9][0-9;]*m)|(\^D\x08\x08)', rb'', data, flags=re.IGNORECASE)
        script.write(text)
        return data

    write(f'Script started on {date()}\n', file)
    write(f'command: {" ".join(argv)}\n', file)
    with open(file, 'ab') as script:
        returncode = ptyng.spawn(argv, master_read, timeout=timeout)
    write(f'Script done on  {date()}\n', file)
    return returncode
