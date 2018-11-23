# -*- coding: utf-8 -*-

import argparse
import sys

from macdaily.util.const import __version__


def get_cleanup_parser():
    #######################################################
    # Cleanup CLI
    #   * options
    #       - optional arguments
    #       - general arguments
    #       - package arguments
    #       - control arguments
    #   * specifications
    #######################################################

    parser = argparse.ArgumentParser(prog='macdaily-cleanup',
                                     description='macOS Package Cache Cleanup',
                                     usage='macdaily cleanup [options] <mode-selection> ...',
                                     epilog='aliases: clean')
    parser.add_argument('-V', '--version', action='version', version=__version__)
    parser.add_argument('more_opts', nargs=argparse.REMAINDER, help=argparse.SUPPRESS)

    genl_group = parser.add_argument_group(title='general arguments')
    genl_group.add_argument('-a', '--all', action='store_true',
                            help=('cleanup caches of all packages installed through Node.js, '
                                  'Homebrew, Caskroom and Python'))
    genl_group.add_argument('-q', '--quiet', action='store_true',
                            help='run in quiet mode, with no output information')
    genl_group.add_argument('-v', '--verbose', action='store_true',
                            help='run in verbose mode, with detailed output information')
    genl_group.add_argument('-l', '--show-log', action='store_true',
                            help='open log in Console.app upon completion of command')

    ctrl_group = parser.add_argument_group(title='control arguments',
                                           description='options used to disable update of certain mode')
    ctrl_group.add_argument('--no-npm', action='store_true', help='do not update Node.js modules')
    ctrl_group.add_argument('--no-pip', action='store_true', help='do not update Python packages')
    ctrl_group.add_argument('--no-brew', action='store_true', help='do not update Homebrew formulae')
    ctrl_group.add_argument('--no-cask', action='store_true', help='do not update Caskroom binaries')

    parser.add_argument_group(title='mode selection',
                              description=('cleanup caches of packages installed through a specified method, '
                                           'e.g.: npm, pip, brew, cask'))

    return parser


def get_npm_parser():
    #######################################################
    # Npm Cleanup CLI
    #   * options
    #       - optional arguments
    #       - general arguments
    #       - miscellaneous arguments
    #   * packages
    #######################################################

    npm_parser = argparse.ArgumentParser(prog='macdaily-cleanup-npm',
                                         description='Node.js Module Cache Cleanup',
                                         usage='macdaily cleanup npm [options] ...')
    npm_parser.add_argument('-V', '--version', action='version', version=__version__)
    npm_parser.add_argument('more_opts', nargs=argparse.REMAINDER, help=argparse.SUPPRESS)

    npm_genl_group = npm_parser.add_argument_group(title='general arguments')
    npm_genl_group.add_argument('-q', '--quiet', action='store_true',
                                help='run in quiet mode, with no output information')
    npm_genl_group.add_argument('-v', '--verbose', action='store_true',
                                help='run in verbose mode, with detailed output information')

    return npm_parser


def get_pip_parser():
    #######################################################
    # Pip Cleanup CLI
    #   * options
    #       - optional arguments
    #       - general arguments
    #       - miscellaneous arguments
    #   * packages
    #######################################################

    pip_parser = argparse.ArgumentParser(prog='macdaily-cleanup-pip',
                                         description='Python Package Cache Cleanup',
                                         usage='macdaily cleanup pip [options] ...')
    pip_parser.add_argument('-V', '--version', action='version', version=__version__)
    pip_parser.add_argument('more_opts', nargs=argparse.REMAINDER, help=argparse.SUPPRESS)

    pip_spec_group = pip_parser.add_argument_group(title='specification arguments')
    pip_spec_group.add_argument('-b', '--brew', action='store_true',
                                help='cleanup caches of Python installed from Homebrew')
    pip_spec_group.add_argument('-c', '--cpython', action='store_true',
                                help='cleanup caches of CPython implementation')
    pip_spec_group.add_argument('-e', '--python', action='append', nargs='+',
                                default=list(), metavar='VER', dest='version',
                                help='indicate packages from which version of Python will cleanup')
    pip_spec_group.add_argument('-r', '--pypy', action='store_true',
                                help='cleanup caches of PyPy implementation')
    pip_spec_group.add_argument('-s', '--system', action='store_true',
                                help='cleanup caches of Python provided by macOS system')

    pip_genl_group = pip_parser.add_argument_group(title='general arguments')
    pip_genl_group.add_argument('-q', '--quiet', action='store_true',
                                help='run in quiet mode, with no output information')
    pip_genl_group.add_argument('-v', '--verbose', action='store_true',
                                help='run in verbose mode, with detailed output information')

    return pip_parser


