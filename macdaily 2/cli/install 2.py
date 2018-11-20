# -*- coding: utf-8 -*-

import argparse
import sys

from macdaily.util.const import __version__, bold, reset


def get_install_parser():
    #######################################################
    # Install CLI
    #   * options
    #       - optional arguments
    #       - general arguments
    #       - package arguments
    #       - control arguments
    #   * specifications
    #######################################################

    parser = argparse.ArgumentParser(prog='macdaily-install',
                                     description='macOS Package Automate Installer',
                                     usage='macdaily install [options] <mode-selection> ...',
                                     epilog='aliases: i')
    parser.add_argument('-V', '--version', action='version', version=__version__)
    parser.add_argument('more_opts', nargs=argparse.REMAINDER, help=argparse.SUPPRESS)

    genl_group = parser.add_argument_group(title='general arguments')
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
                            help='name of Atom plug-ins to install')
    pkgs_group.add_argument('--gem', action='append', nargs='+', default=list(), metavar='GEM', dest='gem_pkgs',
                            help='name of Ruby gems to install')
    pkgs_group.add_argument('--mas', action='append', nargs='+', default=list(), metavar='APP', dest='mas_pkgs',
                            help='name of macOS applications to install')
    pkgs_group.add_argument('--npm', action='append', nargs='+', default=list(), metavar='MOD', dest='npm_pkgs',
                            help='name of Node.js modules to install')
    pkgs_group.add_argument('--pip', action='append', nargs='+', default=list(), metavar='PKG', dest='pip_pkgs',
                            help='name of Python packages to install')
    pkgs_group.add_argument('--brew', action='append', nargs='+', default=list(), metavar='FORM', dest='brew_pkgs',
                            help='name of Homebrew formulae to install')
    pkgs_group.add_argument('--cask', action='append', nargs='+', default=list(), metavar='CASK', dest='cask_pkgs',
                            help='name of Caskroom binaries to install')
    pkgs_group.add_argument('--system', action='append', nargs='+', default=list(), metavar='SW', dest='system_pkgs',
                            help='name of system software to install')

    parser.add_argument_group(title='mode selection',
                              description=('install packages through a specified method, '
                                           'e.g.: apm, gem, mas, npm, pip, brew, cask, system'))

    return parser


def get_apm_parser():
    #######################################################
    # Apm Install CLI
    #   * options
    #       - optional arguments
    #       - specification arguments
    #       - general arguments
    #       - miscellaneous arguments
    #   * packages
    #######################################################

    apm_parser = argparse.ArgumentParser(prog='macdaily-install-apm',
                                         description='Atom Plug-In Automate Installer',
                                         usage='macdaily install apm [options] <plug-ins>')
    apm_parser.add_argument('-V', '--version', action='version', version=__version__)
    apm_parser.add_argument('more_opts', nargs=argparse.REMAINDER, help=argparse.SUPPRESS)

    apm_spec_group = apm_parser.add_argument_group(title='specification arguments')
    apm_spec_group.add_argument('-b', '--beta', action='store_true',
                                help='install Atom Beta plug-ins')
    apm_spec_group.add_argument('-p', '--packages', action='append', nargs='+', default=list(), metavar='PI',
                                help='name of Atom plug-ins to install')

    apm_genl_group = apm_parser.add_argument_group(title='general arguments')
    apm_genl_group.add_argument('-q', '--quiet', action='store_true',
                                help='run in quiet mode, with no output information')
    apm_genl_group.add_argument('-v', '--verbose', action='store_true',
                                help='run in verbose mode, with detailed output information')
    apm_genl_group.add_argument('-y', '--yes', action='store_true',
                                help='yes for all selections')

    apm_misc_group = apm_parser.add_argument_group(title='miscellaneous arguments')
    apm_misc_group.add_argument('-I', '--install', action='store', default=str(), metavar='ARG',
                                help="options for `{}apm install <plug-in>{}' command".format(bold, reset))

    return apm_parser


