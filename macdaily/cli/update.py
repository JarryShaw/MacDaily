# -*- coding: utf-8 -*-

import argparse
import sys

from macdaily.util.const import __version__, bold, reset


def get_update_parser():
    #######################################################
    # Update CLI
    #   * options
    #       - optional arguments
    #       - general arguments
    #       - package arguments
    #       - control arguments
    #   * specifications
    #######################################################

    parser = argparse.ArgumentParser(prog='macdaily update',
                                     description='macOS Package Update Automator',
                                     usage='macdaily update [options] <mode-selection> ...',
                                     epilog='aliases: up, upgrade')
    parser.add_argument('-V', '--version', action='version', version=__version__)
    parser.add_argument('more_opts', nargs=argparse.REMAINDER, help=argparse.SUPPRESS)

    genl_group = parser.add_argument_group(title='general arguments')
    genl_group.add_argument('-a', '--all', action='store_true',
                            help=('update all packages installed through Atom, RubyGems, Node.js, '
                                  'Homebrew, Caskroom, Mac App Store, and etc'))
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
    pkgs_group.add_argument('--apm', action='append', nargs='+', default=list(), metavar='PI', dest='apm_pkgs',
                            help='name of Atom plug-ins to update')
    pkgs_group.add_argument('--gem', action='append', nargs='+', default=list(), metavar='GEM', dest='gem_pkgs',
                            help='name of Ruby gems to update')
    pkgs_group.add_argument('--mas', action='append', nargs='+', default=list(), metavar='APP', dest='mas_pkgs',
                            help='name of macOS applications to update')
    pkgs_group.add_argument('--npm', action='append', nargs='+', default=list(), metavar='MOD', dest='npm_pkgs',
                            help='name of Node.js modules to update')
    pkgs_group.add_argument('--pip', action='append', nargs='+', default=list(), metavar='PKG', dest='pip_pkgs',
                            help='name of Python packages to update')
    pkgs_group.add_argument('--brew', action='append', nargs='+', default=list(), metavar='FORM', dest='brew_pkgs',
                            help='name of Homebrew formulae to update')
    pkgs_group.add_argument('--cask', action='append', nargs='+', default=list(), metavar='CASK', dest='cask_pkgs',
                            help='name of Caskroom binaries to update')
    pkgs_group.add_argument('--system', action='append', nargs='+', default=list(), metavar='SW', dest='system_pkgs',
                            help='name of system software to update')

    ctrl_group = parser.add_argument_group(title='control arguments',
                                           description='options used to disable update of certain mode')
    ctrl_group.add_argument('--no-apm', action='store_true', help='do not update Atom plug-ins')
    ctrl_group.add_argument('--no-gem', action='store_true', help='do not update Ruby gems')
    ctrl_group.add_argument('--no-mas', action='store_true', help='do not update macOS applications')
    ctrl_group.add_argument('--no-npm', action='store_true', help='do not update Node.js modules')
    ctrl_group.add_argument('--no-pip', action='store_true', help='do not update Python packages')
    ctrl_group.add_argument('--no-brew', action='store_true', help='do not update Homebrew formulae')
    ctrl_group.add_argument('--no-cask', action='store_true', help='do not update Caskroom binaries')
    ctrl_group.add_argument('--no-system', action='store_true', help='do not update system software')

    parser.add_argument_group(title='mode selection',
                              description=('update outdated packages installed through a specified method, '
                                           'e.g.: apm, gem, mas, npm, pip, brew, cask, system'))

    return parser


