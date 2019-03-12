# -*- coding: utf-8 -*-

import functools
import os
import platform
import queue
import signal
import sys

from macdaily.util.compat import multiprocessing, subprocess, threading
from macdaily.util.const.macro import USER, USR
from macdaily.util.const.term import bold, dim, red, reset, under, yellow
from macdaily.util.error import ChildExit, IncorrectPassword, TimeExpired, UnsupportedOS
from macdaily.util.tools.make import make_pipe
from macdaily.util.tools.misc import kill
from macdaily.util.tools.print import print_term

# error-not-raised flag
ERR_FLAG = True
# func-not-called flag
FUNC_FLAG = True


def beholder(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        from macdaily.util.tools.get import get_logfile

        if platform.system() != 'Darwin':
            print_term('macdaily: error: script runs only on macOS', get_logfile())
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
                _funeral(f'macdaily: {red}error{reset}: operation interrupted')
            raise
        except Exception:
            if ERR_FLAG:
                _funeral(f'macdaily: {red}error{reset}: operation failed')
            raise
    return wrapper


def check(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        from macdaily.util.tools.get import get_logfile

        password = func(*args, **kwargs)
        try:
            subprocess.run(['sudo', '--reset-timestamp'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            with make_pipe(password, redirect=True) as pipe:
                subprocess.check_call(['sudo', '--stdin', '--prompt=""', "true"],
                                      stdin=pipe.stdout, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            global ERR_FLAG
            ERR_FLAG = False
            print_term(f'macdaily: {red}error{reset}: incorrect password {dim}{password!r}{reset} for '
                       f'{bold}{USER}{reset} ({under}{USR}{reset})', get_logfile())
            raise IncorrectPassword from None
        return password
    return wrapper


def retry(default=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            from macdaily.util.tools.get import get_logfile

            if sys.stdin.isatty():  # pylint: disable=no-else-return
                return func(*args, **kwargs)
            else:
                # timeout interval
                from macdaily.util.tools.get import get_int
                TIMEOUT = get_int('TIMEOUT', 60)

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
                        print_term(f'macdaily: {yellow}error{reset}: function {func.__qualname__!r} '
                                   f'exits with exit status {proc.exitcode} on child process', get_logfile())
                        raise ChildExit
                else:
                    print_term(f'macdaily: {red}error{reset}: function {func.__qualname__!r} '
                               f'retry timeout after {TIMEOUT} seconds', get_logfile())
                    raise TimeExpired
                try:
                    return QUEUE.get(block=False)
                except queue.Empty:
                    return default
        return wrapper
    return decorator