def get_gem_parser():
    #######################################################
    # Gem Install CLI
    #   * options
    #       - optional arguments
    #       - specification arguments
    #       - general arguments
    #       - miscellaneous arguments
    #   * packages
    #######################################################

    gem_parser = argparse.ArgumentParser(prog='macdaily-install-gem',
                                         description='Ruby Gem Automate Installer',
                                         usage='macdaily install gem [options] <gems>')
    gem_parser.add_argument('-V', '--version', action='version', version=__version__)
    gem_parser.add_argument('more_opts', nargs=argparse.REMAINDER, help=argparse.SUPPRESS)

    gem_spec_group = gem_parser.add_argument_group(title='specification arguments')
    gem_spec_group.add_argument('-b', '--brew', action='store_true',
                                help='install gems by Ruby installed from Homebrew')
    gem_spec_group.add_argument('-s', '--system', action='store_true',
                                help='install gems by Ruby provided by macOS system')
    gem_spec_group.add_argument('-p', '--packages', action='append', nargs='+', default=list(), metavar='GEM',
                                help='name of Ruby gems to install')

    gem_genl_group = gem_parser.add_argument_group(title='general arguments')
    gem_genl_group.add_argument('-q', '--quiet', action='store_true',
                                help='run in quiet mode, with no output information')
    gem_genl_group.add_argument('-v', '--verbose', action='store_true',
                                help='run in verbose mode, with detailed output information')
    gem_genl_group.add_argument('-y', '--yes', action='store_true',
                                help='yes for all selections')

    gem_misc_group = gem_parser.add_argument_group(title='miscellaneous arguments')
    gem_misc_group.add_argument('-I', '--install', action='store', default=str(), metavar='ARG',
                                help="options for `{}gem install <gem>{}' command".format(bold, reset))

    return gem_parser


def get_mas_parser():
    #######################################################
    # Mas Install CLI
    #   * options
    #       - optional arguments
    #       - general arguments
    #       - miscellaneous arguments
    #   * packages
    #######################################################

    mas_parser = argparse.ArgumentParser(prog='macdaily-install-mas',
                                         description='macOS Application Automate Installer',
                                         usage='macdaily install mas [options] <applications>')
    mas_parser.add_argument('-V', '--version', action='version', version=__version__)
    mas_parser.add_argument('more_opts', nargs=argparse.REMAINDER, help=argparse.SUPPRESS)

    mas_spec_group = mas_parser.add_argument_group(title='specification arguments')
    mas_spec_group.add_argument('-f', '--force', action='store_true',
                                help='force reinstall')
    mas_spec_group.add_argument('-p', '--packages', action='append', nargs='+', default=list(), metavar='APP',
                                help='name of macOS applications to install')

    mas_genl_group = mas_parser.add_argument_group(title='general arguments')
    mas_genl_group.add_argument('-q', '--quiet', action='store_true',
                                help='run in quiet mode, with no output information')
    mas_genl_group.add_argument('-v', '--verbose', action='store_true',
                                help='run in verbose mode, with detailed output information')
    mas_genl_group.add_argument('-y', '--yes', action='store_true',
                                help='yes for all selections')

    mas_misc_group = mas_parser.add_argument_group(title='miscellaneous arguments')
    mas_misc_group.add_argument('-I', '--install', action='store', default=str(), metavar='ARG',
                                help="options for `{}mas install|lucky <application>' command{}".format(bold, reset))

    return mas_parser


def get_npm_parser():
    #######################################################
    # Npm Install CLI
    #   * options
    #       - optional arguments
    #       - general arguments
    #       - miscellaneous arguments
    #   * packages
    #######################################################

    npm_parser = argparse.ArgumentParser(prog='macdaily-install-npm',
                                         description='Node.js Module Automate Installer',
                                         usage='macdaily install npm [options] <modules>')
    npm_parser.add_argument('-V', '--version', action='version', version=__version__)
    npm_parser.add_argument('more_opts', nargs=argparse.REMAINDER, help=argparse.SUPPRESS)

    npm_spec_group = npm_parser.add_argument_group(title='specification arguments')
    npm_spec_group.add_argument('-p', '--packages', action='append', nargs='+', default=list(), metavar='MOD',
                                help='name of Node.js modules to install')

    npm_genl_group = npm_parser.add_argument_group(title='general arguments')
    npm_genl_group.add_argument('-q', '--quiet', action='store_true',
                                help='run in quiet mode, with no output information')
    npm_genl_group.add_argument('-v', '--verbose', action='store_true',
                                help='run in verbose mode, with detailed output information')
    npm_genl_group.add_argument('-y', '--yes', action='store_true',
                                help='yes for all selections')
    npm_genl_group.add_argument('-n', '--no-cleanup', action='store_true',
                                help='do not run cleanup process')

    npm_misc_group = npm_parser.add_argument_group(title='miscellaneous arguments')
    npm_misc_group.add_argument('-I', '--install', action='store', default=str(), metavar='ARG',
                                help="options for `{}npm install --global <module>{}' command".format(bold, reset))

    return npm_parser


