# -*- coding: utf-8 -*-
"""refined errors"""

import sys

from macdaily.util.const.macro import DEVMODE


class Error(Exception):
    def __init__(self, *args, **kwargs):
        if not DEVMODE:
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
