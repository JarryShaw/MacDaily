# -*- coding: utf-8 -*-
"""function decorators"""

import functools
import os
import platform
import shlex
import sys
import traceback

from macdaily.util.colour import red, reset
from macdaily.util.const import ROOT
from macdaily.util.error import PasswordError, UnsupportedOS
from macdaily.util.helper import make_pipe

try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess


def beholder(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if platform.system() != 'Darwin':
            raise UnsupportedOS('macdaily: script runs only on macOS')
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            print(
                f'\nmacdaily: {red}error{reset}: operation interrupted\n', file=sys.stderr)
            raise
    return wrapper


def check(parse):
    @functools.wraps(parse)
    def wrapper():
        config = parse()
        subprocess.run(['sudo', '--reset-timestamp'],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            with make_pipe(config) as PIPE:
                subprocess.check_call(['sudo', '--stdin', '--validate'],
                                      stdin=PIPE.stdout, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            raise PasswordError(
                1, f"Invalid password for {config['Account']['username']!r}") from None
        return config
    return wrapper


def aftermath(logfile, tmpfile=None, command=None, logmode='null'):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except subprocess.TimeoutExpired:
                with open(logfile, 'a') as file:
                    file.write(
                        f'\nERR: {traceback.format_exc().splitlines()[-1]}\n')
                if command is not None:
                    print(
                        f'\nmacdaily: {red}{command}{reset}: operation timeout\n', file=sys.stderr)
                raise
            except BaseException:
                path = os.path.join(ROOT, f'lib{command}/aftermath.sh')
                if os.path.isfile(path):
                    subprocess.run(['bash', path, shlex.quote(logfile), shlex.quote(tmpfile), 'true', logmode],
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                raise
        return wrapper
    return decorator
