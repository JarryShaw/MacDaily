# -*- coding: utf-8 -*-

import argparse
import sys

from macdaily.util.const import __version__, bold, reset


def get_dependency_parser():
    #######################################################
    # Dependency CLI
    #   * options
    #       - optional arguments
    #       - general arguments
    #       - package arguments
    #       - control arguments
    #   * specifications
    #######################################################

    parser = argparse.ArgumentParser(prog='macdaily-dependency',
                                     description='macOS Package Dependency Query',
                                     usage='macdaily dependency [options] <mode-selection> ...',
                                     epilog='aliases: deps, dp')
    parser.add_argument('-V', '--version', action='version', version=__version__)
    parser.add_argument('more_opts', nargs=argparse.REMAINDER, help=argparse.SUPPRESS)

    genl_group = parser.add_argument_group(title='general arguments')
    genl_group.add_argument('-a', '--all', action='store_true',
                            help=('query all packages installed through Python and Homebrew'))
    genl_group.add_argument('-q', '--quiet', action='store_true',
                            help='run in quiet mode, with no output information')
    genl_group.add_argument('-v', '--verbose', action='store_true',
                            help='run in verbose mode, with detailed output information')
    genl_group.add_argument('-n', '--no-cleanup', action='store_true',
                            help='do not run cleanup process')
    genl_group.add_argument('-l', '--show-log', action='store_true',
                            help='open log in Console.app upon completion of command')
    genl_group.add_argument('-f', '--tree', action='store_true',
                            help='show dependencies as a tree [requires DictDumper]')
    genl_group.add_argument('-g', '--topological', action='store_true',
                            help='show dependencies in topological order')
    genl_group.add_argument('-d', '--depth', action='store', type=int, metavar='LEVEL',
                            help='max display depth of the dependency tree')

    pkgs_group = parser.add_argument_group(title='package arguments',
                                           description='options used to specify packages of each mode')
    pkgs_group.add_argument('--pip', action='append', nargs='+', default=list(), metavar='PKG', dest='pip_pkgs',
                            help='name of Python packages to query')
    pkgs_group.add_argument('--brew', action='append', nargs='+', default=list(), metavar='FORM', dest='brew_pkgs',
                            help='name of Homebrew formulae to query')

    ctrl_group = parser.add_argument_group(title='control arguments',
                                           description='options used to disable update of certain mode')
    ctrl_group.add_argument('--no-pip', action='store_true', help='do not query Python packages')
    ctrl_group.add_argument('--no-brew', action='store_true', help='do not query Homebrew formulae')

    parser.add_argument_group(title='mode selection',
                              description=('query dependency of packages installed through a specified method, '
                                           'e.g.: pip, brew'))

    return parser


def get_pip_parser():
    #######################################################
    # Pip Dependency CLI
    #   * options
    #       - optional arguments
    #       - specification arguments
    #       - general arguments
    #       - miscellaneous arguments
    #   * packages
    #######################################################

    pip_parser = argparse.ArgumentParser(prog='macdaily-dependency-pip',
                                         description='Python Package Dependency Query',
                                         usage='macdaily dependency pip [options] <packages> ...')
    pip_parser.add_argument('-V', '--version', action='version', version=__version__)
    pip_parser.add_argument('more_opts', nargs=argparse.REMAINDER, help=argparse.SUPPRESS)

    pip_spec_group = pip_parser.add_argument_group(title='specification arguments')
    pip_spec_group.add_argument('-b', '--brew', action='store_true',
                                help='query packages of Python installed from Homebrew')
    pip_spec_group.add_argument('-c', '--cpython', action='store_true',
                                help='query packages of CPython implementation')
    pip_spec_group.add_argument('-e', '--python', action='append', nargs='+',
                                default=list(), metavar='VER', dest='version',
                                help='indicate packages from which version of Python will query')
    pip_spec_group.add_argument('-r', '--pypy', action='store_true',
                                help='query packages of PyPy implementation')
    pip_spec_group.add_argument('-s', '--system', action='store_true',
                                help='query packages of Python provided by macOS system')
    pip_spec_group.add_argument('-p', '--packages', action='append', nargs='+', default=list(), metavar='PKG',
                                help='name of Python packages to query')

    pip_genl_group = pip_parser.add_argument_group(title='general arguments')
    pip_genl_group.add_argument('-a', '--all', action='store_true',
                                help='query all Python packages installed through Python Package Index')
    pip_genl_group.add_argument('-q', '--quiet', action='store_true',
                                help='run in quiet mode, with no output information')
    pip_genl_group.add_argument('-v', '--verbose', action='store_true',
                                help='run in verbose mode, with detailed output information')
    pip_genl_group.add_argument('-n', '--no-cleanup', action='store_true',
                                help='do not run cleanup process')
    pip_genl_group.add_argument('-f', '--tree', action='store_true',
                                help='show dependencies as a tree [requires DictDumper]')
    pip_genl_group.add_argument('-g', '--topological', action='store_true',
                                help='show dependencies in topological order')
    pip_genl_group.add_argument('-d', '--depth', action='store', type=int, metavar='LEVEL',
                                help='max display depth of the dependency tree')

    return pip_parser