def get_apm_parser():
    #######################################################
    # Apm Update CLI
    #   * options
    #       - optional arguments
    #       - specification arguments
    #       - general arguments
    #       - miscellaneous arguments
    #   * packages
    #######################################################

    apm_parser = argparse.ArgumentParser(prog='macdaily update apm',
                                         description='Atom Plug-In Update Automator',
                                         usage='macdaily update apm [options] <plug-ins>')
    apm_parser.add_argument('-V', '--version', action='version', version=__version__)
    apm_parser.add_argument('more_opts', nargs=argparse.REMAINDER, help=argparse.SUPPRESS)

    apm_spec_group = apm_parser.add_argument_group(title='specification arguments')
    apm_spec_group.add_argument('-b', '--beta', action='store_true',
                                help='update Atom Beta plug-ins')
    apm_spec_group.add_argument('-p', '--packages', action='append', nargs='+', default=list(), metavar='PI',
                                help='name of Atom plug-ins to update')

    apm_genl_group = apm_parser.add_argument_group(title='general arguments')
    apm_genl_group.add_argument('-a', '--all', action='store_true',
                                help='update all plug-ins installed through Atom Package Manager')
    apm_genl_group.add_argument('-q', '--quiet', action='store_true',
                                help='run in quiet mode, with no output information')
    apm_genl_group.add_argument('-v', '--verbose', action='store_true',
                                help='run in verbose mode, with detailed output information')
    apm_genl_group.add_argument('-y', '--yes', action='store_true',
                                help='yes for all selections')

    apm_misc_group = apm_parser.add_argument_group(title='miscellaneous arguments')
    apm_misc_group.add_argument('-L', '--logging', action='store', default=str(), metavar='ARG',
                                help="options for `{}apm upgrade --list{}' command".format(bold, reset))
    apm_misc_group.add_argument('-U', '- update', action='store', default=str(), metavar='ARG',
                                help="options for `{}apm upgrade <plug-in>{}' command".format(bold, reset))

    return apm_parser


def get_gem_parser():
    #######################################################
    # Gem Update CLI
    #   * options
    #       - optional arguments
    #       - specification arguments
    #       - general arguments
    #       - miscellaneous arguments
    #   * packages
    #######################################################

    gem_parser = argparse.ArgumentParser(prog='macdaily update gem',
                                         description='Ruby Gem Update Automator',
                                         usage='macdaily update gem [options] <gems>')
    gem_parser.add_argument('-V', '--version', action='version', version=__version__)
    gem_parser.add_argument('more_opts', nargs=argparse.REMAINDER, help=argparse.SUPPRESS)

    gem_spec_group = gem_parser.add_argument_group(title='specification arguments')
    gem_spec_group.add_argument('-b', '--brew', action='store_true',
                                help='update gems of Ruby installed from Homebrew')
    gem_spec_group.add_argument('-s', '--system', action='store_true',
                                help='update gems of Ruby provided by macOS system')
    gem_spec_group.add_argument('-p', '--packages', action='append', nargs='+', default=list(), metavar='GEM',
                                help='name of Ruby gems to update')

    gem_genl_group = gem_parser.add_argument_group(title='general arguments')
    gem_genl_group.add_argument('-a', '--all', action='store_true',
                                help='update all gems installed through RubyGems')
    gem_genl_group.add_argument('-q', '--quiet', action='store_true',
                                help='run in quiet mode, with no output information')
    gem_genl_group.add_argument('-v', '--verbose', action='store_true',
                                help='run in verbose mode, with detailed output information')
    gem_genl_group.add_argument('-y', '--yes', action='store_true',
                                help='yes for all selections')

    gem_misc_group = gem_parser.add_argument_group(title='miscellaneous arguments')
    gem_misc_group.add_argument('-L', '--logging', action='store', default=str(), metavar='ARG',
                                help="options for `{}gem outdated{}' command".format(bold, reset))
    gem_misc_group.add_argument('-U', '- update', action='store', default=str(), metavar='ARG',
                                help="options for `{}gem update <gem>{}' command".format(bold, reset))

    return gem_parser


