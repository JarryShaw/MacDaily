# -*- coding: utf-8 -*-

import argparse

from macdaily.util.colour import bold, reset
from macdaily.util.const import __version__


def get_parser():
    """Return ArgumentParser for update command."""
    #######################################################
    # Update CLI
    #   * options
    #       - optional arguments
    #       - general arguments
    #       - package arguments
    #       - control arguments
    #   * specifications
    #######################################################

    parser = argparse.ArgumentParser(prog='update',
                                     description='macOS Package Update Automator',
                                     usage='macdaily update [options] <mode-selection> ...',
                                     epilog='aliases: up, upgrade')
    parser.add_argument('-V', '--version', action='version', version=__version__)
    parser.add_argument('unknown_opts', nargs=argparse.REMAINDER, help=argparse.SUPPRESS)

    genl_group = parser.add_argument_group(title='general arguments')
    genl_group.add_argument('-a', '--all', action='store_true', default=False,
                            help=('update all packages installed through Atom, RubyGem, Node.js, '
                                  'Homebrew, Caskroom, Mac App Store, and etc'))
    genl_group.add_argument('-q', '--quiet', action='store_true', default=False,
                            help='run in quiet mode, with no output information')
    genl_group.add_argument('-v', '--verbose', action='store_true', default=False,
                            help='run in verbose mode, with detailed output information')
    genl_group.add_argument('-l', '--show-log', action='store_true',
                            help='open log in Console.app upon completion of command')
    genl_group.add_argument('-y', '--yes', action='store_true',
                            help='yes for all selections')
    genl_group.add_argument('-n', '--no-cleanup', action='store_true',
                            help='do not run cleanup process')

    pkgs_group = parser.add_argument_group(title='package arguments',
                                           description='options used to specify packages of each mode')
    pkgs_group.add_argument('--apm', action='append', metavar='PI', dest='apm_pkgs',
                            help='name of Atom plug-ins to update')
    pkgs_group.add_argument('--gem', action='append', metavar='GEM', dest='gem_pkgs',
                            help='name of Ruby gems to update')
    pkgs_group.add_argument('--mas', action='append', metavar='APP', dest='mas_pkgs',
                            help='name of macOS applications to update')
    pkgs_group.add_argument('--npm', action='append', metavar='MOD', dest='npm_pkgs',
                            help='name of Node.js modules to update')
    pkgs_group.add_argument('--pip', action='append', metavar='PKG', dest='pip_pkgs',
                            help='name of Python packages to update')
    pkgs_group.add_argument('--brew', action='append', metavar='FORM', dest='brew_pkgs',
                            help='name of Homebrew formulae to update')
    pkgs_group.add_argument('--cask', action='append', metavar='CASK', dest='cask_pkgs',
                            help='name of Caskroom binaries to update')
    pkgs_group.add_argument('--system', action='append', metavar='SW', dest='system_pkgs',
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

    subparser = parser.add_subparsers(title='mode selection', metavar='MODE', dest='mode',
                                      help=('update outdated packages installed through a specified method, '
                                            'e.g.: apm, gem, mas, npm, pip, brew, cask, system'))

    #######################################################
    # Apm Update CLI
    #   * options
    #       - optional arguments
    #       - specification arguments
    #       - general arguments
    #       - miscellaneous arguments
    #   * packages
    #######################################################

    parser_apm = subparser.add_parser('apm', description='Atom Plug-In Update Automator',
                                      usage='macdaily update apm [options] <plug-ins>')
    parser_apm.add_argument('-V', '--version', action='version', version=__version__)
    parser_apm.add_argument('-p', '--package', metavar='PI', action='append', dest='apm_pkgs', nargs='+',
                            help='name of Atom plug-ins to update')
    parser_apm.add_argument('apm_pkgs', action='append', nargs='*', metavar='plug-in',
                            help='name of Atom plug-ins to update')

    apm_spec_group = parser_apm.add_argument_group(title='specification arguments')
    apm_spec_group.add_argument('-b', '--beta', action='store_true',
                                help='update Atom Beta plug-ins')

    apm_genl_group = parser_apm.add_argument_group(title='general arguments')
    apm_genl_group.add_argument('-a', '--all', action='store_true',
                                help='update all plug-ins installed through Atom Package Manager')
    apm_genl_group.add_argument('-q', '--quiet', action='store_true',
                                help='run in quiet mode, with no output information')
    apm_genl_group.add_argument('-v', '--verbose', action='store_true',
                                help='run in verbose mode, with detailed output information')
    apm_genl_group.add_argument('-l', '--show-log', action='store_true',
                                help='open log in Console.app upon completion of command')
    apm_genl_group.add_argument('-y', '--yes', action='store_true',
                                help='yes for all selections')

    apm_misc_group = parser_apm.add_argument_group(title='miscellaneous arguments')
    apm_misc_group.add_argument('-L', '--logging', action='store', dest='logging_opts', metavar='ARG',
                                help=f"options for `{bold}apm upgrade --list{reset}' command")
    apm_misc_group.add_argument('-U', '--update', action='store', dest='update_opts', metavar='ARG',
                                help=f"options for `{bold}apm upgrade <plug-in>{reset}' command")

    #######################################################
    # Gem Update CLI
    #   * options
    #       - optional arguments
    #       - specification arguments
    #       - general arguments
    #       - miscellaneous arguments
    #   * packages
    #######################################################

    parser_gem = subparser.add_parser('gem', description='Ruby Gem Update Automator',
                                      usage='macdaily update gem [options] <gems>')
    parser_gem.add_argument('-V', '--version', action='version', version=__version__)
    parser_gem.add_argument('-p', '--package', metavar='GEM', action='append', dest='gem_pkgs', nargs='+',
                            help='name of Ruby gems to update')
    parser_gem.add_argument('gem_pkgs', action='append', nargs='*', metavar='gem',
                            help='name of Ruby gems to update')

    gem_spec_group = parser_gem.add_argument_group(title='specification arguments')
    gem_spec_group.add_argument('-b', '--brew', action='store_true',
                                help='update gems of Ruby installed from Homebrew')
    gem_spec_group.add_argument('-s', '--system', action='store_true',
                                help='update gems of Ruby provided by macOS system')

    gem_genl_group = parser_gem.add_argument_group(title='general arguments')
    gem_genl_group.add_argument('-a', '--all', action='store_true',
                                help='update all gems installed through RubyGems')
    gem_genl_group.add_argument('-q', '--quiet', action='store_true',
                                help='run in quiet mode, with no output information')
    gem_genl_group.add_argument('-v', '--verbose', action='store_true',
                                help='run in verbose mode, with detailed output information')
    gem_genl_group.add_argument('-l', '--show-log', action='store_true',
                                help='open log in Console.app upon completion of command')
    gem_genl_group.add_argument('-y', '--yes', action='store_true',
                                help='yes for all selections')

    gem_misc_group = parser_gem.add_argument_group(title='miscellaneous arguments')
    gem_misc_group.add_argument('-L', '--logging', action='store', dest='logging_opts', metavar='ARG',
                                help=f"options for `{bold}gem outdated{reset}' command")
    gem_misc_group.add_argument('-U', '--update', action='store', dest='update_opts', metavar='ARG',
                                help=f"options for `{bold}gem update <gem>{reset}' command")

    #######################################################
    # Mas Update CLI
    #   * options
    #       - optional arguments
    #       - general arguments
    #       - miscellaneous arguments
    #   * packages
    #######################################################

    parser_mas = subparser.add_parser('mas', description='macOS Application Update Automator',
                                      usage='macdaily update mas [options] <applications>')
    parser_mas.add_argument('-V', '--version', action='version', version=__version__)
    parser_mas.add_argument('-p', '--package', metavar='APP', action='append', dest='mas_pkgs', nargs='+',
                            help='name of macOS applications to update')
    parser_mas.add_argument('mas_pkgs', action='append', nargs='*', metavar='application',
                            help='name of macOS applications to update')

    mas_genl_group = parser_mas.add_argument_group(title='general arguments')
    mas_genl_group.add_argument('-a', '--all', action='store_true',
                                help='update all macOS applications installed through Mac App Store')
    mas_genl_group.add_argument('-q', '--quiet', action='store_true',
                                help='run in quiet mode, with no output information')
    mas_genl_group.add_argument('-v', '--verbose', action='store_true',
                                help='run in verbose mode, with detailed output information')
    mas_genl_group.add_argument('-l', '--show-log', action='store_true',
                                help='open log in Console.app upon completion of command')
    mas_genl_group.add_argument('-y', '--yes', action='store_true',
                                help='yes for all selections')

    mas_misc_group = parser_mas.add_argument_group(title='miscellaneous arguments')
    mas_misc_group.add_argument('-L', '--logging', action='store', dest='logging_opts', metavar='ARG',
                                help=f"options for `{bold}mas outdated' command{reset}")
    mas_misc_group.add_argument('-U', '--update', action='store', dest='update_opts', metavar='ARG',
                                help=f"options for `{bold}mas upgrade <application>{reset}' command")

    #######################################################
    # Npm Update CLI
    #   * options
    #       - optional arguments
    #       - general arguments
    #       - miscellaneous arguments
    #   * packages
    #######################################################

    parser_npm = subparser.add_parser('npm', description='Node.js Module Update Automator',
                                      usage='macdaily update npm [options] <modules>')
    parser_npm.add_argument('-V', '--version', action='version', version=__version__)
    parser_npm.add_argument('-p', '--package', metavar='MOD', action='append', dest='npm_pkgs', nargs='+',
                            help='name of Node.js modules to update')
    parser_npm.add_argument('npm_pkgs', action='append', nargs='*', metavar='module',
                            help='name of Node.js modules to update')

    npm_genl_group = parser_npm.add_argument_group(title='general arguments')
    npm_genl_group.add_argument('-a', '--all', action='store_true',
                                help='update all Node.js modules installed through Node.js Package Manager')
    npm_genl_group.add_argument('-q', '--quiet', action='store_true',
                                help='run in quiet mode, with no output information')
    npm_genl_group.add_argument('-v', '--verbose', action='store_true',
                                help='run in verbose mode, with detailed output information')
    npm_genl_group.add_argument('-l', '--show-log', action='store_true',
                                help='open log in Console.app upon completion of command')
    npm_genl_group.add_argument('-y', '--yes', action='store_true',
                                help='yes for all selections')
    npm_genl_group.add_argument('-n', '--no-cleanup', action='store_true',
                                help='do not run cleanup process')

    npm_misc_group = parser_npm.add_argument_group(title='miscellaneous arguments')
    npm_misc_group.add_argument('-L', '--logging', action='store', dest='logging_opts', metavar='ARG',
                                help=f"options for `{bold}npm outdated --global{reset}' command")
    npm_misc_group.add_argument('-U', '--update', action='store', dest='update_opts', metavar='ARG',
                                help=f"options for `{bold}npm upgrade --global <module>{reset}' command")

    #######################################################
    # Pip Update CLI
    #   * options
    #       - optional arguments
    #       - specification arguments
    #       - general arguments
    #       - miscellaneous arguments
    #   * packages
    #######################################################

    parser_pip = subparser.add_parser('pip', description='Python Package Update Automator',
                                      usage='macdaily update pip [options] <packages>')
    parser_pip.add_argument('-V', '--version', action='version', version=__version__)
    parser_pip.add_argument('-p', '--package', metavar='PKG', action='append', dest='pip_pkgs', nargs='+',
                            help='name of Python packages to update')
    parser_pip.add_argument('pip_pkgs', action='append', nargs='*', metavar='package',
                            help='name of Python packages to update')

    pip_spec_group = parser_pip.add_argument_group(title='specification arguments')
    pip_spec_group.add_argument('-b', '--brew', action='store_true',
                                help='update packages of Python installed from Homebrew')
    pip_spec_group.add_argument('-c', '--cpython', action='store_true',
                                help='update packages of CPython implementation')
    pip_spec_group.add_argument('-d', '--pre', action='store_true',
                                help='include pre-release and development versions')
    pip_spec_group.add_argument('-e', '--python', action='store', metavar='VER', dest='version',
                                help='indicate packages from which version of Python will update')
    pip_spec_group.add_argument('-r', '--pypy', action='store_true',
                                help='update packages of PyPy implementation')
    pip_spec_group.add_argument('-s', '--system', action='store_true',
                                help='update packages of Python provided by macOS system')

    pip_genl_group = parser_pip.add_argument_group(title='general arguments')
    pip_genl_group.add_argument('-a', '--all', action='store_true',
                                help='update all Python packages installed through Python Package Index')
    pip_genl_group.add_argument('-q', '--quiet', action='store_true',
                                help='run in quiet mode, with no output information')
    pip_genl_group.add_argument('-v', '--verbose', action='store_true',
                                help='run in verbose mode, with detailed output information')
    pip_genl_group.add_argument('-l', '--show-log', action='store_true',
                                help='open log in Console.app upon completion of command')
    pip_genl_group.add_argument('-y', '--yes', action='store_true',
                                help='yes for all selections')
    pip_genl_group.add_argument('-n', '--no-cleanup', action='store_true',
                                help='do not run cleanup process')

    pip_misc_group = parser_pip.add_argument_group(title='miscellaneous arguments')
    pip_misc_group.add_argument('-L', '--logging', action='store', dest='logging_opts', metavar='ARG',
                                help=f"options for `{bold}pip list --outdated{reset}' command")
    pip_misc_group.add_argument('-U', '--update', action='store', dest='update_opts', metavar='ARG',
                                help=f"options for `{bold}pip install --upgrade <package>{reset}' command")

    #######################################################
    # Brew Update CLI
    #   * options
    #       - optional arguments
    #       - specification arguments
    #       - general arguments
    #       - miscellaneous arguments
    #   * packages
    #######################################################

    parser_brew = subparser.add_parser('brew', description='Homebrew Formula Update Automator',
                                       usage='macdaily update brew [options] <formulae>')
    parser_brew.add_argument('-V', '--version', action='version', version=__version__)
    parser_brew.add_argument('-p', '--package', metavar='FORM', action='append', dest='brew_pkgs', nargs='+',
                             help='name of Homebrew formulae to update')
    parser_brew.add_argument('brew_pkgs', action='append', nargs='*',
                             help='name of Homebrew formulae to update')

    brew_spec_group = parser_brew.add_argument_group(title='specification arguments')
    brew_spec_group.add_argument('-f', '--force', action='store_true',
                                 help='always do a slower, full update check even if unnecessary')
    brew_spec_group.add_argument('-m', '--merge', action='store_true',
                                 help=(f"`{bold}git merge{reset}' is used to include updates "
                                       f"(rather than `{bold}git rebase{reset}')"))

    brew_genl_group = parser_brew.add_argument_group(title='general arguments')
    brew_genl_group.add_argument('-a', '--all', action='store_true',
                                 help='update all Homebrew formulae installed through Homebrew')
    brew_genl_group.add_argument('-q', '--quiet', action='store_true',
                                 help='run in quiet mode, with no output information')
    brew_genl_group.add_argument('-v', '--verbose', action='store_true',
                                 help='run in verbose mode, with detailed output information')
    brew_genl_group.add_argument('-l', '--show-log', action='store_true',
                                 help='open log in Console.app upon completion of command')
    brew_genl_group.add_argument('-y', '--yes', action='store_true',
                                 help='yes for all selections')
    brew_genl_group.add_argument('-n', '--no-cleanup', action='store_true',
                                 help='do not run cleanup process')

    brew_misc_group = parser_brew.add_argument_group(title='miscellaneous arguments')
    brew_misc_group.add_argument('-L', '--logging', action='store', dest='logging_opts', metavar='ARG',
                                 help=f"options for `{bold}brew outdated{reset}' command")
    brew_misc_group.add_argument('-U', '--update', action='store', dest='update_opts', metavar='ARG',
                                 help=f"options for `{bold}brew upgrade <formula>{reset}' command")

    #######################################################
    # Cask Update CLI
    #   * options
    #       - optional arguments
    #       - specification arguments
    #       - general arguments
    #       - miscellaneous arguments
    #   * packages
    #######################################################

    parser_cask = subparser.add_parser('cask', description='Homebrew Cask Update Packages',
                                       usage='macdaily update cask [options] <casks>')
    parser_cask.add_argument('-V', '--version', action='version', version=__version__)
    parser_cask.add_argument('-p', '--package', metavar='CASK', action='append', dest='cask_pkgs', nargs='+',
                             help='name of Caskroom binaries to update')
    parser_cask.add_argument('cask_pkgs', action='append', nargs='*',
                             help='name of Caskroom binaries to update')

    cask_spec_group = parser_cask.add_argument_group(title='specification arguments')
    cask_spec_group.add_argument('-f', '--force', action='store_true',
                                 help=(f"use `{bold}--force{reset}' when running "
                                       f"`{bold}brew cask upgrade <cask>{reset}' command"))
    cask_spec_group.add_argument('-g', '--greedy', action='store_true',
                                 help=(f"use `{bold}--greedy{reset}' when running "
                                       f"`{bold}brew cask upgrade <cask>{reset}' command"))
    cask_spec_group.add_argument('-m', '--merge', action='store_true',
                                 help=(f"`{bold}git merge{reset}' is used to include updates "
                                       f"(rather than `{bold}git rebase{reset}')"))
    cask_spec_group.add_argument('-x', '--exhaust', action='store_true',
                                 help='exhaustively check Caskroom for outdated Homebrew Casks')

    cask_genl_group = parser_cask.add_argument_group(title='general arguments')
    cask_genl_group.add_argument('-a', '--all', action='store_true',
                                 help='update all Caskroom binaries installed through Homebrew')
    cask_genl_group.add_argument('-q', '--quiet', action='store_true',
                                 help='run in quiet mode, with no output information')
    cask_genl_group.add_argument('-v', '--verbose', action='store_true',
                                 help='run in verbose mode, with detailed output information')
    cask_genl_group.add_argument('-l', '--show-log', action='store_true',
                                 help='open log in Console.app upon completion of command')
    cask_genl_group.add_argument('-y', '--yes', action='store_true',
                                 help='yes for all selections')
    cask_genl_group.add_argument('-n', '--no-cleanup', action='store_true',
                                 help='do not run cleanup process')

    cask_misc_group = parser_cask.add_argument_group(title='miscellaneous arguments')
    cask_misc_group.add_argument('-L', '--logging', action='store', dest='logging_opts', metavar='ARG',
                                 help=f"options for `{bold}brew cask outdated{reset}' command")
    cask_misc_group.add_argument('-U', '--update', action='store', dest='update_opts', metavar='ARG',
                                 help=f"options for `{bold}brew cask upgrade <cask>{reset}' command")

    #######################################################
    # System Update CLI
    #   * options
    #       - optional arguments
    #       - specification arguments
    #       - general arguments
    #       - miscellaneous arguments
    #   * packages
    #######################################################

    parser_system = subparser.add_parser('system', description='System Software Update Automator',
                                         usage='macdaily update system [options] <software>')
    parser_system.add_argument('-V', '--version', action='version', version=__version__)
    parser_system.add_argument('-p', '--package', metavar='SW', action='append', dest='system_pkgs', nargs='+',
                               help='name of system software to update')
    parser_system.add_argument('cask_pkgs', action='append', nargs='*',
                               help='name of system software to update')

    system_spec_group = parser_system.add_argument_group(title='specification arguments')
    system_spec_group.add_argument('-R', '--restart', action='store_true',
                                   help='automatically restart (or shut down) if required to complete installation')
    system_spec_group.add_argument('-r', '--recommended', action='store_true',
                                   help='only update software that is recommended for your system')

    system_genl_group = parser_system.add_argument_group(title='general arguments')
    system_genl_group.add_argument('-a', '--all', action='store_true',
                                   help=f"update all system software installed through `{bold}softwareupdate{reset}'")
    system_genl_group.add_argument('-q', '--quiet', action='store_true',
                                   help='run in quiet mode, with no output information')
    system_genl_group.add_argument('-l', '--show-log', action='store_true',
                                   help='open log in Console.app upon completion of command')
    system_genl_group.add_argument('-y', '--yes', action='store_true',
                                   help='yes for all selections')

    system_misc_group = parser_system.add_argument_group(title='miscellaneous arguments')
    system_misc_group.add_argument('-L', '--logging', action='store', dest='logging_opts', metavar='ARG',
                                   help=f"options for `{bold}softwareupdate --list{reset}' command")
    system_misc_group.add_argument('-U', '--update', action='store', dest='update_opts', metavar='ARG',
                                   help=f"options for `{bold}softwareupdate --install <software>{reset}' command")

    return parser
