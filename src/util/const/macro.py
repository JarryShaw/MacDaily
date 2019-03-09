# -*- coding: utf-8 -*-
"""utility macros"""

import getpass
import os
import pwd
import shutil
import sys

from macdaily.util.compat import pathlib

# version string
VERSION = '2019.3.9'

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
MAP_MAGIC = {'magic', 'moo', 'whoop-de-doo'}
MAP_POSTINSTALL = {'postinstall', 'post', 'ps'}
MAP_REINSTALL = {'reinstall', 're'}
MAP_UNINSTALL = {'uninstall', 'un', 'unlink', 'remove', 'rm', 'r'}
MAP_UPDATE = {'update', 'up', 'upgrade'}
MAP_ALL = (MAP_ARCHIVE | MAP_BUNDLE | MAP_CLEANUP | MAP_COMMANDS | MAP_CONFIG | MAP_DEPENDENCY | MAP_HELP |
           MAP_INSTALL | MAP_LAUNCH | MAP_LOGGING | MAP_POSTINSTALL | MAP_REINSTALL | MAP_UNINSTALL | MAP_UPDATE)

# command subsidiaries
CMD_ARCHIVE = set()
CMD_BUNDLE = {'dump', 'load'}
CMD_CLEANUP = {'brew', 'cask', 'npm', 'pip'}
CMD_COMMANDS = set()
CMD_CONFIG = set()
CMD_DEPENDENCY = {'brew', 'pip'}
CMD_HELP = set()
CMD_INSTALL = {'apm', 'brew', 'cask', 'gem', 'mas', 'npm', 'pip', 'system'}
CMD_LAUNCH = set()
CMD_LOGGING = {'apm', 'app', 'brew', 'cask', 'gem', 'mas', 'npm', 'pip', 'tap'}
CMD_POSTINSTALL = set()
CMD_REINSTALL = {'brew', 'cask'}
CMD_UNINSTALL = {'brew', 'cask', 'pip'}
CMD_UPDATE = {'apm', 'brew', 'cask', 'gem', 'mas', 'npm', 'pip', 'system'}
