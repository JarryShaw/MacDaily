# -*- coding: utf-8 -*-

import argparse

from macdaily.util.colour import bold, reset
from macdaily.util.const import __version__


def get_parser():
    parser = argparse.ArgumentParser(prog='update',
                                     description='macOS Package Update Automator',
                                     usage='macdaily update [options] [mode-options] <mode-selection> ...',
                                     epilog='aliases: up, upgrade')

    parser.add_argument('-a', '--all', action='store_true', default=False,
                        help=('update all packages installed through Atom, RubyGem, Node.js, '
                              'Homebrew, Caskroom, Mac App Store, and etc'))
    parser.add_argument('-q', '--quiet', action='store_true', default=False,
                        help='run in quiet mode, with no output information')
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help='run in verbose mode, with detailed output information')
    parser.add_argument('-l', '--show-log', action='store_true',
                        help='open log in Console.app upon completion of command')
    parser.add_argument('-Y', '--yes', action='store_true',
                        help='yes for all selections')
    parser.add_argument('-N', '--no-cleanup', action='store_true',
                        help='do not run cleanup process')
    parser.add_argument('-V', '--version', action='version', version=__version__)
    parser.add_argument('unknown_opts', nargs=argparse.REMAINDER, help=argparse.SUPPRESS)

    pkgs_group = parser.add_argument_group(title='mode packages options',
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

    swch_group = parser.add_argument_group(title='mode switches options',
                                           description='options used to disable update of certain mode')
    swch_group.add_argument('--no-apm', action='store_true', help='do not update Atom plug-ins')
    swch_group.add_argument('--no-gem', action='store_true', help='do not update Ruby gems')
    swch_group.add_argument('--no-mas', action='store_true', help='do not update macOS applications')
    swch_group.add_argument('--no-npm', action='store_true', help='do not update Node.js modules')
    swch_group.add_argument('--no-pip', action='store_true', help='do not update Python packages')
    swch_group.add_argument('--no-brew', action='store_true', help='do not update Homebrew formulae')
    swch_group.add_argument('--no-cask', action='store_true', help='do not update Caskroom binaries')
    swch_group.add_argument('--no-system', action='store_true', help='do not update system software')

    subparser = parser.add_subparsers(title='mode selection', metavar='MODE', dest='mode',
                                      help=('update outdated packages installed through a specified method, '
                                            'e.g.: apm, gem, mas, npm, pip, brew, cask, system'))

    parser_apm = subparser.add_parser('apm', description='Atom Plug-In Update Automator',
                                      usage='macdaily update apm [options] <plug-ins>')
    parser_apm.add_argument('-a', '--all', action='store_true',
                            help='update all plug-ins installed through Atom Package Manager')
    parser_apm.add_argument('-p', '--package', metavar='PI', action='append', dest='apm_pkgs',
                            help='name of Atom plug-ins to update')
    parser_apm.add_argument('-b', '--beta', action='store_true',
                            help='update Atom Beta plug-ins')
    parser_apm.add_argument('-q', '--quiet', action='store_true',
                            help='run in quiet mode, with no output information')
    parser_apm.add_argument('-v', '--verbose', action='store_true',
                            help='run in verbose mode, with detailed output information')
    parser_apm.add_argument('-l', '--show-log', action='store_true',
                            help='open log in Console.app upon completion of command')
    parser_apm.add_argument('-Y', '--yes', action='store_true',
                            help='yes for all selections')
    parser_apm.add_argument('-L', '--logging', action='store', dest='logging_opts', metavar='ARG',
                            help=f"options for `{bold}apm upgrade --list{reset}' command")
    parser_apm.add_argument('-U', '--update', action='store', dest='update_opts', metavar='ARG',
                            help=f"options for `{bold}apm upgrade <plug-in>{reset}' command")
    parser_apm.add_argument('-V', '--version', action='version', version=__version__)
    parser_apm.add_argument('apm_pkgs', action='append', nargs='*', help=argparse.SUPPRESS)

    parser_gem = subparser.add_parser('gem', description='Ruby Gem Update Automator',
                                      usage='macdaily update gem [options] <gems>')
    parser_gem.add_argument('-a', '--all', action='store_true',
                            help='update all gems installed through RubyGems')
    parser_gem.add_argument('-p', '--package', metavar='GEM', action='append', dest='gem_pkgs',
                            help='name of Ruby gems to update')
    parser_gem.add_argument('-b', '--brew', action='store_true',
                            help='update gems of Ruby installed from Homebrew')
    parser_gem.add_argument('-s', '--system', action='store_true',
                            help='update gems of Ruby provided by macOS system')
    parser_gem.add_argument('-q', '--quiet', action='store_true',
                            help='run in quiet mode, with no output information')
    parser_gem.add_argument('-v', '--verbose', action='store_true',
                            help='run in verbose mode, with detailed output information')
    parser_gem.add_argument('-l', '--show-log', action='store_true',
                            help='open log in Console.app upon completion of command')
    parser_gem.add_argument('-Y', '--yes', action='store_true',
                            help='yes for all selections')
    parser_gem.add_argument('-L', '--logging', action='store', dest='logging_opts', metavar='ARG',
                            help=f"options for `{bold}gem outdated{reset}' command")
    parser_gem.add_argument('-U', '--update', action='store', dest='update_opts', metavar='ARG',
                            help=f"options for `{bold}gem update <gem>{reset}' command")
    parser_gem.add_argument('-V', '--version', action='version', version=__version__)
    parser_gem.add_argument('gem_pkgs', action='append', nargs='*', help=argparse.SUPPRESS)

    parser_mas = subparser.add_parser('mas', description='macOS Application Update Automator',
                                      usage='macdaily update mas [options] <applications>')
    parser_mas.add_argument('-a', '--all', action='store_true',
                            help='update all macOS applications installed through Mac App Store')
    parser_mas.add_argument('-p', '--package', metavar='APP', action='append', dest='mas_pkgs',
                            help='name of macOS applications to update')
    parser_mas.add_argument('-q', '--quiet', action='store_true',
                            help='run in quiet mode, with no output information')
    parser_mas.add_argument('-v', '--verbose', action='store_true',
                            help='run in verbose mode, with detailed output information')
    parser_mas.add_argument('-l', '--show-log', action='store_true',
                            help='open log in Console.app upon completion of command')
    parser_mas.add_argument('-Y', '--yes', action='store_true',
                            help='yes for all selections')
    parser_mas.add_argument('-L', '--logging', action='store', dest='logging_opts', metavar='ARG',
                            help=f"options for `{bold}mas outdated' command{reset}")
    parser_mas.add_argument('-U', '--update', action='store', dest='update_opts', metavar='ARG',
                            help=f"options for `{bold}mas upgrade <application>{reset}' command")
    parser_mas.add_argument('-V', '--version', action='version', version=__version__)
    parser_mas.add_argument('mas_pkgs', action='append', nargs='*', help=argparse.SUPPRESS)

    parser_npm = subparser.add_parser('npm', description='Node.js Module Update Automator',
                                      usage='macdaily update npm [options] <modules>')
    parser_npm.add_argument('-a', '--all', action='store_true',
                            help='update all Node.js modules installed through Node.js Package Manager')
    parser_npm.add_argument('-p', '--package', metavar='MOD', action='append', dest='npm_pkgs',
                            help='name of Node.js modules to update')
    parser_npm.add_argument('-q', '--quiet', action='store_true',
                            help='run in quiet mode, with no output information')
    parser_npm.add_argument('-v', '--verbose', action='store_true',
                            help='run in verbose mode, with detailed output information')
    parser_npm.add_argument('-l', '--show-log', action='store_true',
                            help='open log in Console.app upon completion of command')
    parser_npm.add_argument('-Y', '--yes', action='store_true',
                            help='yes for all selections')
    parser_npm.add_argument('-N', '--no-cleanup', action='store_true',
                            help='do not run cleanup process')
    parser_npm.add_argument('-L', '--logging', action='store', dest='logging_opts', metavar='ARG',
                            help=f"options for `{bold}npm outdated --global{reset}' command")
    parser_npm.add_argument('-U', '--update', action='store', dest='update_opts', metavar='ARG',
                            help=f"options for `{bold}npm upgrade --global <module>{reset}' command")
    parser_npm.add_argument('-V', '--version', action='version', version=__version__)
    parser_npm.add_argument('npm_pkgs', action='append', nargs='*', help=argparse.SUPPRESS)

    parser_pip = subparser.add_parser('pip', description='Python Package Update Automator',
                                      usage='macdaily update pip [options] <packages>')
    parser_pip.add_argument('-a', '--all', action='store_true',
                            help='update all Python packages installed through Python Package Index')
    parser_pip.add_argument('-p', '--package', metavar='PKG', action='append', dest='pip_pkgs',
                            help='name of Python packages to update')
    parser_pip.add_argument('-I', '--python', action='store', metavar='VER', dest='version',
                            help='indicate packages from which version of Python will update')
    parser_pip.add_argument('-s', '--system', action='store_true',
                            help='update packages of Python provided by macOS system')
    parser_pip.add_argument('-b', '--brew', action='store_true',
                            help='update packages of Python installed from Homebrew')
    parser_pip.add_argument('-c', '--cpython', action='store_true',
                            help='update packages of CPython implementation')
    parser_pip.add_argument('-y', '--pypy', action='store_true',
                            help='update packages of PyPy implementation')
    parser_pip.add_argument('-d', '--pre', action='store_true',
                            help='include pre-release and development versions')
    parser_pip.add_argument('-q', '--quiet', action='store_true',
                            help='run in quiet mode, with no output information')
    parser_pip.add_argument('-v', '--verbose', action='store_true',
                            help='run in verbose mode, with detailed output information')
    parser_pip.add_argument('-l', '--show-log', action='store_true',
                            help='open log in Console.app upon completion of command')
    parser_pip.add_argument('-Y', '--yes', action='store_true',
                            help='yes for all selections')
    parser_pip.add_argument('-N', '--no-cleanup', action='store_true',
                            help='do not run cleanup process')
    parser_pip.add_argument('-L', '--logging', action='store', dest='logging_opts', metavar='ARG',
                            help=f"options for `{bold}pip list --outdated{reset}' command")
    parser_pip.add_argument('-U', '--update', action='store', dest='update_opts', metavar='ARG',
                            help=f"options for `{bold}pip install --upgrade <package>{reset}' command")
    parser_pip.add_argument('-V', '--version', action='version', version=__version__)
    parser_pip.add_argument('pip_pkgs', action='append', nargs='*', help=argparse.SUPPRESS)

    parser_brew = subparser.add_parser('brew', description='Homebrew Formula Update Automator',
                                       usage='macdaily update brew [options] <formulae>')
    parser_brew.add_argument('-a', '--all', action='store_true',
                             help='update all Homebrew formulae installed through Homebrew')
    parser_brew.add_argument('-p', '--package', metavar='FORM', action='append', dest='brew_pkgs',
                             help='name of Homebrew formulae to update')
    parser_brew.add_argument('-f', '--force', action='store_true',
                             help='always do a slower, full update check even if unnecessary')
    parser_brew.add_argument('-m', '--merge', action='store_true',
                             help=(f"`{bold}git merge{reset}' is used to include updates "
                                   f"(rather than `{bold}git rebase{reset}')"))
    parser_brew.add_argument('-q', '--quiet', action='store_true',
                             help='run in quiet mode, with no output information')
    parser_brew.add_argument('-v', '--verbose', action='store_true',
                             help='run in verbose mode, with detailed output information')
    parser_brew.add_argument('-l', '--show-log', action='store_true',
                             help='open log in Console.app upon completion of command')
    parser_brew.add_argument('-Y', '--yes', action='store_true',
                             help='yes for all selections')
    parser_brew.add_argument('-N', '--no-cleanup', action='store_true',
                             help='do not run cleanup process')
    parser_brew.add_argument('-L', '--logging', action='store', dest='logging_opts', metavar='ARG',
                             help=f"options for `{bold}brew outdated{reset}' command")
    parser_brew.add_argument('-U', '--update', action='store', dest='update_opts', metavar='ARG',
                             help=f"options for `{bold}brew upgrade <formula>{reset}' command")
    parser_brew.add_argument('-V', '--version', action='version', version=__version__)
    parser_brew.add_argument('brew_pkgs', action='append', nargs='*', help=argparse.SUPPRESS)

    parser_cask = subparser.add_parser('cask', description='Homebrew Cask Update Packages',
                                       usage='macdaily update cask [options] <casks>')
    parser_cask.add_argument('-a', '--all', action='store_true',
                             help='update all Caskroom binaries installed through Homebrew')
    parser_cask.add_argument('-p', '--package', metavar='CASK', action='append', dest='cask_pkgs',
                             help='name of Caskroom binaries to update')
    parser_cask.add_argument('-x', '--exhaust', action='store_true',
                             help='exhaustively check Caskroom for outdated Homebrew Casks')
    parser_cask.add_argument('-m', '--merge', action='store_true',
                             help=(f"`{bold}git merge{reset}' is used to include updates "
                                   f"(rather than `{bold}git rebase{reset}')"))
    parser_cask.add_argument('-f', '--force', action='store_true',
                             help=(f"use `{bold}--force{reset}' when running "
                                   f"`{bold}brew cask upgrade <cask>{reset}' command"))
    parser_cask.add_argument('-g', '--greedy', action='store_true',
                             help=(f"use `{bold}--greedy{reset}' when running "
                                   f"`{bold}brew cask upgrade <cask>{reset}' command"))
    parser_cask.add_argument('-q', '--quiet', action='store_true',
                             help='run in quiet mode, with no output information')
    parser_cask.add_argument('-v', '--verbose', action='store_true',
                             help='run in verbose mode, with detailed output information')
    parser_cask.add_argument('-l', '--show-log', action='store_true',
                             help='open log in Console.app upon completion of command')
    parser_cask.add_argument('-Y', '--yes', action='store_true',
                             help='yes for all selections')
    parser_cask.add_argument('-N', '--no-cleanup', action='store_true',
                             help='do not run cleanup process')
    parser_cask.add_argument('-L', '--logging', action='store', dest='logging_opts', metavar='ARG',
                             help=f"options for `{bold}brew cask outdated{reset}' command")
    parser_cask.add_argument('-U', '--update', action='store', dest='update_opts', metavar='ARG',
                             help=f"options for `{bold}brew cask upgrade <cask>{reset}' command")
    parser_cask.add_argument('-V', '--version', action='version', version=__version__)
    parser_cask.add_argument('cask_pkgs', action='append', nargs='*', help=argparse.SUPPRESS)

    parser_system = subparser.add_parser('system', description='System Software Update Automator',
                                         usage='macdaily update system [options] <software>')
    parser_system.add_argument('-a', '--all', action='store_true',
                               help=f"update all system software installed through `{bold}softwareupdate{reset}'")
    parser_system.add_argument('-p', '--package', metavar='SW', action='append', dest='system_pkgs',
                               help='name of system software to update')
    parser_system.add_argument('-r', '--recommended', action='store_true',
                               help='only update software that is recommended for your system')
    parser_system.add_argument('-R', '--restart', action='store_true',
                               help='automatically restart (or shut down) if required to complete installation')
    parser_system.add_argument('-q', '--quiet', action='store_true',
                               help='run in quiet mode, with no output information')
    parser_system.add_argument('-l', '--show-log', action='store_true',
                               help='open log in Console.app upon completion of command')
    parser_system.add_argument('-Y', '--yes', action='store_true',
                               help='yes for all selections')
    parser_system.add_argument('-L', '--logging', action='store', dest='logging_opts', metavar='ARG',
                               help=f"options for `{bold}softwareupdate --list{reset}' command")
    parser_system.add_argument('-U', '--update', action='store', dest='update_opts', metavar='ARG',
                               help=f"options for `{bold}softwareupdate --install <software>{reset}' command")
    parser_system.add_argument('-V', '--version', action='version', version=__version__)
    parser_system.add_argument('cask_pkgs', action='append', nargs='*', help=argparse.SUPPRESS)

    return parser
