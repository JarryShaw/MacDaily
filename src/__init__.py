# -*- coding: utf-8 -*-

import importlib
import os
import platform
import sys

import tbtrim

from macdaily.util.const.macro import ROOT
from macdaily.util.const.term import red, reset
from macdaily.util.error import Error, UnsupportedOS

# set up sys.excepthook
tbtrim.set_trim_rule(lambda filename: ROOT in os.path.realpath(filename),
                     exception=(Error, KeyboardInterrupt), strict=False)

# check platform
if platform.system() != 'Darwin':
    print('macdaily: error: script runs only on macOS', file=sys.stderr)
    raise UnsupportedOS

# check dependencies
if sys.version_info[:2] <= (3, 4):
    def test_import(module):
        try:
            importlib.import_module(module)
        except ImportError:
            print(f'macdaily: {red}error{reset}: broken dependency', file=sys.stderr)
            raise
    test_import('pathlib2')
    test_import('subprocess32')
