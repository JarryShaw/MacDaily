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
            print('logging: {}apm{}: {}Atom{} packages logged in {}{}{}'.format(green, reset, bold, reset, under, file, reset))
    else:
        print('logging: {}apm{}: command not found'.format(red, reset), file=sys.stderr)


def logging_appstore(args, file, password, bash_timeout):
    if shutil.which('find') is not None:
        subprocess.run(['bash', os.path.join(ROOT, 'logging_appstore.sh'), file],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=bash_timeout)
        if not args.quiet:
            print('logging: {}appstore{}: {}Mac App Store{} '
                  'applications logged in {}{}{}'.format(green, reset, bold, reset, under, file, reset))
    else:
        print('logging: {}appstore{}: command not found'.format(red, reset), file=sys.stderr)


def logging_brew(args, file, password, bash_timeout):
    if shutil.which('brew') is not None:
        subprocess.run(['bash', os.path.join(ROOT, 'logging_brew.sh'), file],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=bash_timeout)
        if not args.quiet:
            print('logging: {}brew{}: {}Homebrew{} formulae logged in {}{}{}'.format(green, reset, bold, reset, under, file, reset))
    else:
        print('logging: {}brew{}: command not found'.format(red, reset), file=sys.stderr)


def logging_cask(args, file, password, bash_timeout):
    testing = subprocess.run(['brew', 'command', 'cask'],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if testing.returncode == 0:
        subprocess.run(['bash', os.path.join(ROOT, 'logging_cask.sh'), file],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=bash_timeout)
        if not args.quiet:
            print('logging: {}cask{}: {}Caskroom{} binaries logged in {}{}{}'.format(green, reset, bold, reset, under, file, reset))
    else:
        print('logging: {}cask{}: command not found'.format(red, reset), file=sys.stderr)


def logging_dotapp(args, file, password, bash_timeout):
    if shutil.which('python') is not None:
        subprocess.run(['bash', os.path.join(ROOT, 'logging_dotapp.sh'), password, file],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=bash_timeout)
        if not args.quiet:
            print('logging: {}dotapp{}: all applications ({}*.app{}) '
                  'logged in {}{}{}'.format(green, reset, bold, reset, under, file, reset))
    else:
        print('logging: {}dotapp{}: command not found'.format(red, reset), file=sys.stderr)


def logging_gem(args, file, password, bash_timeout):
    if shutil.which('npm') is not None:
        subprocess.run(['bash', os.path.join(ROOT, 'logging_gem.sh'), file],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=bash_timeout)
        if not args.quiet:
            print('logging: {}gem{}: {}Ruby{} gems logged in {}{}{}'.format(green, reset, bold, reset, under, file, reset))
    else:
        print('logging: {}gem{}: command not found'.format(red, reset), file=sys.stderr)


def logging_macapp(args, file, password, bash_timeout):
    if shutil.which('find') is not None:
        subprocess.run(['bash', os.path.join(ROOT, 'logging_macapp.sh'), file],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=bash_timeout)
        if not args.quiet:
            print('logging: {}macapp{}: all applications placed in {}/Application{} folder '
                  'logged in {}{}{}'.format(green, reset, bold, reset, under, file, reset))
    else:
        print('logging: {}macapp{}: command not found'.format(red, reset), file=sys.stderr)


def logging_npm(args, file, password, bash_timeout):
    if shutil.which('npm') is not None:
        subprocess.run(['bash', os.path.join(ROOT, 'logging_npm.sh'), file],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=bash_timeout)
        if not args.quiet:
            print('logging: {}npm{}: {}Node.js{} modules logged in {}{}{}'.format(green, reset, bold, reset, under, file, reset))
    else:
        print('logging: {}npm{}: command not found'.format(red, reset), file=sys.stderr)


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
            print('logging: {}pip{}: {}Python{} packages logged in {}{}{}'.format(green, reset, bold, reset, under, file, reset))
    else:
        print('logging: {}pip{}: command not found'.format(red, reset), file=sys.stderr)
