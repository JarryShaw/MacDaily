# -*- coding: utf-8 -*-

import argparse
import sys

from macdaily.util.const import __version__


def get_archive_parser():
    #######################################################
    # Archive CLI
    #   * options
    #       - optional arguments
    #       - specification arguments
    #       - general arguments
    #       - miscellaneous arguments
    #   * packages
    #######################################################

    parser = argparse.ArgumentParser(prog='macdaily-archive',
                                     description='MacDaily Log Archive Utility',
                                     usage='macdaily archive [options] <path-selection> ...')
    parser.add_argument('-V', '--version', action='version', version=__version__)

    spec_group = parser.add_argument_group(title='specification arguments')
    spec_group.add_argument('path', nargs='*', metavar='CMD',
                            help=('archive logs of specified command, e.g. archive, cleanup, '
                                  'dependency, logging, postinstall, reinstall, uninstall, update, '
                                  'logging/apm, logging/app, logging/brew, logging/cask, logging/gem, '
                                  'logging/mas, logging/npm, logging/pip and logging/tap'))

    genl_group = parser.add_argument_group(title='general arguments')
    genl_group.add_argument('-a', '--all', action='store_true',
                            help='archive all ancient logs')
    genl_group.add_argument('-n', '--no-storage', action='store_true',
                            help='do not move ancient logs into external hard disk')
    genl_group.add_argument('-q', '--quiet', action='store_true',
                            help='run in quiet mode, with no output information')
    genl_group.add_argument('-v', '--verbose', action='store_true',
                            help='run in verbose mode, with detailed output information')
    genl_group.add_argument('-l', '--show-log', action='store_true',
                            help='open log in Console.app upon completion of command')

    return parser


def parse_args(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    # main parser process
    main_parser = get_archive_parser()
    main_args = main_parser.parse_args(argv)

    return main_args
