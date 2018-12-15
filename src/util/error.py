# -*- coding: utf-8 -*-
"""refined errors"""

import sys


class Error(Exception):
    def __init__(self, *args, **kwargs):
        sys.tracebacklimit = 0
        super().__init__(*args, **kwargs)


class ChildExit(Error, ChildProcessError):
    pass


class CommandNotImplemented(Error, NotImplementedError):
    pass


class ConfigNotFoundError(Error, FileNotFoundError):
    pass


class TimeExpired(Error, TimeoutError):
    pass


class UnsupportedOS(Error, RuntimeError):
    pass