def get_brew_parser():
    #######################################################
    # Brew Cleanup CLI
    #   * options
    #       - optional arguments
    #       - general arguments
    #       - miscellaneous arguments
    #   * packages
    #######################################################

    brew_parser = argparse.ArgumentParser(prog='macdaily-cleanup-brew',
                                          description='Homebrew Formula Cache Cleanup',
                                          usage='macdaily cleanup brew [options] ...')
    brew_parser.add_argument('-V', '--version', action='version', version=__version__)
    brew_parser.add_argument('more_opts', nargs=argparse.REMAINDER, help=argparse.SUPPRESS)

    brew_genl_group = brew_parser.add_argument_group(title='general arguments')
    brew_genl_group.add_argument('-q', '--quiet', action='store_true',
                                 help='run in quiet mode, with no output information')
    brew_genl_group.add_argument('-v', '--verbose', action='store_true',
                                 help='run in verbose mode, with detailed output information')

    return brew_parser


def get_cask_parser():
    #######################################################
    # Cask Cleanup CLI
    #   * options
    #       - optional arguments
    #       - general arguments
    #       - miscellaneous arguments
    #   * packages
    #######################################################

    cask_parser = argparse.ArgumentParser(prog='macdaily-cleanup-cask',
                                          description='Homebrew Cask Cache Cleanup',
                                          usage='macdaily cleanup cask [options] ...')
    cask_parser.add_argument('-V', '--version', action='version', version=__version__)
    cask_parser.add_argument('more_opts', nargs=argparse.REMAINDER, help=argparse.SUPPRESS)

    cask_genl_group = cask_parser.add_argument_group(title='general arguments')
    cask_genl_group.add_argument('-q', '--quiet', action='store_true',
                                 help='run in quiet mode, with no output information')
    cask_genl_group.add_argument('-v', '--verbose', action='store_true',
                                 help='run in verbose mode, with detailed output information')

    return cask_parser


def parse_args(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    # main parser process
    main_parser = get_cleanup_parser()
    main_args = main_parser.parse_args(argv)

    def _update(d, e):
        for k, v in e.items():
            if k in d:
                if isinstance(v, list):
                    d[k].extend(v)
                else:
                    d[k] = v
            else:
                d[k] = v
        return d

    # recursively parse mode options
    more_opts = main_args.more_opts
    while more_opts:
        # traverse all extra options
        for index, option in enumerate(more_opts, start=1):
            # ignore ``--`` (end of option list)
            if option == '--':
                continue

            # check if legal mode
            get_parser = globals().get(f'get_{option}_parser')
            if get_parser is None:
                main_parser.error(f'unrecognized arguments: {option}')

            # parse mode arguments
            parser = get_parser()
            args = parser.parse_args(more_opts[index:])

            # store/update parsed arguments
            opt_dict = getattr(main_args, option, dict())
            opt_dict.pop('more_opts', None)
            setattr(main_args, option, _update(opt_dict, vars(args)))

            # check for extra options
            more_opts = args.more_opts
            break

    delattr(main_args, 'more_opts')
    return main_args
