# -*- coding: utf-8 -*-

import functools
import multiprocessing
import os
import platform
import sys

from macdaily.util.const.term import red, reset, yellow
from macdaily.util.error import ChildExit, TimeExpired, UnsupportedOS
from macdaily.util.tools.print import print_term

try:
    import threading
except ImportError:
    import dummy_threading as threading


# error-not-raised flag
FLAG = True
# timeout interval
TIMEOUT = int(os.environ.get('TIMEOUT', '60'))


def beholder(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        global FLAG
        if platform.system() != 'Darwin':
            print_term('macdaily: error: script runs only on macOS', os.devnull)
            raise UnsupportedOS
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            if FLAG:
                FLAG = False
                print('macdaily: {}error{}: operation interrupted'.format(red, reset), file=sys.stderr)
            sys.stdout.write(reset)
            sys.tracebacklimit = 0
            raise
        except Exception:
            if FLAG:
                FLAG = False
                print('macdaily: {}error{}: operation failed'.format(red, reset), file=sys.stderr)
            sys.stdout.write(reset)
            sys.tracebacklimit = 0
            raise
    return wrapper


def retry(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if sys.stdin.isatty():
            return func(*args, **kwargs)
        else:
            QUEUE = multiprocessing.Queue(1)
            kwargs['queue'] = QUEUE
            for _ in range(3):
                proc = multiprocessing.Process(target=func, args=args, kwargs=kwargs)
                timer = threading.Timer(TIMEOUT, function=lambda: proc.kill())
                timer.start()
                proc.start()
                proc.join()
                timer.cancel()
                if proc.exitcode == 0:
                    break
                if proc.exitcode != 9:
                    print_term('macdaily: {}misc{}: function {!r} '
                               'exits with exit status {} on child process'.format(yellow, reset, func.__qualname__, proc.exitcode), os.devnull)
                    raise ChildExit
            else:
                print_term('macdaily: {}misc{}: function {!r} '
                           'retry timeout after {} seconds'.format(red, reset, func.__qualname__, TIMEOUT), os.devnull)
                raise TimeExpired
            return QUEUE.get(block=False)
    return wrapper
