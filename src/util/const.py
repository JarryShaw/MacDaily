# -*- coding: utf-8 -*-
"""utility constants"""

import functools
import getpass
import os
import pwd
import shutil
import sys

try:
    import pathlib2 as pathlib
except ImportError:
    import pathlib

# version string
__version__ = '2018.11.18.dev30'


###########################################################
# Miscellaneous Constants
###########################################################


# script utilities
SCRIPT = shutil.which('script')
UNBUFFER = shutil.which('unbuffer')

# environment macros
ROOT = str(pathlib.Path(__file__).resolve().parents[1])
SHELL = os.getenv('SHELL', shutil.which('sh'))
USER = pwd.getpwnam(getpass.getuser()).pw_gecos


###########################################################
# Magic Strings
###########################################################


@functools.total_ordering
class minstr:

    def __lt__(self, value):
        if isinstance(value, str):
            return True
        return NotImplemented


@functools.total_ordering
class maxstr:

    def __gt__(self, value):
        if isinstance(value, str):
            return True
        return NotImplemented


# string boundaries
MIN = minstr()
MAX = maxstr()


###########################################################
# Terminal Display
###########################################################


# terminal commands
python = sys.executable         # Python version
program = ' '.join(sys.argv)    # arguments

# terminal length
length = shutil.get_terminal_size().columns

# ANSI colours
reset = '\033[0m'           # reset
bold = '\033[1m'            # bold
dim = '\033[2m'             # dim
under = '\033[4m'           # underline
flash = '\033[5m'           # flash

red_dim = '\033[31m'        # dim red foreground
green_dim = '\033[32m'      # dim green foreground
yellow_dim = '\033[33m'     # dim yellow foreground
purple_dim = '\033[34m'     # dim purple foreground
pink_dim = '\033[35m'       # dim pink foreground
blue_dim = '\033[36m'       # dim blue foreground

red_bg_dim = '\033[41m'     # dim red background
green_bg_dim = '\033[42m'   # dim green background
yellow_bg_dim = '\033[43m'  # dim yellow background
purple_bg_dim = '\033[44m'  # dim purple background
pink_bg_dim = '\033[45m'    # dim pink background
blue_bg_dim = '\033[46m'    # dim blue background

grey = '\033[90m'           # bright grey foreground
red = '\033[91m'            # bright red foreground
green = '\033[92m'          # bright green foreground
yellow = '\033[93m'         # bright yellow foreground
purple = '\033[94m'         # bright purple foreground
pink = '\033[95m'           # bright pink foreground
blue = '\033[96m'           # bright blue foreground

grey_bg = '\033[100m'       # bright grey background
red_bg = '\033[101m'        # bright red background
green_bg = '\033[102m'      # bright green background
yellow_bg = '\033[103m'     # bright yellow background
purple_bg = '\033[104m'     # bright purple background
pink_bg = '\033[105m'       # bright pink background
blue_bg = '\033[106m'       # bright blue background
