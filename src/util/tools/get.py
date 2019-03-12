# -*- coding: utf-8 -*-

import getpass
import os
import re
import sys
import time
import uuid

from macdaily.util.compat import subprocess
from macdaily.util.const.macro import BOOLEAN_STATES, PASS, USER, VERSION
from macdaily.util.const.term import reset
from macdaily.util.tools.deco import check, retry


def get_boolean(environ, default=False):
    boolean = os.getenv(environ)
    if boolean is None:
        return default
    return BOOLEAN_STATES.get(boolean.strip().lower(), default)


def get_logfile():
    logfile = os.getenv('MACDAILY_LOGFILE')
    if logfile is None:
        dirname = os.path.join(get_logdir(), 'misc', VERSION)
        os.makedirs(dirname, exist_ok=True)
        filename = os.path.join(dirname, f'{time.strftime(r"%Y%m%d-%H%M%S")}-{uuid.uuid4()!s}.log')
        return filename
    return logfile


def get_logdir():
    return os.path.expanduser(os.getenv('MACDAILY_LOGDIR', '~/Library/Logs/MacDaily'))


@retry('N')
def get_input(confirm, prompt='Input: ', *, prefix='', suffix='', queue=None):
    if sys.stdin.isatty():
        try:
            return input(f'{prompt}{suffix}')
        except KeyboardInterrupt:
            print(reset)
            raise
    try:
        subprocess.check_call(['osascript', confirm, f'{prefix}{prompt}'],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        RETURN = 'N'
    else:
        RETURN = 'Y'
    finally:
        if queue is not None:
            queue.put(RETURN)
    return RETURN


def get_int(environ, default=0):
    integer = os.getenv(environ)
    if integer is None:
        return default
    integer = re.sub(r'[,_]', '', integer.strip(), flags=re.IGNORECASE)
    try:
        if re.match(r'0x[0-9a-f]+', integer, re.IGNORECASE):
            return int(integer, base=16)
        if re.match(r'0o[0-7]+', integer, re.IGNORECASE):
            return int(integer, base=8)
        if re.match(r'0[0-7]+', integer, re.IGNORECASE):
            return int(f'0o{"".join(integer[2:])}', base=8)
        if re.match(r'0b[01]+', integer, re.IGNORECASE):
            return int(integer, base=2)
        return int(integer)
    except ValueError:
        return default


@check
@retry(PASS)
def get_pass(askpass, queue=None):
    SUDO_PASSWORD = os.getenv('SUDO_PASSWORD')
    if SUDO_PASSWORD is not None:
        if queue is not None:
            queue.put(SUDO_PASSWORD)
        return SUDO_PASSWORD
    if sys.stdin.isatty():
        try:
            return getpass.getpass(prompt='Password:')
        except KeyboardInterrupt:
            print(reset)
            raise
    RETURN = subprocess.check_output([askpass, f'🔑 Enter your password for {USER}.'],  # pylint: disable=E1101
                                     stderr=subprocess.DEVNULL).strip().decode()
    if queue is not None:
        queue.put(RETURN)
    return RETURN


def get_path(environ, default='.'):
    path = os.getenv(environ)
    if path is None:
        return os.path.realpath(os.path.expanduser(default))
    return os.path.realpath(os.path.expanduser(path.strip()))
