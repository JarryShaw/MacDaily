# -*- coding: utf-8 -*-

import argparse
import sys

from macdaily.util.const import __version__, bold, reset


def get_uninstall_parser():
    #######################################################
    # Uninstall CLI
    #   * options
    #       - optional arguments
    #       - general arguments
    #       - package arguments
    #       - control arguments
    #   * specifications
    #######################################################

    parser = argparse.ArgumentParser(prog='macdaily-uninstall',
                                     description='Automate macOS Package Uninstaller',
                                     usage='macdaily uninstall [options] <mode-selection> ...',
                                     epilog='aliases: un, unlink, remove, rm, r')
    parser.add_argument('-V', '--version',
                        action='version', version=__version__)
    parser.add_argument('more_opts', nargs=argparse.REMAINDER, help=argparse.SUPPRESS)

    genl_group = parser.add_argument_group(title='general arguments')
    genl_group.add_argument('-a', '--all', action='store_true',
                            help='uninstall all packages installed through Homebrew, Caskroom, and etc')
    genl_group.add_argument('-k', '--dry-run', action='store_true',
                            help=('list all packages which would be removed, '
                                  'but will not actually delete any packages'))
    genl_group.add_argument('-i', '--ignore-dependencies', action='store_true',
                            help='run in non-recursive mode, i.e. ignore dependencies packages')
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

    pkgs_group = parser.add_argument_group(title='package arguments',
                                           description='options used to specify packages of each mode')
    pkgs_group.add_argument('--pip', action='append', nargs='+', default=list(), metavar='PKG', dest='pip_pkgs',
                            help='name of Python packages to uninstall')
    pkgs_group.add_argument('--brew', action='append', nargs='+', default=list(), metavar='FORM', dest='brew_pkgs',
                            help='name of Homebrew formulae to uninstall')
    pkgs_group.add_argument('--cask', action='append', nargs='+', default=list(), metavar='CASK', dest='cask_pkgs',
                            help='name of Caskroom binaries to uninstall')

    ctrl_group = parser.add_argument_group(title='control arguments',
                                           description='options used to disable uninstall of certain mode')
    ctrl_group.add_argument('--no-pip', action='store_true',
                            help='do not uninstall Python packages')
    ctrl_group.add_argument('--no-brew', action='store_true',
                            help='do not uninstall Homebrew formulae')
    ctrl_group.add_argument('--no-cask', action='store_true',
                            help='do not uninstall Caskroom binaries')

    parser.add_argument_group(title='mode selection',
                              description=('uninstall existing packages installed through a specified method, '
                                           'e.g.: pip, brew, cask'))

    return parser


def get_pip_parser():
    #######################################################
    # Pip Uninstall CLI
    #   * options
    #       - optional arguments
    #       - specification arguments
    #       - general arguments
    #       - miscellaneous arguments
    #   * packages
    #######################################################

    pip_parser = argparse.ArgumentParser(prog='macdaily-uninstall-pip',
                                         description='Automate Python Package Uninstaller',
                                         usage='macdaily uninstall pip [options] <packages>')
    pip_parser.add_argument('-V', '--version', action='version', version=__version__)
    pip_parser.add_argument('more_opts', nargs=argparse.REMAINDER, help=argparse.SUPPRESS)

    pip_spec_group = pip_parser.add_argument_group(title='specification arguments')
    pip_spec_group.add_argument('-b', '--brew', action='store_true',
                                help='uninstall packages of Python installed from Homebrew')
    pip_spec_group.add_argument('-c', '--cpython', action='store_true',
                                help='uninstall packages of CPython implementation')
    pip_spec_group.add_argument('-d', '--pre', action='store_true',
                                help='include pre-release and development versions')
    pip_spec_group.add_argument('-e', '--python', action='append', nargs='+',
                                default=list(), metavar='VER', dest='version',
                                help='indicate packages from which version of Python will be uninstalled')
    pip_spec_group.add_argument('-r', '--pypy', action='store_true',
                                help='uninstall packages of PyPy implementation')
    pip_spec_group.add_argument('-s', '--system', action='store_true',
                                help='uninstall packages of Python provided by macOS system')
    pip_spec_group.add_argument('-p', '--packages', action='append', nargs='+', default=list(), metavar='PKG',
                                help='name of Python packages to uninstall')

    pip_genl_group = pip_parser.add_argument_group(title='general arguments')
    pip_genl_group.add_argument('-a', '--all', action='store_true',
                                help='uninstall all Python packages installed through Python Package Index')
    pip_genl_group.add_argument('-k', '--dry-run', action='store_true',
                                help=('list all Python packages which would be removed, '
                                      'but will not actually delete any Python packages'))
    pip_genl_group.add_argument('-i', '--ignore-dependencies', action='store_true',
                                help='run in non-recursive mode, i.e. ignore dependencies packages')
    pip_genl_group.add_argument('-q', '--quiet', action='store_true',
                                help='run in quiet mode, with no output information')
    pip_genl_group.add_argument('-v', '--verbose', action='store_true',
                                help='run in verbose mode, with detailed output information')
    pip_genl_group.add_argument('-y', '--yes', action='store_true',
                                help='yes for all selections')
    pip_genl_group.add_argument('-n', '--no-cleanup', action='store_true',
                                help='do not run cleanup process')

    pip_misc_group = pip_parser.add_argument_group(title='miscellaneous arguments')
    pip_misc_group.add_argument('-L', '--logging', action='store', default=str(), metavar='ARG',
                                help="options for `{}pip freeze{}' command".format(bold, reset))
    pip_misc_group.add_argument('-U', '--uninstall', action='store', default=str(), metavar='ARG',
                                help="options for `{}pip uninstall <package>{}' command".format(bold, reset))

    return pip_parser


