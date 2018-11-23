# -*- coding: utf-8 -*-

import argparse
import sys

from macdaily.util.const import __version__, bold, reset


def get_config_parser():
    #######################################################
    # Config CLI
    #   * options
    #       - optional arguments
    #       - specification arguments
    #       - general arguments
    #       - miscellaneous arguments
    #   * packages
    #######################################################

    parser = argparse.ArgumentParser(prog='macdaily-config',
                                     description='MacDaily Runtime Configuration Helper',
                                     usage='macdaily config [options] <key> <value> ...',
                                     epilog='aliases: init')
    parser.add_argument('-V', '--version', action='version', version=__version__)

    spec_group = parser.add_argument_group(title='specification arguments')
    spec_group.add_argument('-a', '--add', action='store_true',
                            help=('adds a new line to the option without altering any '
                                  'existing values [requires ConfigUpdater]'))
    spec_group.add_argument('-g', '--get', action='store_true',
                            help='get the value for a given key')
    spec_group.add_argument('-u', '--unset', action='store_true',
                            help=('remove the line matching the key from config file '
                                  '[requires ConfigUpdater]'))
    spec_group.add_argument('-i', '--interactive', action='store_true',
                            help='enter interactive configuration mode')
    spec_group.add_argument('-l', '--list', action='store_true',
                            help='list all variables set in config file, along with their values')

    genl_group = parser.add_argument_group(title='general arguments')
    genl_group.add_argument('key', action='store', nargs='?', help='a given key')
    genl_group.add_argument('value', action='store', nargs='?', help='the value for a given key')
    genl_group.add_argument('-q', '--quiet', action='store_true',
                            help='run in quiet mode, with no output information')
    genl_group.add_argument('-v', '--verbose', action='store_true',
                            help='run in verbose mode, with detailed output information')

    ctrl_group = parser.add_argument_group(title='control arguments',
                                           description='options used to set true or false')
    ctrl_group.add_argument('-T', '--true', action='store_true',
                            help="set the value for a given key to `{}true{}'".format(bold, reset))
    ctrl_group.add_argument('-F', '--false', action='store_true',
                            help="set the value for a given key to `{}false{}'".format(bold, reset))

    return parser


def parse_args(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    # main parser process
    main_parser = get_config_parser()
    main_args = main_parser.parse_args(argv)

    return main_args