def get_mas_parser():
    #######################################################
    # Mas Update CLI
    #   * options
    #       - optional arguments
    #       - general arguments
    #       - miscellaneous arguments
    #   * packages
    #######################################################

    mas_parser = argparse.ArgumentParser(prog='macdaily update mas',
                                         description='macOS Application Update Automator',
                                         usage='macdaily update mas [options] <applications>')
    mas_parser.add_argument('-V', '--version', action='version', version=__version__)
    mas_parser.add_argument('more_opts', nargs=argparse.REMAINDER, help=argparse.SUPPRESS)

    mas_spec_group = mas_parser.add_argument_group(title='specification arguments')
    mas_spec_group.add_argument('-p', '--packages', action='append', nargs='+', default=list(), metavar='APP',
                                help='name of macOS applications to update')

    mas_genl_group = mas_parser.add_argument_group(title='general arguments')
    mas_genl_group.add_argument('-a', '--all', action='store_true',
                                help='update all macOS applications installed through Mac App Store')
    mas_genl_group.add_argument('-q', '--quiet', action='store_true',
                                help='run in quiet mode, with no output information')
    mas_genl_group.add_argument('-v', '--verbose', action='store_true',
                                help='run in verbose mode, with detailed output information')
    mas_genl_group.add_argument('-y', '--yes', action='store_true',
                                help='yes for all selections')

    mas_misc_group = mas_parser.add_argument_group(title='miscellaneous arguments')
    mas_misc_group.add_argument('-L', '--logging', action='store', default=str(), metavar='ARG',
                                help="options for `{}mas outdated' command{}".format(bold, reset))
    mas_misc_group.add_argument('-U', '- update', action='store', default=str(), metavar='ARG',
                                help="options for `{}mas upgrade <application>{}' command".format(bold, reset))

    return mas_parser


def get_npm_parser():
    #######################################################
    # Npm Update CLI
    #   * options
    #       - optional arguments
    #       - general arguments
    #       - miscellaneous arguments
    #   * packages
    #######################################################

    npm_parser = argparse.ArgumentParser(prog='macdaily update npm',
                                         description='Node.js Module Update Automator',
                                         usage='macdaily update npm [options] <modules>')
    npm_parser.add_argument('-V', '--version', action='version', version=__version__)
    npm_parser.add_argument('more_opts', nargs=argparse.REMAINDER, help=argparse.SUPPRESS)

    npm_spec_group = npm_parser.add_argument_group(title='specification arguments')
    npm_spec_group.add_argument('-p', '--packages', action='append', nargs='+', default=list(), metavar='MOD',
                                help='name of Node.js modules to update')

    npm_genl_group = npm_parser.add_argument_group(title='general arguments')
    npm_genl_group.add_argument('-a', '--all', action='store_true',
                                help='update all Node.js modules installed through Node.js Package Manager')
    npm_genl_group.add_argument('-q', '--quiet', action='store_true',
                                help='run in quiet mode, with no output information')
    npm_genl_group.add_argument('-v', '--verbose', action='store_true',
                                help='run in verbose mode, with detailed output information')
    npm_genl_group.add_argument('-y', '--yes', action='store_true',
                                help='yes for all selections')
    npm_genl_group.add_argument('-n', '--no-cleanup', action='store_true',
                                help='do not run cleanup process')

    npm_misc_group = npm_parser.add_argument_group(title='miscellaneous arguments')
    npm_misc_group.add_argument('-L', '--logging', action='store', default=str(), metavar='ARG',
                                help="options for `{}npm outdated --global{}' command".format(bold, reset))
    npm_misc_group.add_argument('-U', '- update', action='store', default=str(), metavar='ARG',
                                help="options for `{}npm upgrade --global <module>{}' command".format(bold, reset))

    return npm_parser


