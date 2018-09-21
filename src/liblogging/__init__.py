# -*- coding: utf-8 -*-

import os
import shlex
import shutil
import subprocess
import sys

from macdaily.daily_utility import bold, green, red, reset, under

__all__ = [
    'logging_apm', 'logging_gem', 'logging_pip', 'logging_npm',
    'logging_brew', 'logging_cask', 'logging_dotapp', 'logging_macapp', 'logging_appstore',
]

# root path
ROOT = os.path.dirname(os.path.abspath(__file__))


def logging_apm(args, file, password, bash_timeout):
    if shutil.which('apm') is not None:
        subprocess.run(['bash', os.path.join(ROOT, 'logging_apm.sh'), file],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=bash_timeout)
        if not args.quiet:
            print(f'logging: {green}apm{reset}: {bold}Atom{reset} packages logged in {under}{file}{reset}')
    else:
        print(f'logging: {red}apm{reset}: command not found', file=sys.stderr)


def logging_appstore(args, file, password, bash_timeout):
    if shutil.which('find') is not None:
        subprocess.run(['bash', os.path.join(ROOT, 'logging_appstore.sh'), file],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=bash_timeout)
        if not args.quiet:
            print(f'logging: {green}appstore{reset}: {bold}Mac App Store{reset} '
                  f'applications logged in {under}{file}{reset}')
    else:
        print(f'logging: {red}appstore{reset}: command not found', file=sys.stderr)


def logging_brew(args, file, password, bash_timeout):
    if shutil.which('brew') is not None:
        subprocess.run(['bash', os.path.join(ROOT, 'logging_brew.sh'), file],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=bash_timeout)
        if not args.quiet:
            print(f'logging: {green}brew{reset}: {bold}Homebrew{reset} formulae logged in {under}{file}{reset}')
    else:
        print(f'logging: {red}brew{reset}: command not found', file=sys.stderr)


def logging_cask(args, file, password, bash_timeout):
    testing = subprocess.run(['brew', 'command', 'cask'],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if testing.returncode == 0:
        subprocess.run(['bash', os.path.join(ROOT, 'logging_cask.sh'), file],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=bash_timeout)
        if not args.quiet:
            print(f'logging: {green}cask{reset}: {bold}Caskroom{reset} binaries logged in {under}{file}{reset}')
    else:
        print(f'logging: {red}cask{reset}: command not found', file=sys.stderr)


def logging_dotapp(args, file, password, bash_timeout):
    if shutil.which('python') is not None:
        subprocess.run(['bash', os.path.join(ROOT, 'logging_dotapp.sh'), password, file],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=bash_timeout)
        if not args.quiet:
            print(f'logging: {green}dotapp{reset}: all applications ({bold}*.app{reset}) '
                  f'logged in {under}{file}{reset}')
    else:
        print(f'logging: {red}dotapp{reset}: command not found', file=sys.stderr)


def logging_gem(args, file, password, bash_timeout):
    if shutil.which('npm') is not None:
        subprocess.run(['bash', os.path.join(ROOT, 'logging_gem.sh'), file],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=bash_timeout)
        if not args.quiet:
            print(f'logging: {green}gem{reset}: {bold}Ruby{reset} gems logged in {under}{file}{reset}')
    else:
        print(f'logging: {red}gem{reset}: command not found', file=sys.stderr)


def logging_macapp(args, file, password, bash_timeout):
    if shutil.which('find') is not None:
        subprocess.run(['bash', os.path.join(ROOT, 'logging_macapp.sh'), file],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=bash_timeout)
        if not args.quiet:
            print(f'logging: {green}macapp{reset}: all applications placed in {bold}/Application{reset} folder '
                  f'logged in {under}{file}{reset}')
    else:
        print(f'logging: {red}macapp{reset}: command not found', file=sys.stderr)


def logging_npm(args, file, password, bash_timeout):
    if shutil.which('npm') is not None:
        subprocess.run(['bash', os.path.join(ROOT, 'logging_npm.sh'), file],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=bash_timeout)
        if not args.quiet:
            print(f'logging: {green}npm{reset}: {bold}Node.js{reset} modules logged in {under}{file}{reset}')
    else:
        print(f'logging: {red}npm{reset}: command not found', file=sys.stderr)


def logging_pip(args, file, password, bash_timeout):
    if shutil.which('python') is not None:
        flag = not ('pip' in args.mode and any((args.version, args.system, args.brew, args.cpython, args.pypy)))
        if flag:
            system, brew, cpython, pypy, version = 'true', 'true', 'true', 'true', '1'
        else:
            system, brew, cpython, pypy, version = \
                str(args.system).lower(), str(args.brew).lower(), \
                str(args.cpython).lower(), str(args.pypy).lower(), str(args.version)
        subprocess.run(['bash', os.path.join(ROOT, 'logging_pip.sh'), file, system, brew, cpython, pypy, version],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=bash_timeout)
        subprocess.run(['bash', os.path.join(ROOT, 'relink_pip.sh')],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if not args.quiet:
            print(f'logging: {green}pip{reset}: {bold}Python{reset} packages logged in {under}{file}{reset}')
    else:
        print(f'logging: {red}pip{reset}: command not found', file=sys.stderr)
