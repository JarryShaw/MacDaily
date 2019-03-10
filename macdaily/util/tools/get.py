# -*- coding: utf-8 -*-

import getpass
import os
import re
import sys

from macdaily.util.compat import subprocess
from macdaily.util.const.macro import BOOLEAN_STATES, PASS, USER
from macdaily.util.const.term import reset
from macdaily.util.tools.deco import retry


def get_boolean(environ, default=False):
    boolean = os.environ.get(environ)
    if boolean is None:
        return default
    return BOOLEAN_STATES.get(boolean.strip().lower(), default)


@retry('N')
def get_input(confirm, prompt='Input: ', *, prefix='', suffix='', queue=None):
    if sys.stdin.isatty():
        try:
            return input('{}{}'.format(prompt, suffix))
        except KeyboardInterrupt:
            print(reset)
            raise
    try:
        subprocess.check_call(['osascript', confirm, '{}{}'.format(prefix, prompt)],
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
    integer = os.environ.get(environ)
    if integer is None:
        return default
    integer = re.sub(r'[,_]', '', integer.strip(), flags=re.IGNORECASE)
    try:
        if re.match(r'0x[0-9a-f]+', integer, re.IGNORECASE):
            return int(integer, base=16)
        if re.match(r'0o[0-7]+', integer, re.IGNORECASE):
            return int(integer, base=8)
        if re.match(r'0[0-7]+', integer, re.IGNORECASE):
            return int('0o{}'.format("".join(integer[2:])), base=8)
        if re.match(r'0b[01]+', integer, re.IGNORECASE):
            return int(integer, base=2)
        return int(integer)
    except ValueError:
        return default


@retry(PASS)
def get_pass(askpass, queue=None):
    SUDO_PASSWORD = os.environ.get('SUDO_PASSWORD')
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
    RETURN = subprocess.check_output([askpass, '🔑 Enter your password for {}.'.format(USER)],  # pylint: disable=E1101
                                     stderr=subprocess.DEVNULL).strip().decode()
    if queue is not None:
        queue.put(RETURN)
    return RETURN


def get_path(environ, default='.'):
    path = os.environ.get(environ)
    if path is None:
        return os.path.realpath(os.path.expanduser(default))
    return os.path.realpath(os.path.expanduser(path.strip()))
