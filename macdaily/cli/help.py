# -*- coding: utf-8 -*-

import argparse
import sys

from macdaily.util.const.macro import STR_HELP
from macdaily.util.const.macro import VERSION as __version__


def get_help_parser():
    #######################################################
    # Help CLI
    #   * options
    #       - optional arguments
    #       - specification arguments
    #       - general arguments
    #       - miscellaneous arguments
    #   * packages
    #######################################################

    parser = argparse.ArgumentParser(prog='macdaily-help',
                                     description='MacDaily Usage Information Manual',
                                     usage='macdaily help [options] <cmd-selection> ...',
                                     epilog=STR_HELP)
    parser.add_argument('-V', '--version', action='version', version=__version__)

    spec_group = parser.add_argument_group(title='specification arguments')
    spec_group.add_argument('command', action='store', nargs='?', metavar='CMD',
                            help=("display manual information about such command".format()))

    return parser


def parse_args(argv=None):
    if argv is None:
        argv = sys.argv[1:] or ['--help']

    # main parser process
    main_parser = get_help_parser()
    main_args = main_parser.parse_args(argv)

    return main_args
