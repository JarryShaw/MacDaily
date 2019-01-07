# -*- coding: utf-8 -*-

import getpass
import sys

from macdaily.util.const.macro import USER
from macdaily.util.const.term import reset
from macdaily.util.tools.deco import retry

if sys.version_info[:2] <= (3, 4):
    import subprocess32 as subprocess
else:
    import subprocess


@retry
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


@retry
def get_pass(askpass, queue=None):
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