def get_pip_parser():
    #######################################################
    # Pip Install CLI
    #   * options
    #       - optional arguments
    #       - specification arguments
    #       - general arguments
    #       - miscellaneous arguments
    #   * packages
    #######################################################

    pip_parser = argparse.ArgumentParser(prog='macdaily-install-pip',
                                         description='Python Package Automate Installer',
                                         usage='macdaily install pip [options] <packages>')
    pip_parser.add_argument('-V', '--version', action='version', version=__version__)
    pip_parser.add_argument('more_opts', nargs=argparse.REMAINDER, help=argparse.SUPPRESS)

    pip_spec_group = pip_parser.add_argument_group(title='specification arguments')
    pip_spec_group.add_argument('-u', '--user', action='store_true',
                                help='install to the Python user install directory for your platform')
    pip_spec_group.add_argument('-b', '--brew', action='store_true',
                                help='install packages of Python installed from Homebrew')
    pip_spec_group.add_argument('-c', '--cpython', action='store_true',
                                help='install packages of CPython implementation')
    pip_spec_group.add_argument('-d', '--pre', action='store_true',
                                help='include pre-release and development versions')
    pip_spec_group.add_argument('-e', '--python', action='append', nargs='+',
                                default=list(), metavar='VER', dest='version',
                                help='install packages by which version of Python')
    pip_spec_group.add_argument('-r', '--pypy', action='store_true',
                                help='install packages of PyPy implementation')
    pip_spec_group.add_argument('-s', '--system', action='store_true',
                                help='install packages of Python provided by macOS system')
    pip_spec_group.add_argument('-p', '--packages', action='append', nargs='+', default=list(), metavar='PKG',
                                help='name of Python packages to install')

    pip_genl_group = pip_parser.add_argument_group(title='general arguments')
    pip_genl_group.add_argument('-q', '--quiet', action='store_true',
                                help='run in quiet mode, with no output information')
    pip_genl_group.add_argument('-v', '--verbose', action='store_true',
                                help='run in verbose mode, with detailed output information')
    pip_genl_group.add_argument('-y', '--yes', action='store_true',
                                help='yes for all selections')
    pip_genl_group.add_argument('-n', '--no-cleanup', action='store_true',
                                help='do not run cleanup process')

    pip_misc_group = pip_parser.add_argument_group(title='miscellaneous arguments')
    pip_misc_group.add_argument('-I', '--install', action='store', default=str(), metavar='ARG',
                                help="options for `{}pip install <package>{}' command".format(bold, reset))

    return pip_parser


def get_brew_parser():
    #######################################################
    # Brew Install CLI
    #   * options
    #       - optional arguments
    #       - specification arguments
    #       - general arguments
    #       - miscellaneous arguments
    #   * packages
    #######################################################

    brew_parser = argparse.ArgumentParser(prog='macdaily-install-brew',
                                          description='Homebrew Formula Automate Installer',
                                          usage='macdaily install brew [options] <formulae>')
    brew_parser.add_argument('-V', '--version', action='version', version=__version__)
    brew_parser.add_argument('more_opts', nargs=argparse.REMAINDER, help=argparse.SUPPRESS)

    brew_spec_group = brew_parser.add_argument_group(title='specification arguments')
    brew_spec_group.add_argument('-p', '--packages', action='append', nargs='+', default=list(), metavar='FORM',
                                 help='name of Homebrew formulae to install')

    brew_genl_group = brew_parser.add_argument_group(title='general arguments')
    brew_genl_group.add_argument('-q', '--quiet', action='store_true',
                                 help='run in quiet mode, with no output information')
    brew_genl_group.add_argument('-v', '--verbose', action='store_true',
                                 help='run in verbose mode, with detailed output information')
    brew_genl_group.add_argument('-y', '--yes', action='store_true',
                                 help='yes for all selections')
    brew_genl_group.add_argument('-n', '--no-cleanup', action='store_true',
                                 help='do not run cleanup process')

    brew_misc_group = brew_parser.add_argument_group(title='miscellaneous arguments')
    brew_misc_group.add_argument('-I', '--install', action='store', default=str(), metavar='ARG',
                                 help="options for `{}brew install <formula>{}' command".format(bold, reset))

    return brew_parser


