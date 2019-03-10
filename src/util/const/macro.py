# -*- coding: utf-8 -*-
"""utility macros"""

import getpass
import os
import pwd
import shutil
import sys

from macdaily.util.compat import pathlib

# version string
VERSION = '2019.3.10'

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

# command aliases
LNK_ARCHIVE = set()
LNK_BUNDLE = set()
LNK_CLEANUP = {'clean'}
LNK_COMMANDS = set()
LNK_CONFIG = {'cfg'}
LNK_DEPENDENCY = {'deps', 'dp'}
LNK_HELP = {'doc', 'man'}
LNK_INSTALL = {'i'}
LNK_LAUNCH = {'init'}
LNK_LOGGING = {'log'}
LNK_POSTINSTALL = {'post', 'ps'}
LNK_REINSTALL = {'re'}
LNK_UNINSTALL = {'un', 'unlink', 'remove', 'rm', 'r'}
LNK_UPDATE = {'up', 'upgrade'}

# aliases strings
STR_ARCHIVE = None
STR_BUNDLE = None
STR_CLEANUP = f"aliases: {', '.join(sorted(LNK_CLEANUP))}"
STR_CONFIG = f"aliases: {', '.join(sorted(LNK_CONFIG))}"
STR_DEPENDENCY = f"aliases: {', '.join(sorted(LNK_DEPENDENCY))}"
STR_HELP = f"aliases: {', '.join(sorted(LNK_HELP))}"
STR_INSTALL = f"aliases: {', '.join(sorted(LNK_INSTALL))}"
STR_LAUNCH = f"aliases: {', '.join(sorted(LNK_LAUNCH))}"
STR_LOGGING = f"aliases: {', '.join(sorted(LNK_LOGGING))}"
STR_POSTINSTALL = f"aliases: {', '.join(sorted(LNK_POSTINSTALL))}"
STR_REINSTALL = f"aliases: {', '.join(sorted(LNK_REINSTALL))}"
STR_UNINSTALL = f"aliases: {', '.join(sorted(LNK_UNINSTALL))}"
STR_UPDATE = f"aliases: {', '.join(sorted(LNK_UPDATE))}"

# command mappings
MAP_ARCHIVE = {'archive'} | LNK_ARCHIVE
MAP_BUNDLE = {'bundle'} | LNK_BUNDLE
MAP_CLEANUP = {'cleanup'} | LNK_CLEANUP
MAP_COMMANDS = {'commands'} | LNK_COMMANDS
MAP_CONFIG = {'config'} | LNK_CONFIG
MAP_DEPENDENCY = {'dependency'} | LNK_DEPENDENCY
MAP_HELP = {'help'} | LNK_HELP
MAP_INSTALL = {'install'} | LNK_INSTALL
MAP_LAUNCH = {'launch'} | LNK_LAUNCH
MAP_LOGGING = {'logging'} | LNK_LOGGING
MAP_MAGIC = {'magic', 'moo', 'whoop-de-doo'}
MAP_POSTINSTALL = {'postinstall'} | LNK_POSTINSTALL
MAP_REINSTALL = {'reinstall'} | LNK_REINSTALL
MAP_UNINSTALL = {'uninstall'} | LNK_UNINSTALL
MAP_UPDATE = {'update'} | LNK_UPDATE
MAP_ALL = (MAP_ARCHIVE | MAP_BUNDLE | MAP_CLEANUP | MAP_COMMANDS | MAP_CONFIG | MAP_DEPENDENCY | MAP_HELP |
           MAP_INSTALL | MAP_LAUNCH | MAP_LOGGING | MAP_POSTINSTALL | MAP_REINSTALL | MAP_UNINSTALL | MAP_UPDATE)

# mode aliases
LNK_APM = {'atom'}
LNK_APP = {'macos', 'application'}
LNK_BREW = {'homebrew'}
LNK_CASK = {'caskroom', 'brew-cask'}
LNK_GEM = {'ruby', 'rubygems'}
LNK_MAS = {'mac', 'appstore', 'app-store', 'mac-app-store'}
LNK_NPM = {'node', 'node.js'}
LNK_PIP = {'python', 'cpython', 'pypy'}
LNK_SYSTEM = {'software', 'softwareupdate'}
LNK_TAP = {'brew-tap'}

# aliases strings
STR_APM = f"aliases: {', '.join(sorted(LNK_APM))}"
STR_APP = f"aliases: {', '.join(sorted(LNK_APP))}"
STR_BREW = f"aliases: {', '.join(sorted(LNK_BREW))}"
STR_CASK = f"aliases: {', '.join(sorted(LNK_CASK))}"
STR_GEM = f"aliases: {', '.join(sorted(LNK_GEM))}"
STR_MAS = f"aliases: {', '.join(sorted(LNK_MAS))}"
STR_NPM = f"aliases: {', '.join(sorted(LNK_NPM))}"
STR_PIP = f"aliases: {', '.join(sorted(LNK_PIP))}"
STR_SYSTEM = f"aliases: {', '.join(sorted(LNK_SYSTEM))}"
STR_TAP = f"aliases: {', '.join(sorted(LNK_TAP))}"

# mode mappings
MAP_APM = {'apm'} | LNK_APM
MAP_APP = {'app'} | LNK_APP
MAP_BREW = {'brew'} | LNK_BREW
MAP_CASK = {'cask'} | LNK_CASK
MAP_GEM = {'gem'} | LNK_GEM
MAP_MAS = {'mas'} | LNK_MAS
MAP_NPM = {'npm'} | LNK_NPM
MAP_PIP = {'pip'} | LNK_PIP
MAP_SYSTEM = {'system'} | LNK_SYSTEM
MAP_TAP = {'tap'} | LNK_TAP

# mode dictionary
MAP_DICT = dict()
for mode, link in (('apm', MAP_APM),
                   ('app', MAP_APP),
                   ('brew', MAP_BREW),
                   ('cask', MAP_CASK),
                   ('gem', MAP_GEM),
                   ('mas', MAP_MAS),
                   ('npm', MAP_NPM),
                   ('pip', MAP_PIP),
                   ('system', MAP_SYSTEM),
                   ('tap', MAP_TAP)):
    for alias in link:
        MAP_DICT[alias] = mode

# command subsidiaries
CMD_ARCHIVE = set()
CMD_BUNDLE = {'dump', 'load'}
CMD_CLEANUP = MAP_BREW | MAP_CASK | MAP_NPM | MAP_PIP
CMD_COMMANDS = set()
CMD_CONFIG = set()
CMD_DEPENDENCY = MAP_BREW | MAP_PIP
CMD_HELP = set()
CMD_INSTALL = MAP_APM | MAP_BREW | MAP_CASK | MAP_GEM | MAP_MAS | MAP_NPM | MAP_PIP | MAP_SYSTEM
CMD_LAUNCH = set()
CMD_LOGGING = MAP_APM | MAP_APP | MAP_BREW | MAP_CASK | MAP_GEM | MAP_MAS | MAP_NPM | MAP_PIP | MAP_TAP
CMD_POSTINSTALL = set()
CMD_REINSTALL = MAP_BREW | MAP_CASK
CMD_UNINSTALL = MAP_BREW | MAP_CASK | MAP_PIP
CMD_UPDATE = MAP_APM | MAP_BREW | MAP_CASK | MAP_GEM | MAP_MAS | MAP_NPM | MAP_PIP | MAP_SYSTEM
