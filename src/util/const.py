# -*- coding: utf-8 -*-
"""utility constants"""

import os
import shutil
import sys

# version string
__version__ = '2018.10.18.dev1'

# terminal commands
python = sys.executable         # Python version
program = ' '.join(sys.argv)    # arguments

# environment macros
ROOT = os.path.dirname(os.path.abspath(__file__))
SHELL = os.environ.get('SHELL', shutil.which('sh'))
