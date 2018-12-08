# -*- coding: utf-8 -*-

import argparse
import sys

from macdaily.api.archive import archive
# from macdaily.api.bundle import bundle
from macdaily.api.cleanup import cleanup
from macdaily.api.config import config
from macdaily.api.dependency import dependency
from macdaily.api.help import help_
from macdaily.api.install import install
from macdaily.api.launch import launch
from macdaily.api.logging import logging
from macdaily.api.postinstall import postinstall
from macdaily.api.reinstall import reinstall
from macdaily.api.uninstall import uninstall
from macdaily.api.update import update
from macdaily.util.const import (COMMANDS, MAP_ALL, MAP_ARCHIVE, MAP_BUNDLE,
                                 MAP_CLEANUP, MAP_COMMANDS, MAP_CONFIG,
                                 MAP_DEPENDENCY, MAP_HELP, MAP_INSTALL,
                                 MAP_LAUNCH, MAP_LOGGING, MAP_POSTINSTALL,
                                 MAP_REINSTALL, MAP_UNINSTALL, MAP_UPDATE,
                                 __version__, bold, reset)
from macdaily.util.error import CommandNotImplemented
from macdaily.util.misc import beholder


def get_parser():
    parser = argparse.ArgumentParser(prog='MacDaily',
                                     description='macOS Automated Package Manager',
                                     usage='macdaily [options] <command> ...')
    parser.add_argument('-V', '--version', action='version', version=__version__)

    group = parser.add_argument_group('command selection',
                                      'MacDaily provides a friendly CLI workflow for the '
                                      'administrator of macOS to manipulate packages, see '
                                      "`{}macdaily commands{} for more information".format(bold, reset))
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
    elif command in MAP_HELP:
        help_(options)
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
        parser.error("argument CMD: invalid choice: {!r} "
                     "(choose from {})".format(command, ', '.join(sorted(MAP_ALL))))


if __name__ == '__main__':
    sys.exit(main())
