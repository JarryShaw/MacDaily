# -*- coding: utf-8 -*-

import functools
import os
import platform
import queue
import signal
import sys

from macdaily.util.compat import multiprocessing, threading
from macdaily.util.const.term import red, reset, yellow
from macdaily.util.error import ChildExit, TimeExpired, UnsupportedOS
from macdaily.util.tools.misc import kill
from macdaily.util.tools.print import print_term

# error-not-raised flag
ERR_FLAG = True
# func-not-called flag
FUNC_FLAG = True
# timeout interval
TIMEOUT = int(os.environ.get('TIMEOUT', '60'))


def beholder(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if platform.system() != 'Darwin':
            print_term('macdaily: error: script runs only on macOS', os.devnull)
            raise UnsupportedOS

        def _finale(epilogue):
            global FUNC_FLAG
            if FUNC_FLAG:
                FUNC_FLAG = False
                sys.stdout.write(reset)
                sys.stderr.write(reset)
                kill(os.getpid(), signal.SIGSTOP)
            return epilogue

        def _funeral(last_words):
            global ERR_FLAG
            ERR_FLAG = False
            # sys.tracebacklimit = 0
            sys.stdout.write(reset)
            sys.stderr.write(reset)
            kill(os.getpid(), signal.SIGKILL)
            print(last_words, file=sys.stderr)

        try:
            return _finale(func(*args, **kwargs))
        except KeyboardInterrupt:
            if ERR_FLAG:
                _funeral('macdaily: {}error{}: operation interrupted'.format(red, reset))
            raise
        except Exception:
            if ERR_FLAG:
                _funeral('macdaily: {}error{}: operation failed'.format(red, reset))
            raise
    return wrapper


def retry(default=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if sys.stdin.isatty():  # pylint: disable=no-else-return
                return func(*args, **kwargs)
            else:
                QUEUE = multiprocessing.Queue(1)
                kwargs['queue'] = QUEUE
                for _ in range(3):
                    proc = multiprocessing.Process(target=func, args=args, kwargs=kwargs)
                    timer = threading.Timer(TIMEOUT, function=proc.kill)
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
                try:
                    return QUEUE.get(block=False)
                except queue.Empty:
                    return default
        return wrapper
    return decorator