def get_brew_parser():
    #######################################################
    # Brew Uninstall CLI
    #   * options
    #       - optional arguments
    #       - specification arguments
    #       - general arguments
    #       - miscellaneous arguments
    #   * packages
    #######################################################

    brew_parser = argparse.ArgumentParser(prog='macdaily-uninstall-brew',
                                          description='Automate Homebrew Formula Uninstaller',
                                          usage='macdaily uninstall brew [options] <formulae>')
    brew_parser.add_argument('-V', '--version', action='version', version=__version__)
    brew_parser.add_argument('more_opts', nargs=argparse.REMAINDER, help=argparse.SUPPRESS)

    brew_spec_group = brew_parser.add_argument_group(title='specification arguments')
    brew_spec_group.add_argument('-f', '--force', action='store_true',
                                 help='delete all installed versions')
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
                                 help='name of Homebrew formulae to uninstall')

    brew_genl_group = brew_parser.add_argument_group(title='general arguments')
    brew_genl_group.add_argument('-a', '--all', action='store_true',
                                 help='uninstall all Homebrew formulae installed through Homebrew')
    brew_genl_group.add_argument('-k', '--dry-run', action='store_true',
                                 help=('list all Homebrew formulae which would be removed, '
                                       'but will not actually delete any Homebrew formulae'))
    brew_genl_group.add_argument('-i', '--ignore-dependencies', action='store_true',
                                 help='run in non-recursive mode, i.e. ignore dependencies packages')
    brew_genl_group.add_argument('-q', '--quiet', action='store_true',
                                 help='run in quiet mode, with no output information')
    brew_genl_group.add_argument('-v', '--verbose', action='store_true',
                                 help='run in verbose mode, with detailed output information')
    brew_genl_group.add_argument('-y', '--yes', action='store_true',
                                 help='yes for all selections')
    brew_genl_group.add_argument('-n', '--no-cleanup', action='store_true',
                                 help='do not run cleanup process')

    brew_misc_group = brew_parser.add_argument_group(title='miscellaneous arguments')
    brew_misc_group.add_argument('-L', '--logging', action='store', default=str(), metavar='ARG',
                                 help="options for `{}brew list{}' command".format(bold, reset))
    brew_misc_group.add_argument('-U', '--uninstall', action='store', default=str(), metavar='ARG',
                                 help="options for `{}brew uninstall <formula>{}' command".format(bold, reset))

    return brew_parser


def get_cask_parser():
    #######################################################
    # Cask Uninstall CLI
    #   * options
    #       - optional arguments
    #       - specification arguments
    #       - general arguments
    #       - miscellaneous arguments
    #   * packages
    #######################################################

    cask_parser = argparse.ArgumentParser(prog='macdaily-uninstall-cask',
                                          description='Automate Homebrew Cask Uninstaller',
                                          usage='macdaily uninstall cask [options] <casks>')
    cask_parser.add_argument('-V', '--version', action='version', version=__version__)
    cask_parser.add_argument('more_opts', nargs=argparse.REMAINDER, help=argparse.SUPPRESS)

    cask_spec_group = cask_parser.add_argument_group(title='specification arguments')
    cask_spec_group.add_argument('-f', '--force', action='store_true',
                                 help='uninstall even if the Cask does not appear to be present')
    cask_spec_group.add_argument('-p', '--packages', action='append', nargs='+', default=list(), metavar='CASK',
                                 help='name of Caskroom binaries to uninstall')

    cask_genl_group = cask_parser.add_argument_group(title='general arguments')
    cask_genl_group.add_argument('-a', '--all', action='store_true',
                                 help='uninstall all Caskroom binaries installed through Homebrew')
    cask_genl_group.add_argument('-k', '--dry-run', action='store_true',
                                 help=('list all Caskroom binaries which would be removed, '
                                       'but will not actually delete any Caskroom binaries'))
    cask_genl_group.add_argument('-q', '--quiet', action='store_true',
                                 help='run in quiet mode, with no output information')
    cask_genl_group.add_argument('-v', '--verbose', action='store_true',
                                 help='run in verbose mode, with detailed output information')
    cask_genl_group.add_argument('-y', '--yes', action='store_true',
                                 help='yes for all selections')
    cask_genl_group.add_argument('-n', '--no-cleanup', action='store_true',
                                 help='do not run cleanup process')

    cask_misc_group = cask_parser.add_argument_group(title='miscellaneous arguments')
    cask_misc_group.add_argument('-L', '--logging', action='store', default=str(), metavar='ARG',
                                 help="options for `{}brew cask list{}' command".format(bold, reset))
    cask_misc_group.add_argument('-U', '--uninstall', action='store', default=str(), metavar='ARG',
                                 help="options for `{}brew cask uninstall <cask>{}' command".format(bold, reset))

    return cask_parser


def parse_args(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    # main parser process
    main_parser = get_uninstall_parser()
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
