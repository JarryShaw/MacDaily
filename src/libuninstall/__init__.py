# -*- coding: utf-8 -*-

import collections
import os
import re
import shlex
import shutil
import signal
import subprocess
import sys

from macdaily.daily_utility import (blue, blush, bold, flash, green, make_mode,
                                    purple, red, reset, under)

__all__ = ['uninstall_all', 'uninstall_pip', 'uninstall_brew', 'uninstall_cask']

# root path
ROOT = os.path.dirname(os.path.abspath(__file__))


def _merge_packages(args):
    if 'package' in args and args.package:
        packages = list()
        for pkg in map(lambda s: re.split(r'\W*,\W*', s), args.package):
            if 'all' in pkg:
                setattr(args, 'all', True)
                packages = {'all'}
                break
            if 'null' in pkg:
                setattr(args, 'all', False)
                packages = {'null'}
                break
            packages.extend(pkg)
    elif 'all' in args.mode or args.all:
        packages = {'all'}
    else:
        packages = {'null'}
    return set(packages)


def uninstall_all(args, file, temp, password, bash_timeout, sudo_timeout):
    log = collections.defaultdict(set)
    for mode in filter(lambda mode: (not getattr(args, 'no_{}'.format(mode))), {'pip', 'brew', 'cask'}):
        log[mode] = eval('uninstall_{}'.format(mode))(args, file=file, temp=temp, retset=True, password=password,
                                              bash_timeout=bash_timeout, sudo_timeout=sudo_timeout)
    return log


def uninstall_pip(args, file, temp, password, bash_timeout, sudo_timeout, retset=False):
    logname = shlex.quote(file)
    tmpname = shlex.quote(temp)
    quiet = str(args.quiet).lower()
    verbose = str(args.verbose).lower()
    yes = str(args.yes).lower()
    idep = str(args.idep).lower()
    packages = _merge_packages(args)

    make_mode(args, file, 'Python')
    if 'null' in packages:
        log = set()
        with open(file, 'a') as logfile:
            logfile.write('INF: no uninstallation performed\n')
        if not args.quiet:
            print('uninstall: ${}pip${}: no uninstallation performed\n'.format(green, reset))
    else:
        flag = not ('pip' in args.mode and any((args.version, args.system, args.brew, args.cpython, args.pypy)))
        if flag and packages:
            system, brew, cpython, pypy, version = 'true', 'true', 'true', 'true', '1'
        else:
            system, brew, cpython, pypy, version = \
                str(args.system).lower(), str(args.brew).lower(), \
                str(args.cpython).lower(), str(args.pypy).lower(), str(args.version)

        logging = subprocess.run(['bash', os.path.join(ROOT, 'logging_pip.sh'), logname, tmpname,
                                  system, brew, cpython, pypy, version, idep] + list(packages),
                                 stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=bash_timeout)
        log = set(re.sub(r'\^D\x08\x08', '', logging.stdout.decode().strip(), re.IGNORECASE).split())
        if 'macdaily' in log:
            os.kill(os.getpid(), signal.SIGUSR1)

        subprocess.run(['bash', os.path.join(ROOT, 'uninstall_pip.sh'), password, sudo_timeout, logname, tmpname,
                        system, brew, cpython, pypy, version, verbose, quiet, yes, idep] + list(packages),
                       timeout=bash_timeout)
        subprocess.run(['bash', os.path.join(ROOT, 'relink_pip.sh')],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=bash_timeout)

    (lambda: None if args.quiet else print())()
    return log if retset else dict(pip=log)


def uninstall_brew(args, file, temp, password, bash_timeout, sudo_timeout, retset=False):
    if shutil.which('brew') is None:
        print('uninstall: {}{}brew{}: command not found\n'
              'uninstall: {}brew{}: you may find Homebrew on {}{}https://brew.sh{}, '
              'or install Homebrew through following command -- `{}/usr/bin/ruby -e '
              '"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"{}`\n'.format(blush, flash, reset, red, reset, purple, under, reset, bold, reset),
              file=sys.stderr)
        return set() if retset else dict(brew=set())

    logname = shlex.quote(file)
    tmpname = shlex.quote(temp)
    quiet = str(args.quiet).lower()
    verbose = str(args.verbose).lower()
    force = str(args.force).lower()
    yes = str(args.yes).lower()
    idep = str(args.idep).lower()
    packages = _merge_packages(args)

    make_mode(args, file, 'Homebrew')
    if 'null' in packages:
        log = set()
        with open(file, 'a') as logfile:
            logfile.write('INF: no uninstallation performed\n')
        if not args.quiet:
            print('uninstall: ${}brew${}: no uninstallation performed\n'.format(green, reset))
    else:
        logging = subprocess.run(['bash', os.path.join(ROOT, 'logging_brew.sh'),
                                  logname, tmpname, idep] + list(packages),
                                 stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=bash_timeout)
        log = set(re.sub(r'\^D\x08\x08', '', logging.stdout.decode().strip(), re.IGNORECASE).split())

        subprocess.run(['bash', os.path.join(ROOT, 'uninstall_brew.sh'), password, sudo_timeout,
                       logname, tmpname, force, quiet, verbose, idep, yes] + list(packages), timeout=bash_timeout)

    (lambda: None if args.quiet else print())()
    return log if retset else dict(brew=log)


def uninstall_cask(args, file, temp, password, bash_timeout, sudo_timeout, retset=False):
    testing = subprocess.run(['brew', 'command', 'cask'],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if testing.returncode != 0:
        print('uninstall: {}{}cask{}: command not found\n'
              'uninstall: {}cask{}: you may find Caskroom on {}https://caskroom.github.io{}, '
              'or install Caskroom through following command -- '
              '`{}brew tap caskroom/cask{}`\n'.format(blush, flash, reset, red, reset, under, reset, bold, reset), file=sys.stderr)
        return set() if retset else dict(cask=set())

    logname = shlex.quote(file)
    tmpname = shlex.quote(temp)
    quiet = str(args.quiet).lower()
    verbose = str(args.verbose).lower()
    force = str(args.force).lower()
    packages = _merge_packages(args)

    make_mode(args, file, 'Caskroom')
    if 'null' in packages:
        log = set()
        with open(file, 'a') as logfile:
            logfile.write('INF: no uninstallation performed\n')
        if not args.quiet:
            print('uninstall: ${}cask${}: no uninstallation performed\n'.format(green, reset))
    else:
        logging = subprocess.run(['bash', os.path.join(ROOT, 'logging_cask.sh'), logname, tmpname] + list(packages),
                                 stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=bash_timeout)
        log = set(re.sub(r'\^D\x08\x08', '', logging.stdout.decode().strip(), re.IGNORECASE).split())

        subprocess.run(['bash', os.path.join(ROOT, 'uninstall_cask.sh'), password, sudo_timeout,
                       logname, tmpname, quiet, verbose, force] + list(packages), timeout=bash_timeout)

    (lambda: None if args.quiet else print())()
    return log if retset else dict(cask=log)
