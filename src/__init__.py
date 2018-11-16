# -*- coding: utf-8 -*-

import platform
import sys


class UnsupportedOS(RuntimeError):
    def __init__(self, message, *args, **kwargs):
        sys.tracebacklimit = 0
        super().__init__(message, *args, **kwargs)


# check platform
if platform.system() != 'Darwin':
    raise UnsupportedOS('macdaily: script runs only on macOS')
