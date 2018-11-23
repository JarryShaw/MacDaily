# -*- coding: utf-8 -*-

import argparse
import sys

from macdaily.api.archive import archive
# from macdaily.api.bundle import bundle
from macdaily.api.cleanup import cleanup
from macdaily.api.config import config
from macdaily.api.dependency import dependency
# from macdaily.api.help import help
from macdaily.api.install import install
from macdaily.api.launch import launch
from macdaily.api.logging import logging
from macdaily.api.postinstall import postinstall
from macdaily.api.reinstall import reinstall
from macdaily.api.uninstall import uninstall
from macdaily.api.update import update
from macdaily.util.const import __version__
from macdaily.util.error import CommandNotImplemented
from macdaily.util.misc import beholder

# command mappings
MAP_COMMANDS = {'commands'}
MAP_HELP = {'help', 'doc'}
MAP_ARCHIVE = {'archive'}
MAP_BUNDLE = {'bundle'}
MAP_CLEANUP = {'cleanup', 'clean'}
MAP_CONFIG = {'config', 'cfg'}
MAP_DEPENDENCY = {'dependency', 'deps', 'dp'}
MAP_INSTALL = {'install', 'i'}
MAP_LAUNCH = {'launch', 'init'}
MAP_LOGGING = {'logging', 'log'}
MAP_POSTINSTALL = {'postinstall', 'post', 'ps'}
MAP_REINSTALL = {'reinstall', 're'}
MAP_UNINSTALL = {'uninstall', 'un', 'unlink', 'remove', 'rm', 'r'}
MAP_UPDATE = {'update', 'up', 'upgrade'}
MAP_ALL = (MAP_COMMANDS | MAP_HELP | MAP_ARCHIVE | MAP_BUNDLE | MAP_CLEANUP | MAP_CONFIG | MAP_DEPENDENCY |
           MAP_INSTALL | MAP_LAUNCH | MAP_LOGGING | MAP_POSTINSTALL | MAP_REINSTALL | MAP_UNINSTALL | MAP_UPDATE)

# available commands
COMMANDS = '''\
MacDaily available commands & corresponding subsidiaries:
    archive
    bundle          dump, load
    cleanup         brew, cask, npm, pip
    config
    dependency      brew, pip
    install         apm, brew ,cask, gem, mas, npm, pip, system
    launch          askpass, confirm, daemons
    logging         apm, app, brew, cask, gem, mas, npm, pip, tap
    postinstall
    reinstall       brew, cask
    uninstall       brew, cask, pip
    update          apm, brew, cask, gem, mas, npm, pip, system
'''


def get_parser():
    parser = argparse.ArgumentParser(prog='MacDaily',
                                     description='macOS Automate Package Manager',
                                     usage='macdaily [options] <command> ...')
    parser.add_argument('-V', '--version', action='version', version=__version__)

    group = parser.add_argument_group('Commands',
                                      'MacDaily provides a friendly CLI workflow for the '
                                      'administrator of macOS to manipulate packages')
    group.add_argument('command', metavar='CMD', help=argparse.SUPPRESS)

    return parser


@beholder
def main():
    # parse args
    parser = get_parser()
    args = parser.parse_args(sys.argv[1:2])

    # fetch command & paras
    command = args.command.lower()
    options = sys.argv[2:]

    if command in MAP_COMMANDS:
        print(COMMANDS, end='')
    elif command in MAP_HELP:
        # help_(options)
        raise CommandNotImplemented
    elif command in MAP_ARCHIVE:
        archive(options)
    elif command in MAP_BUNDLE:
        # bundle(options)
        raise CommandNotImplemented
    elif command in MAP_CLEANUP:
        cleanup(options)
    elif command in MAP_CONFIG:
        config(options)
    elif command in MAP_DEPENDENCY:
        dependency(options)
    elif command in MAP_INSTALL:
        install(options)
    elif command in MAP_LAUNCH:
        launch(options)
    elif command in MAP_LOGGING:
        logging(options)
    elif command in MAP_POSTINSTALL:
        postinstall(options)
    elif command in MAP_REINSTALL:
        reinstall(options)
    elif command in MAP_UNINSTALL:
        uninstall(options)
    elif command in MAP_UPDATE:
        update(options)
    else:
        parser.error(f"argument CMD: invalid choice: {command!r} "
                     f"(choose from {', '.join(sorted(MAP_ALL))})")


if __name__ == '__main__':
    sys.exit(main())
