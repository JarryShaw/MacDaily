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
__version__ = '2018.12.17'


###########################################################
# Command Mappings
###########################################################


# available commands
COMMANDS = '''\
MacDaily available commands & corresponding subsidiaries:
    archive
    bundle          dump, load
    cleanup         brew, cask, npm, pip
    commands
    config
    dependency      brew, pip
    help
    install         apm, brew, cask, gem, mas, npm, pip, system
    launch
    logging         apm, app, brew, cask, gem, mas, npm, pip, tap
    postinstall
    reinstall       brew, cask
    uninstall       brew, cask, pip
    update          apm, brew, cask, gem, mas, npm, pip, system
'''

# command mappings
MAP_ARCHIVE = {'archive'}
MAP_BUNDLE = {'bundle'}
MAP_CLEANUP = {'cleanup', 'clean'}
MAP_COMMANDS = {'commands'}
MAP_CONFIG = {'config', 'cfg'}
MAP_DEPENDENCY = {'dependency', 'deps', 'dp'}
MAP_HELP = {'help', 'doc', 'man'}
MAP_INSTALL = {'install', 'i'}
MAP_LAUNCH = {'launch', 'init'}
MAP_LOGGING = {'logging', 'log'}
MAP_POSTINSTALL = {'postinstall', 'post', 'ps'}
MAP_REINSTALL = {'reinstall', 're'}
MAP_UNINSTALL = {'uninstall', 'un', 'unlink', 'remove', 'rm', 'r'}
MAP_UPDATE = {'update', 'up', 'upgrade'}
MAP_ALL = (MAP_ARCHIVE | MAP_BUNDLE | MAP_CLEANUP | MAP_COMMANDS | MAP_CONFIG | MAP_DEPENDENCY | MAP_HELP |
           MAP_INSTALL | MAP_LAUNCH | MAP_LOGGING | MAP_POSTINSTALL | MAP_REINSTALL | MAP_UNINSTALL | MAP_UPDATE)

# manpage subsidiaries
MAN_ARCHIVE = set()
MAN_BUNDLE = {'dump', 'load'}
MAN_CLEANUP = {'brew', 'cask', 'npm', 'pip'}
MAN_COMMANDS = set()
MAN_CONFIG = set()
MAN_DEPENDENCY = {'brew', 'pip'}
MAN_HELP = set()
MAN_INSTALL = {'apm', 'brew', 'cask', 'gem', 'mas', 'npm', 'pip', 'system'}
MAN_LAUNCH = set()
MAN_LOGGING = {'apm', 'app', 'brew', 'cask', 'gem', 'mas', 'npm', 'pip', 'tap'}
MAN_POSTINSTALL = set()
MAN_REINSTALL = {'brew', 'cask'}
MAN_UNINSTALL = {'brew', 'cask', 'pip'}
MAN_UPDATE = {'apm', 'brew', 'cask', 'gem', 'mas', 'npm', 'pip', 'system'}


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
