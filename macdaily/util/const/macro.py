# -*- coding: utf-8 -*-
"""utility macros"""

import getpass
import os
import pwd
import shutil
import sys

from macdaily.util.compat import pathlib

# version string
VERSION = '2019.3.8'

# terminal commands
PYTHON = sys.executable         # Python version
PROGRAM = ' '.join(sys.argv)    # arguments

###########################################################
# Environment Variables
###########################################################

# boolean mappings
BOOLEAN_STATES = {'1': True, '0': False,
                  'yes': True, 'no': False,
                  'true': True, 'false': False,
                  'on': True, 'off': False}

# DEVMODE flag
DEVMODE = BOOLEAN_STATES.get(os.environ.get('MACDAILY_DEVMODE', '').lower(), False)

###########################################################
# Miscellaneous Constants
###########################################################

# script utilities
SCRIPT = shutil.which('script')
UNBUFFER = shutil.which('unbuffer')

# environment macros
ROOT = str(pathlib.Path(__file__).resolve().parents[2])
SHELL = os.getenv('SHELL', shutil.which('sh'))

# user information
USR = getpass.getuser()
PWD = pwd.getpwnam(USR)
USER = PWD.pw_gecos
PASS = PWD.pw_passwd

# emoji mappings
ORIG_BEER = '🍺'
RESP_BEER = 'ð\x9f\x8dº'

# homebrew aliases
NODE = {'node', 'node.js', 'node@11', 'nodejs', 'npm'}
PYTHON2 = {'python@2', 'python2'}
PYTHON3 = {'python', 'python3', 'python@3'}

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
MAP_MAGIC = {'magic', 'whoop-de-doo'}
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
