# -*- coding: utf-8 -*-

import importlib
import platform
import sys

from macdaily.util.const import red, reset
from macdaily.util.error import UnsupportedOS

# check platform
if platform.system() != 'Darwin':
    print('macdaily: error: script runs only on macOS', file=sys.stderr)
    raise UnsupportedOS

# check dependencies
if sys.version_info[:2] == (3, 4):
    def test_import(module):
        try:
            importlib.import_module(module)
        except ImportError:
            print('macdaily: {}error{}: broken dependency'.format(red, reset), file=sys.stderr)
            raise
    test_import('pathlib2')
    test_import('subprocess32')
