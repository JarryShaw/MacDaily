# -*- coding: utf-8 -*-
"""refined errors"""

import sys


class Error(Exception):
    def __init__(self, *args, **kwargs):
        sys.tracebacklimit = 0
        super().__init__(*args, **kwargs)


class UnsupportedOS(Error, RuntimeError):
    pass


class ConfigNotFoundError(Error, FileNotFoundError):
    pass


class CommandNotImplemented(Error, NotImplementedError):
    pass
