# -*- coding: utf-8 -*-

import argparse
import sys

from macdaily.util.const import __version__


def get_logging_parser():
    #######################################################
    # Logging CLI
    #   * options
    #       - optional arguments
    #       - specification arguments
    #       - general arguments
    #       - miscellaneous arguments
    #   * packages
    #######################################################

    parser = argparse.ArgumentParser(prog='macdaily-logging',
                                     description='macOS Package Logging Automator',
                                     usage='macdaily logging [options] <mode-selection> ...',
                                     epilog='aliases: log')
    parser.add_argument('-V', '--version', action='version', version=__version__)
    parser.add_argument('more_opts', nargs=argparse.REMAINDER, help=argparse.SUPPRESS)

    genl_group = parser.add_argument_group(title='general arguments')
    genl_group.add_argument('-a', '--all', action='store_true',
                            help=('log all packages installed through Atom, RubyGems, Node.js, '
                                  'Homebrew, Caskroom, Mac App Store, and etc'))
    genl_group.add_argument('-q', '--quiet', action='store_true',
                            help='run in quiet mode, with no output information')
    genl_group.add_argument('-v', '--verbose', action='store_true',
                            help='run in verbose mode, with detailed output information')
    genl_group.add_argument('-n', '--no-cleanup', action='store_true',
                            help='do not run cleanup process')
    genl_group.add_argument('-l', '--show-log', action='store_true',
                            help='open log in Console.app upon completion of command')

    ctrl_group = parser.add_argument_group(title='control arguments',
                                           description='options used to disable logging of certain mode')
    ctrl_group.add_argument('--no-apm', action='store_true', help='do not log Atom plug-ins')
    ctrl_group.add_argument('--no-app', action='store_true', help='do not log system applications')
    ctrl_group.add_argument('--no-gem', action='store_true', help='do not log Ruby gems')
    ctrl_group.add_argument('--no-mas', action='store_true', help='do not log macOS applications')
    ctrl_group.add_argument('--no-npm', action='store_true', help='do not log Node.js modules')
    ctrl_group.add_argument('--no-pip', action='store_true', help='do not log Python packages')
    ctrl_group.add_argument('--no-tap', action='store_true', help='do not log Homebrew Taps')
    ctrl_group.add_argument('--no-brew', action='store_true', help='do not log Homebrew formulae')
    ctrl_group.add_argument('--no-cask', action='store_true', help='do not log Homebrew Casks')

    parser.add_argument_group(title='mode selection',
                              description=('log existing packages installed through a specified method, '
                                           'e.g.: apm, app, gem, mas, npm, pip, tap, brew, cask'))

    return parser


def get_apm_parser():
    #######################################################
    # Apm Logging CLI
    #   * options
    #       - optional arguments
    #       - specification arguments
    #       - general arguments
    #       - miscellaneous arguments
    #   * packages
    #######################################################

    apm_parser = argparse.ArgumentParser(prog='macdaily-logging-apm',
                                         description='Atom Plug-In Logging Automator',
                                         usage='macdaily logging apm [options] ...')
    apm_parser.add_argument('-V', '--version', action='version', version=__version__)
    apm_parser.add_argument('more_opts', nargs=argparse.REMAINDER, help=argparse.SUPPRESS)

    apm_spec_group = apm_parser.add_argument_group(title='specification arguments')
    apm_spec_group.add_argument('-b', '--beta', action='store_true',
                                help='log Atom Beta plug-ins')

    apm_genl_group = apm_parser.add_argument_group(title='general arguments')
    apm_genl_group.add_argument('-q', '--quiet', action='store_true',
                                help='run in quiet mode, with no output information')
    apm_genl_group.add_argument('-v', '--verbose', action='store_true',
                                help='run in verbose mode, with detailed output information')
    apm_genl_group.add_argument('-n', '--no-cleanup', action='store_true',
                                help='do not run cleanup process')
    apm_genl_group.add_argument('-l', '--show-log', action='store_true',
                                help='open log in Console.app upon completion of command')

    return apm_parser


def get_app_parser():
    #######################################################
    # App Logging CLI
    #   * options
    #       - optional arguments
    #       - specification arguments
    #       - general arguments
    #       - miscellaneous arguments
    #   * packages
    #######################################################

    app_parser = argparse.ArgumentParser(prog='macdaily-logging-app',
                                         description='Mac Application Logging Automator',
                                         usage='macdaily logging app [options] ...')
    app_parser.add_argument('-V', '--version', action='version', version=__version__)
    app_parser.add_argument('more_opts', nargs=argparse.REMAINDER, help=argparse.SUPPRESS)

    app_genl_group = app_parser.add_argument_group(title='general arguments')
    app_genl_group.add_argument('-q', '--quiet', action='store_true',
                                help='run in quiet mode, with no output information')
    app_genl_group.add_argument('-v', '--verbose', action='store_true',
                                help='run in verbose mode, with detailed output information')
    app_genl_group.add_argument('-n', '--no-cleanup', action='store_true',
                                help='do not run cleanup process')
    app_genl_group.add_argument('-l', '--show-log', action='store_true',
                                help='open log in Console.app upon completion of command')

    return app_parser