def get_brew_parser():
    #######################################################
    # Brew Dependency CLI
    #   * options
    #       - optional arguments
    #       - specification arguments
    #       - general arguments
    #       - miscellaneous arguments
    #   * packages
    #######################################################

    brew_parser = argparse.ArgumentParser(prog='macdaily-dependency-brew',
                                          description='Homebrew Formula Dependency Query',
                                          usage='macdaily dependency brew [options] <formulae> ...')
    brew_parser.add_argument('-V', '--version', action='version', version=__version__)
    brew_parser.add_argument('more_opts', nargs=argparse.REMAINDER, help=argparse.SUPPRESS)

    brew_spec_group = brew_parser.add_argument_group(title='specification arguments')
    brew_spec_group.add_argument('-b', '--include-build', action='store_true',
                                 help='include the {}:build{} type dependencies'.format(bold, reset))
    brew_spec_group.add_argument('-o', '--include-optional', action='store_true',
                                 help='include {}:optional{} dependencies'.format(bold, reset))
    brew_spec_group.add_argument('-t', '--include-test', action='store_true',
                                 help='include (non-recursive) {}:test{} dependencies'.format(bold, reset))
    brew_spec_group.add_argument('-s', '--skip-recommended', action='store_true',
                                 help='skip {}:recommended{} type dependencies'.format(bold, reset))
    brew_spec_group.add_argument('-r', '--include-requirements', action='store_true',
                                 help='include requirements in addition to dependencies')
    brew_spec_group.add_argument('-p', '--packages', action='append', nargs='+', default=list(), metavar='FORM',
                                 help='name of Homebrew formulae to query')

    brew_genl_group = brew_parser.add_argument_group(title='general arguments')
    brew_genl_group.add_argument('-a', '--all', action='store_true',
                                 help='query all Homebrew formulae installed through Homebrew')
    brew_genl_group.add_argument('-q', '--quiet', action='store_true',
                                 help='run in quiet mode, with no output information')
    brew_genl_group.add_argument('-v', '--verbose', action='store_true',
                                 help='run in verbose mode, with detailed output information')
    brew_genl_group.add_argument('-n', '--no-cleanup', action='store_true',
                                 help='do not run cleanup process')
    brew_genl_group.add_argument('-f', '--tree', action='store_true',
                                 help='show dependencies as a tree [requires DictDumper]')
    brew_genl_group.add_argument('-g', '--topological', action='store_true',
                                 help='show dependencies in topological order')
    brew_genl_group.add_argument('-d', '--depth', action='store', type=int, metavar='LEVEL',
                                 help='max display depth of the dependency tree')

    return brew_parser


def parse_args(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    # main parser process
    main_parser = get_dependency_parser()
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
            get_parser = globals().get('get_{}_parser'.format(option))
            if get_parser is None:
                main_parser.error('unrecognized arguments: {}'.format(option))

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