def get_pip_parser():
    #######################################################
    # Pip Update CLI
    #   * options
    #       - optional arguments
    #       - specification arguments
    #       - general arguments
    #       - miscellaneous arguments
    #   * packages
    #######################################################

    pip_parser = argparse.ArgumentParser(prog='macdaily update pip',
                                         description='Python Package Update Automator',
                                         usage='macdaily update pip [options] <packages>')
    pip_parser.add_argument('-V', '--version', action='version', version=__version__)
    pip_parser.add_argument('more_opts', nargs=argparse.REMAINDER, help=argparse.SUPPRESS)

    pip_spec_group = pip_parser.add_argument_group(title='specification arguments')
    pip_spec_group.add_argument('-u', '--user', action='store_true',
                                help='install to the Python user install directory for your platform')
    pip_spec_group.add_argument('-b', '--brew', action='store_true',
                                help='update packages of Python installed from Homebrew')
    pip_spec_group.add_argument('-c', '--cpython', action='store_true',
                                help='update packages of CPython implementation')
    pip_spec_group.add_argument('-d', '--pre', action='store_true',
                                help='include pre-release and development versions')
    pip_spec_group.add_argument('-e', '--python', action='append', nargs='+',
                                default=list(), metavar='VER', dest='version',
                                help='indicate packages from which version of Python will update')
    pip_spec_group.add_argument('-r', '--pypy', action='store_true',
                                help='update packages of PyPy implementation')
    pip_spec_group.add_argument('-s', '--system', action='store_true',
                                help='update packages of Python provided by macOS system')
    pip_spec_group.add_argument('-p', '--packages', action='append', nargs='+', default=list(), metavar='PKG',
                                help='name of Python packages to update')

    pip_genl_group = pip_parser.add_argument_group(title='general arguments')
    pip_genl_group.add_argument('-a', '--all', action='store_true',
                                help='update all Python packages installed through Python Package Index')
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
                                help="options for `{}pip list --outdated{}' command".format(bold, reset))
    pip_misc_group.add_argument('-U', '- update', action='store', default=str(), metavar='ARG',
                                help="options for `{}pip install --upgrade <package>{}' command".format(bold, reset))

    return pip_parser


def get_brew_parser():
    #######################################################
    # Brew Update CLI
    #   * options
    #       - optional arguments
    #       - specification arguments
    #       - general arguments
    #       - miscellaneous arguments
    #   * packages
    #######################################################

    brew_parser = argparse.ArgumentParser(prog='macdaily update brew',
                                          description='Homebrew Formula Update Automator',
                                          usage='macdaily update brew [options] <formulae>')
    brew_parser.add_argument('-V', '--version', action='version', version=__version__)
    brew_parser.add_argument('more_opts', nargs=argparse.REMAINDER, help=argparse.SUPPRESS)

    brew_spec_group = brew_parser.add_argument_group(title='specification arguments')
    brew_spec_group.add_argument('-f', '--force', action='store_true',
                                 help='always do a slower, full update check even if unnecessary')
    brew_spec_group.add_argument('-m', '--merge', action='store_true',
                                 help=("`{}git merge{}' is used to include updates "
                                       "(rather than `{}git rebase{}')".format(bold, reset, bold, reset)))
    brew_spec_group.add_argument('-p', '--packages', action='append', nargs='+', default=list(), metavar='FORM',
                                 help='name of Homebrew formulae to update')

    brew_genl_group = brew_parser.add_argument_group(title='general arguments')
    brew_genl_group.add_argument('-a', '--all', action='store_true',
                                 help='update all Homebrew formulae installed through Homebrew')
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
                                 help="options for `{}brew outdated{}' command".format(bold, reset))
    brew_misc_group.add_argument('-U', '- update', action='store', default=str(), metavar='ARG',
                                 help="options for `{}brew upgrade <formula>{}' command".format(bold, reset))

    return brew_parser