def get_gem_parser():
    #######################################################
    # Gem Logging CLI
    #   * options
    #       - optional arguments
    #       - specification arguments
    #       - general arguments
    #       - miscellaneous arguments
    #   * packages
    #######################################################

    gem_parser = argparse.ArgumentParser(prog='macdaily-logging-gem',
                                         description='Ruby Gem Logging Automator',
                                         usage='macdaily logging gem [options] ...')
    gem_parser.add_argument('-V', '--version', action='version', version=__version__)
    gem_parser.add_argument('more_opts', nargs=argparse.REMAINDER, help=argparse.SUPPRESS)

    gem_spec_group = gem_parser.add_argument_group(title='specification arguments')
    gem_spec_group.add_argument('-b', '--brew', action='store_true',
                                help='log gems of Ruby installed from Homebrew')
    gem_spec_group.add_argument('-s', '--system', action='store_true',
                                help='log gems of Ruby provided by macOS system')

    gem_genl_group = gem_parser.add_argument_group(title='general arguments')
    gem_genl_group.add_argument('-q', '--quiet', action='store_true',
                                help='run in quiet mode, with no output information')
    gem_genl_group.add_argument('-v', '--verbose', action='store_true',
                                help='run in verbose mode, with detailed output information')
    gem_genl_group.add_argument('-n', '--no-cleanup', action='store_true',
                                help='do not run cleanup process')
    gem_genl_group.add_argument('-l', '--show-log', action='store_true',
                                help='open log in Console.app upon completion of command')

    return gem_parser


def get_mas_parser():
    #######################################################
    # Mas Logging CLI
    #   * options
    #       - optional arguments
    #       - general arguments
    #       - miscellaneous arguments
    #   * packages
    #######################################################

    mas_parser = argparse.ArgumentParser(prog='macdaily-logging-mas',
                                         description='macOS Application Logging Automator',
                                         usage='macdaily logging mas [options] ...')
    mas_parser.add_argument('-V', '--version', action='version', version=__version__)
    mas_parser.add_argument('more_opts', nargs=argparse.REMAINDER, help=argparse.SUPPRESS)

    mas_genl_group = mas_parser.add_argument_group(title='general arguments')
    mas_genl_group.add_argument('-q', '--quiet', action='store_true',
                                help='run in quiet mode, with no output information')
    mas_genl_group.add_argument('-v', '--verbose', action='store_true',
                                help='run in verbose mode, with detailed output information')
    mas_genl_group.add_argument('-n', '--no-cleanup', action='store_true',
                                help='do not run cleanup process')
    mas_genl_group.add_argument('-l', '--show-log', action='store_true',
                                help='open log in Console.app upon completion of command')

    return mas_parser


def get_npm_parser():
    #######################################################
    # Npm Logging CLI
    #   * options
    #       - optional arguments
    #       - general arguments
    #       - miscellaneous arguments
    #   * packages
    #######################################################

    npm_parser = argparse.ArgumentParser(prog='macdaily-logging-npm',
                                         description='Node.js Module Logging Automator',
                                         usage='macdaily logging npm [options] ...')
    npm_parser.add_argument('-V', '--version', action='version', version=__version__)
    npm_parser.add_argument('more_opts', nargs=argparse.REMAINDER, help=argparse.SUPPRESS)

    npm_spec_group = npm_parser.add_argument_group(title='specification arguments')
    npm_spec_group.add_argument('-i', '--long', action='store_true',
                                help='show extended information')

    npm_genl_group = npm_parser.add_argument_group(title='general arguments')
    npm_genl_group.add_argument('-q', '--quiet', action='store_true',
                                help='run in quiet mode, with no output information')
    npm_genl_group.add_argument('-v', '--verbose', action='store_true',
                                help='run in verbose mode, with detailed output information')
    npm_genl_group.add_argument('-n', '--no-cleanup', action='store_true',
                                help='do not run cleanup process')
    npm_genl_group.add_argument('-l', '--show-log', action='store_true',
                                help='open log in Console.app upon completion of command')

    return npm_parser


