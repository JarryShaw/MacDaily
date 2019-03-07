# -*- coding: utf-8 -*-

import importlib
import platform
import sys

import tbtrim

from macdaily.util.const.macro import DEVMODE
from macdaily.util.const.term import purple, red, reset
from macdaily.util.error import Error, UnsupportedOS
from macdaily.util.tools.misc import predicate

# set up sys.excepthook
if DEVMODE:
    print('macdaily: {}info{}: devmode enabled'.format(purple, reset), file=sys.stderr)
else:
    tbtrim.set_trim_rule(predicate, strict=False,
                         target=(Error, KeyboardInterrupt))

# check platform
if platform.system() != 'Darwin':
    raise UnsupportedOS('macdaily: error: script runs only on macOS')

# check dependencies
if sys.version_info[:2] <= (3, 4):
    def test_import(module):
        try:
            importlib.import_module(module)
        except ImportError:
            print('macdaily: {}error{}: broken dependency'.format(red, reset), file=sys.stderr)
            raise
    test_import('pathlib2')
    test_import('subprocess32')
