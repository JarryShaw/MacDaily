# -*- coding: utf-8 -*-

import argparse
import re
import sys

from macdaily.util.const.macro import CMD_REINSTALL, MAP_DICT, STR_BREW, STR_CASK, STR_REINSTALL
from macdaily.util.const.macro import VERSION as __version__
from macdaily.util.const.term import bold, reset


def get_reinstall_parser():
    #######################################################
    # Reinstall CLI
    #   * options
    #       - optional arguments
    #       - general arguments
    #       - package arguments
    #       - control arguments
    #   * specifications
    #######################################################

    parser = argparse.ArgumentParser(prog='macdaily-reinstall',
                                     description='Automated macOS Package Reinstaller',
                                     usage='macdaily reinstall [options] <mode-selection> ...',
                                     epilog=STR_REINSTALL)
    parser.add_argument('-V', '--version', action='version', version=__version__)
    parser.add_argument('more_opts', nargs=argparse.REMAINDER, help=argparse.SUPPRESS)

    genl_group = parser.add_argument_group(title='general arguments')
    genl_group.add_argument('-a', '--all', action='store_true',
                            help='reinstall all packages installed through Homebrew, Caskroom, and etc')
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
    pkgs_group.add_argument('--brew', action='append', nargs='+', default=list(), metavar='FORM', dest='brew_pkgs',
                            help='name of Homebrew formulae to reinstall')
    pkgs_group.add_argument('--cask', action='append', nargs='+', default=list(), metavar='CASK', dest='cask_pkgs',
                            help='name of Caskroom binaries to reinstall')

    ctrl_group = parser.add_argument_group(title='control arguments',
                                           description='options used to disable reinstall of certain mode')
    ctrl_group.add_argument('--no-brew', action='store_true',
                            help='do not reinstall Homebrew formulae')
    ctrl_group.add_argument('--no-cask', action='store_true',
                            help='do not reinstall Caskroom binaries')

    parser.add_argument_group(title='mode selection',
                              description=('reinstall existing packages installed through a specified method, '
                                           'e.g.: brew, cask'))

    return parser


def get_brew_parser():
    #######################################################
    # Brew Reinstall CLI
    #   * options
    #       - optional arguments
    #       - specification arguments
    #       - general arguments
    #       - miscellaneous arguments
    #   * packages
    #######################################################

    brew_parser = argparse.ArgumentParser(prog='macdaily-reinstall-brew',
                                          description='Automated Homebrew Formula Reinstaller',
                                          usage='macdaily reinstall brew [options] <formulae> ...',
                                          epilog=STR_BREW)
    brew_parser.add_argument('-V', '--version', action='version', version=__version__)
    brew_parser.add_argument('more_opts', nargs=argparse.REMAINDER, help=argparse.SUPPRESS)

    brew_spec_group = brew_parser.add_argument_group(title='specification arguments')
    brew_spec_group.add_argument('-s', '--startswith', action='store', metavar='PREFIX',
                                 help='reinstall procedure starts from such formula, sort in initial alphabets')
    brew_spec_group.add_argument('-e', '--endswith', action='store', metavar='SUFFIX',
                                 help='reinstall procedure ends after such formula, sort in initial alphabets')
    brew_spec_group.add_argument('-p', '--packages', action='append', nargs='+', default=list(), metavar='FORM',
                                 help='name of Homebrew formulae to reinstall')

    brew_genl_group = brew_parser.add_argument_group(title='general arguments')
    brew_genl_group.add_argument('-a', '--all', action='store_true',
                                 help='reinstall all Homebrew formulae installed through Homebrew')
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
                                 help=f"options for `{bold}brew list{reset}' command")
    brew_misc_group.add_argument('-R', '--reinstall', action='store', default=str(), metavar='ARG',
                                 help=f"options for `{bold}brew reinstall <formula>{reset}' command")

    return brew_parser


def get_cask_parser():
    #######################################################
    # Cask Reinstall CLI
    #   * options
    #       - optional arguments
    #       - specification arguments
    #       - general arguments
    #       - miscellaneous arguments
    #   * packages
    #######################################################

    cask_parser = argparse.ArgumentParser(prog='macdaily-reinstall-cask',
                                          description='Automated Homebrew Cask Reinstaller',
                                          usage='macdaily reinstall cask [options] <casks> ...',
                                          epilog=STR_CASK)
    cask_parser.add_argument('-V', '--version', action='version', version=__version__)
    cask_parser.add_argument('more_opts', nargs=argparse.REMAINDER, help=argparse.SUPPRESS)

    cask_spec_group = cask_parser.add_argument_group(title='specification arguments')
    cask_spec_group.add_argument('-s', '--startswith', action='store', metavar='PREFIX',
                                 help='reinstall procedure starts from such binary, sort in initial alphabets')
    cask_spec_group.add_argument('-e', '--endswith', action='store', metavar='SUFFIX',
                                 help='reinstall procedure ends after such binary, sort in initial alphabets')
    cask_spec_group.add_argument('-f', '--force', action='store_true',
                                 help='reinstall even if the Cask does not appear to be present')
    cask_spec_group.add_argument('-t', '--no-quarantine', action='store_true',
                                 help='prevent Gatekeeper from enforcing its security restrictions on the Cask')
    cask_spec_group.add_argument('-p', '--packages', action='append', nargs='+', default=list(), metavar='CASK',
                                 help='name of Caskroom binaries to reinstall')

    cask_genl_group = cask_parser.add_argument_group(title='general arguments')
    cask_genl_group.add_argument('-a', '--all', action='store_true',
                                 help='reinstall all Caskroom binaries installed through Homebrew')
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
                                 help=f"options for `{bold}brew cask list{reset}' command")
    cask_misc_group.add_argument('-R', '--reinstall', action='store', default=str(), metavar='ARG',
                                 help=f"options for `{bold}brew cask reinstall <cask>{reset}' command")

    return cask_parser


def parse_args(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    # main parser process
    main_parser = get_reinstall_parser()
    main_args = main_parser.parse_args(argv or ['--help'])

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
            parser_name = MAP_DICT.get(option.lower(), 'null')
            get_parser = globals().get(f'get_{parser_name}_parser')
            if get_parser is None:
                pattern = rf'.*{option}.*'
                matches = f"', '".join(filter(lambda s: re.match(pattern, s, re.IGNORECASE), CMD_REINSTALL))  # pylint: disable=cell-var-from-loop
                if matches:
                    main_parser.error(f'unrecognized arguments: {option!r} '
                                      f"(did you mean: '{matches}')")
                else:
                    main_parser.error(f'unrecognized arguments: {option!r}')

            # parse mode arguments
            parser = get_parser()
            args = parser.parse_args(more_opts[index:] or ['--help'])

            # store/update parsed arguments
            opt_dict = getattr(main_args, option, dict())
            opt_dict.pop('more_opts', None)
            setattr(main_args, option, _update(opt_dict, vars(args)))

            # check for extra options
            more_opts = args.more_opts
            break

    delattr(main_args, 'more_opts')
    return main_args