def get_pip_parser():
    #######################################################
    # Pip Logging CLI
    #   * options
    #       - optional arguments
    #       - specification arguments
    #       - general arguments
    #       - miscellaneous arguments
    #   * packages
    #######################################################

    pip_parser = argparse.ArgumentParser(prog='macdaily-logging-pip',
                                         description='Python Package Logging Automator',
                                         usage=('macdaily logging pip [options] ...'))
    pip_parser.add_argument('-V', '--version', action='version', version=__version__)
    pip_parser.add_argument('more_opts', nargs=argparse.REMAINDER, help=argparse.SUPPRESS)

    pip_spec_group = pip_parser.add_argument_group(title='specification arguments')
    pip_spec_group.add_argument('-x', '--exclude-editable', action='store_true',
                                help='exclude editable package from output')
    pip_spec_group.add_argument('-b', '--brew', action='store_true',
                                help='log packages of Python installed from Homebrew')
    pip_spec_group.add_argument('-c', '--cpython', action='store_true',
                                help='log packages of CPython implementation')
    pip_spec_group.add_argument('-e', '--python', action='append', nargs='+',
                                default=list(), metavar='VER', dest='version',
                                help='indicate packages from which version of Python will be logged')
    pip_spec_group.add_argument('-r', '--pypy', action='store_true',
                                help='log packages of PyPy implementation')
    pip_spec_group.add_argument('-s', '--system', action='store_true',
                                help='log packages of Python provided by macOS system')

    pip_genl_group = pip_parser.add_argument_group(title='general arguments')
    pip_genl_group.add_argument('-q', '--quiet', action='store_true',
                                help='run in quiet mode, with no output information')
    pip_genl_group.add_argument('-v', '--verbose', action='store_true',
                                help='run in verbose mode, with detailed output information')
    pip_genl_group.add_argument('-n', '--no-cleanup', action='store_true',
                                help='do not run cleanup process')
    pip_genl_group.add_argument('-l', '--show-log', action='store_true',
                                help='open log in Console.app upon completion of command')

    return pip_parser


def get_tap_parser():
    #######################################################
    # Tap Logging CLI
    #   * options
    #       - optional arguments
    #       - specification arguments
    #       - general arguments
    #       - miscellaneous arguments
    #   * packages
    #######################################################

    tap_parser = argparse.ArgumentParser(prog='macdaily-logging-tap',
                                         description='Homebrew Tap Logging Automator',
                                         usage='macdaily logging tap [options] ...')
    tap_parser.add_argument('-V', '--version', action='version', version=__version__)
    tap_parser.add_argument('more_opts', nargs=argparse.REMAINDER, help=argparse.SUPPRESS)

    tap_genl_group = tap_parser.add_argument_group(title='general arguments')
    tap_genl_group.add_argument('-q', '--quiet', action='store_true',
                                help='run in quiet mode, with no output information')
    tap_genl_group.add_argument('-v', '--verbose', action='store_true',
                                help='run in verbose mode, with detailed output information')
    tap_genl_group.add_argument('-n', '--no-cleanup', action='store_true',
                                help='do not run cleanup process')
    tap_genl_group.add_argument('-l', '--show-log', action='store_true',
                                help='open log in Console.app upon completion of command')

    return tap_parser


def get_brew_parser():
    #######################################################
    # Brew Logging CLI
    #   * options
    #       - optional arguments
    #       - specification arguments
    #       - general arguments
    #       - miscellaneous arguments
    #   * packages
    #######################################################

    brew_parser = argparse.ArgumentParser(prog='macdaily-logging-brew',
                                          description='Homebrew Formula Logging Automator',
                                          usage='macdaily logging brew [options] ...')
    brew_parser.add_argument('-V', '--version', action='version', version=__version__)
    brew_parser.add_argument('more_opts', nargs=argparse.REMAINDER, help=argparse.SUPPRESS)

    brew_genl_group = brew_parser.add_argument_group(title='general arguments')
    brew_genl_group.add_argument('-q', '--quiet', action='store_true',
                                 help='run in quiet mode, with no output information')
    brew_genl_group.add_argument('-v', '--verbose', action='store_true',
                                 help='run in verbose mode, with detailed output information')
    brew_genl_group.add_argument('-n', '--no-cleanup', action='store_true',
                                 help='do not run cleanup process')
    brew_genl_group.add_argument('-l', '--show-log', action='store_true',
                                 help='open log in Console.app upon completion of command')

    return brew_parser


def get_cask_parser():
    #######################################################
    # Cask Logging CLI
    #   * options
    #       - optional arguments
    #       - specification arguments
    #       - general arguments
    #       - miscellaneous arguments
    #   * packages
    #######################################################

    cask_parser = argparse.ArgumentParser(prog='macdaily-logging-cask',
                                          description='Homebrew Cask Logging Automator',
                                          usage='macdaily logging cask [options] ...')
    cask_parser.add_argument('-V', '--version', action='version', version=__version__)
    cask_parser.add_argument('more_opts', nargs=argparse.REMAINDER, help=argparse.SUPPRESS)

    cask_genl_group = cask_parser.add_argument_group(title='general arguments')
    cask_genl_group.add_argument('-q', '--quiet', action='store_true',
                                 help='run in quiet mode, with no output information')
    cask_genl_group.add_argument('-v', '--verbose', action='store_true',
                                 help='run in verbose mode, with detailed output information')
    cask_genl_group.add_argument('-n', '--no-cleanup', action='store_true',
                                 help='do not run cleanup process')
    cask_genl_group.add_argument('-l', '--show-log', action='store_true',
                                 help='open log in Console.app upon completion of command')

    return cask_parser


def parse_args(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    # main parser process
    main_parser = get_logging_parser()
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