def get_cask_parser():
    #######################################################
    # Cask Install CLI
    #   * options
    #       - optional arguments
    #       - specification arguments
    #       - general arguments
    #       - miscellaneous arguments
    #   * packages
    #######################################################

    cask_parser = argparse.ArgumentParser(prog='macdaily-install-cask',
                                          description='Homebrew Cask Automate Installer',
                                          usage='macdaily install cask [options] <casks>')
    cask_parser.add_argument('-V', '--version', action='version', version=__version__)
    cask_parser.add_argument('more_opts', nargs=argparse.REMAINDER, help=argparse.SUPPRESS)

    cask_spec_group = cask_parser.add_argument_group(title='specification arguments')
    cask_spec_group.add_argument('-p', '--packages', action='append', nargs='+', default=list(), metavar='CASK',
                                 help='name of Caskroom binaries to install')

    cask_genl_group = cask_parser.add_argument_group(title='general arguments')
    cask_genl_group.add_argument('-q', '--quiet', action='store_true',
                                 help='run in quiet mode, with no output information')
    cask_genl_group.add_argument('-v', '--verbose', action='store_true',
                                 help='run in verbose mode, with detailed output information')
    cask_genl_group.add_argument('-y', '--yes', action='store_true',
                                 help='yes for all selections')
    cask_genl_group.add_argument('-n', '--no-cleanup', action='store_true',
                                 help='do not run cleanup process')

    cask_misc_group = cask_parser.add_argument_group(title='miscellaneous arguments')
    cask_misc_group.add_argument('-I', '--install', action='store', default=str(), metavar='ARG',
                                 help="options for `{}brew cask install <cask>{}' command".format(bold, reset))

    return cask_parser


def get_system_parser():
    #######################################################
    # System Install CLI
    #   * options
    #       - optional arguments
    #       - specification arguments
    #       - general arguments
    #       - miscellaneous arguments
    #   * packages
    #######################################################

    system_parser = argparse.ArgumentParser(prog='macdaily-install-system',
                                            description='System Software Automate Installer',
                                            usage='macdaily install system [options] <software>')
    system_parser.add_argument('-V', '--version', action='version', version=__version__)
    system_parser.add_argument('more_opts', nargs=argparse.REMAINDER, help=argparse.SUPPRESS)

    system_spec_group = system_parser.add_argument_group(title='specification arguments')
    system_spec_group.add_argument('-R', '--restart', action='store_true',
                                   help='automatically restart (or shut down) if required to complete installation')
    system_spec_group.add_argument('-p', '--packages', action='append', nargs='+', default=list(), metavar='SW',
                                   help='name of system software to install')

    system_genl_group = system_parser.add_argument_group(title='general arguments')
    system_genl_group.add_argument('-q', '--quiet', action='store_true',
                                   help='run in quiet mode, with no output information')
    system_genl_group.add_argument('-v', '--verbose', action='store_true',
                                   help='run in verbose mode, with detailed output information')
    system_genl_group.add_argument('-y', '--yes', action='store_true',
                                   help='yes for all selections')

    system_misc_group = system_parser.add_argument_group(title='miscellaneous arguments')
    system_misc_group.add_argument('-I', '--install', action='store', default=str(), metavar='ARG',
                                   help="options for `{}softwareupdate --install <software>{}' command".format(bold, reset))

    return system_parser


def parse_args(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    # main parser process
    main_parser = get_install_parser()
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
