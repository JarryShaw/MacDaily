# -*- coding: utf-8 -*-

import contextlib
import functools
import os
import platform
import sys

from macdaily.util.colour import red, reset
from macdaily.util.error import UnsupportedOS


def make_context(devnull, redirect=False):
    if redirect:
        return contextlib.redirect_stdout(devnull)
    return contextlib.nullcontext()


def write(name, text, linesep=False):
    with open(name, 'a') as file:
        fp = file.write(text)
        if linesep:
            fp = file.write(os.linesep)
    return fp


def writelines(name, lines, linesep=False):
    with open(name, 'a') as file:
        for line in lines:
            fp = file.write(line)
            if linesep:
                fp = file.write(os.linesep)
    return fp


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
