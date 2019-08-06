# -*- coding: utf-8 -*-

import argparse
import sys

from macdaily.util.const.macro import STR_LAUNCH
from macdaily.util.const.macro import VERSION as __version__
from macdaily.util.const.term import bold, reset


def get_launch_parser():
    #######################################################
    # Launch CLI
    #   * options
    #       - optional arguments
    #       - specification arguments
    #       - general arguments
    #       - miscellaneous arguments
    #   * packages
    #######################################################

    parser = argparse.ArgumentParser(prog='macdaily-launch',
                                     description='MacDaily Dependency Launch Helper',
                                     usage='macdaily launch [options] <prog-selection> ...',
                                     epilog=STR_LAUNCH)
    parser.add_argument('-V', '--version', action='version', version=__version__)

    spec_group = parser.add_argument_group(title='specification arguments')
    spec_group.add_argument('program', nargs='*', metavar='PROG',
                            help=(f"helper program to launch, choose from `{bold}askpass{reset}', "
                                  f"`{bold}confirm{reset}' and `{bold}daemons{reset}'"))

    genl_group = parser.add_argument_group(title='general arguments')
    genl_group.add_argument('-a', '--all', action='store_true',
                            help=(f"launch all help programs, i.e. `{bold}askpass{reset}', "
                                  f"`{bold}confirm{reset}' and `{bold}daemons{reset}'"))
    genl_group.add_argument('-q', '--quiet', action='store_true',
                            help='run in quiet mode, with no output information')
    genl_group.add_argument('-v', '--verbose', action='store_true',
                            help='run in verbose mode, with detailed output information')
    genl_group.add_argument('-n', '--no-cleanup', action='store_true',
                            help='do not run cleanup process')
    genl_group.add_argument('-l', '--show-log', action='store_true',
                            help='open log in Console.app upon completion of command')

    return parser


def parse_args(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    # main parser process
    main_parser = get_launch_parser()
    main_args = main_parser.parse_args(argv or ['--help'])

    return main_args