def get_cask_parser():
    #######################################################
    # Cask Update CLI
    #   * options
    #       - optional arguments
    #       - specification arguments
    #       - general arguments
    #       - miscellaneous arguments
    #   * packages
    #######################################################

    cask_parser = argparse.ArgumentParser(prog='macdaily update cask',
                                          description='Homebrew Cask Update Automator',
                                          usage='macdaily update cask [options] <casks>')
    cask_parser.add_argument('-V', '--version', action='version', version=__version__)
    cask_parser.add_argument('more_opts', nargs=argparse.REMAINDER, help=argparse.SUPPRESS)

    cask_spec_group = cask_parser.add_argument_group(title='specification arguments')
    cask_spec_group.add_argument('-f', '--force', action='store_true',
                                 help=("use `{}--force{}' when running "
                                       "`{}brew cask upgrade <cask>{}' command".format(bold, reset, bold, reset)))
    cask_spec_group.add_argument('-g', '--greedy', action='store_true',
                                 help=("use `{}--greedy{}' when running "
                                       "`{}brew cask upgrade <cask>{}' command".format(bold, reset, bold, reset)))
    cask_spec_group.add_argument('-m', '--merge', action='store_true',
                                 help=("`{}git merge{}' is used to include updates "
                                       "(rather than `{}git rebase{}')".format(bold, reset, bold, reset)))
    cask_spec_group.add_argument('-x', '--exhaust', action='store_true',
                                 help='exhaustively check Caskroom for outdated Homebrew Casks')
    cask_spec_group.add_argument('-p', '--packages', action='append', nargs='+', default=list(), metavar='CASK',
                                 help='name of Caskroom binaries to update')

    cask_genl_group = cask_parser.add_argument_group(title='general arguments')
    cask_genl_group.add_argument('-a', '--all', action='store_true',
                                 help='update all Caskroom binaries installed through Homebrew')
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
                                 help="options for `{}brew cask outdated{}' command".format(bold, reset))
    cask_misc_group.add_argument('-U', '- update', action='store', default=str(), metavar='ARG',
                                 help="options for `{}brew cask upgrade <cask>{}' command".format(bold, reset))

    return cask_parser


def get_system_parser():
    #######################################################
    # System Update CLI
    #   * options
    #       - optional arguments
    #       - specification arguments
    #       - general arguments
    #       - miscellaneous arguments
    #   * packages
    #######################################################

    system_parser = argparse.ArgumentParser(prog='macdaily update system',
                                            description='System Software Update Automator',
                                            usage='macdaily update system [options] <software>')
    system_parser.add_argument('-V', '--version', action='version', version=__version__)
    system_parser.add_argument('more_opts', nargs=argparse.REMAINDER, help=argparse.SUPPRESS)

    system_spec_group = system_parser.add_argument_group(title='specification arguments')
    system_spec_group.add_argument('-R', '--restart', action='store_true',
                                   help='automatically restart (or shut down) if required to complete installation')
    system_spec_group.add_argument('-r', '--recommended', action='store_true',
                                   help='only update software that is recommended for your system')
    system_spec_group.add_argument('-p', '--packages', action='append', nargs='+', default=list(), metavar='SW',
                                   help='name of system software to update')

    system_genl_group = system_parser.add_argument_group(title='general arguments')
    system_genl_group.add_argument('-a', '--all', action='store_true',
                                   help="update all system software installed through `{}softwareupdate{}'".format(bold, reset))
    system_genl_group.add_argument('-q', '--quiet', action='store_true',
                                   help='run in quiet mode, with no output information')
    system_genl_group.add_argument('-v', '--verbose', action='store_true',
                                   help='run in verbose mode, with detailed output information')
    system_genl_group.add_argument('-y', '--yes', action='store_true',
                                   help='yes for all selections')

    system_misc_group = system_parser.add_argument_group(title='miscellaneous arguments')
    system_misc_group.add_argument('-L', '--logging', action='store', default=str(), metavar='ARG',
                                   help="options for `{}softwareupdate --list{}' command".format(bold, reset))
    system_misc_group.add_argument('-U', '- update', action='store', default=str(), metavar='ARG',
                                   help="options for `{}softwareupdate --install <software>{}' command".format(bold, reset))

    return system_parser


def parse_args(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    # main parser process
    main_parser = get_update_parser()
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
