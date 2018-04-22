# -*- coding: utf-8 -*-


import os
import shlex
import shutil
import subprocess


__all__ = [
    'logging_apm', 'logging_gem', 'logging_pip', 'logging_npm',
    'logging_brew', 'logging_cask', 'logging_dotapp', 'logging_macapp', 'logging_appstore',
]


# terminal display
reset  = '\033[0m'      # reset
bold   = '\033[1m'      # bold
under  = '\033[4m'      # underline
red    = '\033[91m'     # bright red foreground
green  = "\033[92m"     # bright green foreground


def logging_apm(args, *, file):
    if shutil.which('apm') is not None:
        subprocess.run(['bash', 'liblogging/logging_apm.sh', file])
        if not args.quiet:
            print(f'logging: {green}apm{reset}: {bold}Atom{reset} packages logged in {under}{file}{reset}')
    else:
        if not args.quiet:
            print(f'logging: {red}apm{reset}: command not found')


def logging_appstore(args, *, file):
    if shutil.which('find') is not None:
        subprocess.run(['bash', 'liblogging/logging_appstore.sh', file])
        if not args.quiet:
            print(f'logging: {green}appstore{reset}: {bold}Mac App Store{reset} applications logged in {under}{file}{reset}')
    else:
        if not args.quiet:
            print(f'logging: {red}appstore{reset}: command not found')


def logging_brew(args, *, file):
    if shutil.which('brew') is not None:
        subprocess.run(['bash', 'liblogging/logging_brew.sh', file])
        if not args.quiet:
            print(f'logging: {green}brew{reset}: {bold}Homebrew{reset} formulae logged in {under}{file}{reset}')
    else:
        if not args.quiet:
            print(f'logging: {red}brew{reset}: command not found')


def logging_cask(args, *, file):
    testing = subprocess.run(
        shlex.split('brew cask'),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    if not testing.returncode:
        subprocess.run(['bash', 'liblogging/logging_cask.sh', file])
        if not args.quiet:
            print(f'logging: {green}cask{reset}: {bold}Caskroom{reset} binaries logged in {under}{file}{reset}')
    else:
        if not args.quiet:
            print(f'logging: {red}cask{reset}: command not found')


def logging_dotapp(args, *, file):
    if shutil.which('find') is not None:
        subprocess.run(['sudo', '-H', 'bash', 'liblogging/logging_dotapp.sh', file])
        if not args.quiet:
            print(f'logging: {green}dotapp{reset}: all applications ({bold}*.app{reset}) logged in {under}{file}{reset}')
    else:
        if not args.quiet:
            print(f'logging: {red}dotapp{reset}: command not found')


def logging_gem(args, *, file):
    if shutil.which('npm') is not None:
        subprocess.run(['bash', 'liblogging/logging_gem.sh', file])
        if not args.quiet:
            print(f'logging: {green}gem{reset}: {bold}Ruby{reset} gems logged in {under}{file}{reset}')
    else:
        if not args.quiet:
            print(f'logging: {red}gem{reset}: command not found')


def logging_macapp(args, *, file):
    if shutil.which('find') is not None:
        subprocess.run(['bash', 'liblogging/logging_macapp.sh', file])
        if not args.quiet:
            print(f'logging: {green}macapp{reset}: all applications placed in {bold}/Application{reset} folder logged in {under}{file}{reset}')
    else:
        if not args.quiet:
            print(f'logging: {red}macapp{reset}: command not found')


def logging_npm(args, *, file):
    if shutil.which('npm') is not None:
        subprocess.run(['bash', 'liblogging/logging_npm.sh', file])
        if not args.quiet:
            print(f'logging: {green}npm{reset}: {bold}Node.js{reset} modules logged in {under}{file}{reset}')
    else:
        if not args.quiet:
            print(f'logging: {red}npm{reset}: command not found')


def logging_pip(args, *, file):
    if shutil.which('python') is not None:
        flag = not ('pip' in args.mode and any((args.version, args.system, args.brew, args.cpython, args.pypy)))
        if flag:
            system, brew, cpython, pypy, version = 'true', 'true', 'true', 'true', '1'
        else:
            system, brew, cpython, pypy, version = \
                str(args.system).lower(), str(args.brew).lower(), \
                str(args.cpython).lower(), str(args.pypy).lower(), str(args.version)

        subprocess.run(
            ['bash', 'liblogging/logging_pip.sh', file, system, brew, cpython, pypy, version]
        )
        subprocess.run(
            ['bash', 'liblogging/relink_pip.sh'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        if not args.quiet:
            print(f'logging: {green}pip{reset}: {bold}Python{reset} packages logged in {under}{file}{reset}')
    else:
        if not args.quiet:
            print(f'logging: {red}pip{reset}: command not found')
