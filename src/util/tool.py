# -*- coding: utf-8 -*-

import os
import re

import ptyng
from macdaily.util.colour import bold, reset
from macdaily.util.const import SHELL, program, python
from macdaily.util.misc import write, writelines


def record(file, args, today, config):
    # record program arguments
    script(['echo', f'|ℹ️| {bold}{python} {program}{reset}'], file)
    writelines(file, [f'TIME: {today!s}',
                      f'FILE: {file}'], linesep=True)

    # record parsed arguments
    script(['echo', f'|ℹ️| {bold}Parsing command line arguments{reset}'], file)
    for key, value in vars(args).items():
        if isinstance(value, dict):
            for k, v, in value.items():
                write(file, f'ARG: {key} -> {k} = {v}', linesep=True)
        else:
            write(file, f'ARG: {key} = {value}', linesep=True)

    # record parsed configuration
    script(['echo', f'|ℹ️| {bold}Parsing configuration file '
            f'{os.path.expanduser("~/.dailyrc")!r}{reset}'], file)
    for key, value in config.items():
        for k, v, in value.items():
            write(file, f'CFG: {key} -> {k} = {v}', linesep=True)


def script(argv=SHELL, file='typescript', *, timeout=None, shell=False, executable=None):
    if isinstance(argv, (str, bytes)):
        argv = [argv]
    else:
        argv = list(argv)
    if shell:
        argv = [SHELL, '-c'] + argv
    if executable:
        argv[0] = executable
    with open(file, 'ab') as script:
        def master_read(fd):
            data = os.read(fd, 1024)
            text = re.sub(rb'(\x1b\[[0-9][0-9;]*m)|(\^D\x08\x08)', rb'', data, flags=re.IGNORECASE)
            script.write(text)
            return data
        returncode = ptyng.spawn(argv, master_read, timeout=timeout)
    return returncode
