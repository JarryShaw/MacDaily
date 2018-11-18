# -*- coding: utf-8 -*-

import argparse
import sys

from macdaily.util.const import __version__, bold, reset


def get_postinstall_parser():
    #######################################################
    # Postinstall CLI
    #   * options
    #       - optional arguments
    #       - specification arguments
    #       - general arguments
    #       - miscellaneous arguments
    #   * packages
    #######################################################

    parser = argparse.ArgumentParser(prog='macdaily-postinstall',
                                     description='Homebrew Cask Postinstall Automator',
                                     usage='macdaily postinstall <general-options> <spec-options> <misc-options> ...',
                                     epilog='aliases: post, ps')
    parser.add_argument('-V', '--version', action='version', version=__version__)

    spec_group = parser.add_argument_group(title='specification arguments')
    spec_group.add_argument('-s', '--startswith', action='store', metavar='PREFIX',
                            help='postinstall procedure starts from such formula, sort in initial alphabets')
    spec_group.add_argument('-e', '--endswith', action='store', metavar='SUFFIX',
                            help='postinstall procedure ends after such formula, sort in initial alphabets')
    spec_group.add_argument('-p', '--packages', action='append', nargs='+', default=list(), metavar='FORM',
                            help='name of Homebrew formulae to postinstall')

    genl_group = parser.add_argument_group(title='general arguments')
    genl_group.add_argument('-a', '--all', action='store_true',
                            help='postinstall all Homebrew formulae installed through Homebrew')
    genl_group.add_argument('-q', '--quiet', action='store_true',
                            help='run in quiet mode, with no output information')
    genl_group.add_argument('-v', '--verbose', action='store_true',
                            help='run in verbose mode, with detailed output information')
    genl_group.add_argument('-l', '--show-log', action='store_true',
                            help='open log in Console.app upon completion of command')
    genl_group.add_argument('-y', '--yes', action='store_true',
                            help='yes for all selections')
    genl_group.add_argument('-n', '--no-cleanup', action='store_true',
                            help='do not run cleanup process')

    misc_group = parser.add_argument_group(title='miscellaneous arguments')
    misc_group.add_argument('-L', '--logging', action='store', default=str(), metavar='ARG',
                            help="options for `{}brew list{}' command".format(bold, reset))
    misc_group.add_argument('-U', '--postinstall', action='store', default=str(), metavar='ARG',
                            help="options for `{}brew postinstall <formula>{}' command".format(bold, reset))

    return parser


def parse_args(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    # parser process
    parser = get_postinstall_parser()
    args = parser.parse_args(argv)

    return args
