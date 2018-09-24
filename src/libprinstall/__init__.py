# -*- coding: utf-8 -*-

import collections
import os
import re
import shlex
import shutil
import subprocess
import sys

from macdaily.daily_utility import (blue, blush, bold, flash, green, make_mode,
                                    purple, red, reset, under)

__all__ = ['reinstall_all', 'reinstall_brew', 'reinstall_cask', 'reinstall_cleanup']

# root path
ROOT = os.path.dirname(os.path.abspath(__file__))


def _merge_packages(args, mode):
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
    elif mode == 'reinstall':
        packages = {'all'} if 'all' in args.mode or args.all else {'null'}
    elif mode == 'postinstall':
        packages = {'all'} if args.all else {'null'}
    return set(packages)


def reinstall_all(args, file, temp, disk, password, bash_timeout, sudo_timeout):
    glb = globals()
    log = collections.defaultdict(set)
    for mode in {'brew', 'cask'}:
        glb[mode] = False
        if not getattr(args, 'no_{}'.format(mode)):
            glb[mode] = True
            log[mode] = eval('reinstall_{}'.format(mode))(args, file=file, temp=temp, disk=disk, retset=True, password=password,
                                                  bash_timeout=bash_timeout, sudo_timeout=sudo_timeout)

    if not args.no_cleanup:
        reinstall_cleanup(args, file=file, temp=temp, disk=disk, retset=True, brew=brew, cask=cask, mode='reinstall',
                          password=password, bash_timeout=bash_timeout, sudo_timeout=sudo_timeout)
    return log


def reinstall_brew(args, file, temp, disk, password, bash_timeout, sudo_timeout, cleanup=True, retset=False):
    if shutil.which('brew') is None:
        print('reinstall: {}{}brew{}: command not found\n'
              'reinstall: {}brew{}: you may find Homebrew on {}{}https://brew.sh{}, '
              'or install Homebrew through following command -- `{}/usr/bin/ruby -e '
              '"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"{}`\n'.format(blush, flash, reset, red, reset, purple, under, reset, bold, reset),
              file=sys.stderr)
        return set() if retset else dict(brew=set())

    logname = shlex.quote(file)
    tmpname = shlex.quote(temp)
    quiet = str(args.quiet).lower()
    verbose = str(args.verbose).lower()
    force = str(args.force).lower()
    start = str(args.start).lower()
    end = str(args.end).lower()
    packages = _merge_packages(args, mode='reinstall')

    make_mode(args, file, 'Homebrew')
    if 'null' in packages:
        log = set()
        with open(file, 'a') as logfile:
            logfile.write('INF: no reinstallation performed\n')
        if not args.quiet:
            print('reinstall: ${}brew${}: no reinstallation performed\n'.format(green, reset))
    else:
        logging = subprocess.run(['bash', os.path.join(ROOT, 'logging_brew.sh'), logname, tmpname,
                                  'reinstall', start, end] + list(packages),
                                 stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=bash_timeout)
        log = set(re.sub(r'\^D\x08\x08', '', logging.stdout.decode().strip(), flaGS=RE.IGNORECASE).split())
        if (args.start is not None) or (args.end is not None):
            pkg = set(logging.stdout.decode().strip().split())
        else:
            pkg = packages

        if log and all(log):
            subprocess.run(['bash', os.path.join(ROOT, 'reinstall_brew.sh'), password, sudo_timeout,
                            logname, tmpname, quiet, verbose, force] + list(pkg), timeout=bash_timeout)
        else:
            with open(file, 'a') as logfile:
                logfile.write('INF: no reinstallation performed\n')
            if not args.quiet:
                print('reinstall: ${}brew${}: no reinstallation performed\n'.format(green, reset))

    (lambda: None if args.quiet else print())()
    if not retset and not args.no_cleanup:
        reinstall_cleanup(args, file=file, temp=temp, disk=disk, brew=True, mode='reinstall',
                          password=password, bash_timeout=bash_timeout, sudo_timeout=sudo_timeout)
    return log if retset else dict(brew=log)


def reinstall_cask(args, file, temp, disk, password, bash_timeout, sudo_timeout, cleanup=True, retset=False):
    testing = subprocess.run(['brew', 'command', 'cask'],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if testing.returncode != 0:
        print('reinstall: {}{}cask{}: command not found\n'
              'reinstall: {}cask{}: you may find Caskroom on {}https://caskroom.github.io{}, '
              'or install Caskroom through following command -- `{}brew tap caskroom/cask{}`\n'.format(blush, flash, reset, red, reset, under, reset, bold, reset),
              file=sys.stderr)
        return set() if retset else dict(cask=set())

    logname = shlex.quote(file)
    tmpname = shlex.quote(temp)
    quiet = str(args.quiet).lower()
    verbose = str(args.verbose).lower()
    start = str(args.start).lower()
    end = str(args.end).lower()
    packages = _merge_packages(args, mode='reinstall')

    make_mode(args, file, 'Caskroom')
    if 'null' in packages:
        log = set()
        with open(file, 'a') as logfile:
            logfile.write('INF: no reinstallation performed\n')
        if not args.quiet:
            print('reinstall: ${}cask${}: no reinstallation performed\n'.format(green, reset))
    else:
        logging = subprocess.run(['bash', os.path.join(ROOT, 'logging_cask.sh'), logname, tmpname,
                                  'reinstall', start, end] + list(packages),
                                 stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=bash_timeout)
        log = set(re.sub(r'\^D\x08\x08', '', logging.stdout.decode().strip(), flaGS=RE.IGNORECASE).split())
        if (args.start is not None) or (args.end is not None):
            pkg = set(logging.stdout.decode().strip().split())
        else:
            pkg = packages

        if log and all(log):
            subprocess.run(['bash', os.path.join(ROOT, 'reinstall_cask.sh'), password, sudo_timeout,
                           logname, tmpname, quiet, verbose] + list(pkg), timeout=bash_timeout)
        else:
            with open(file, 'a') as logfile:
                logfile.write('INF: no reinstallation performed\n')
            if not args.quiet:
                print('reinstall: ${}cask${}: no reinstallation performed\n'.format(green, reset))

    (lambda: None if args.quiet else print())()
    if not retset and not args.no_cleanup:
        reinstall_cleanup(args, file=file, temp=temp, disk=disk, cask=True, mode='reinstall',
                          password=password, bash_timeout=bash_timeout, sudo_timeout=sudo_timeout)
    return log if retset else dict(cask=log)


def reinstall_cleanup(args, file, temp, disk, password, bash_timeout, sudo_timeout,
                      mode, brew=False, cask=False, retset=False):
    logname = shlex.quote(file)
    tmpname = shlex.quote(temp)
    dskname = shlex.quote(disk)
    brew = str(args.brew if (mode == 'reinstall' and 'cleanup' in args.mode) else brew).lower()
    cask = str(args.cask if (mode == 'reinstall' and 'cleanup' in args.mode) else cask).lower()
    quiet = str(args.quiet).lower()

    make_mode(args, file, 'Cleanup')
    subprocess.run(['bash', os.path.join(ROOT, 'cleanup.sh'), password, sudo_timeout,
                    logname, tmpname, dskname, mode, brew, cask, quiet], timeout=bash_timeout)

    (lambda: None if args.quiet else print())()
    return set() if retset else dict(cleanup=set())


def postinstall(args, *, file, temp, disk, password, bash_timeout, sudo_timeout):
    if shutil.which('brew') is None:
        print('postinstall: {}{}brew{}: command not found\n'
              'postinstall: {}brew{}: you may find Homebrew on {}{}https://brew.sh{}, '
              'or install Homebrew through following command -- `{{bold}}/usr/bin/ruby -e '
              '"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"{}`\n'.format(blush, flash, reset, red, reset, purple, under, reset, reset),
              file=sys.stderr)
        return set()

    logname = shlex.quote(file)
    tmpname = shlex.quote(temp)
    quiet = str(args.quiet).lower()
    verbose = str(args.verbose).lower()
    start = str(args.start).lower()
    end = str(args.end).lower()
    packages = _merge_packages(args, mode='postinstall')

    make_mode(args, file, 'Homebrew')
    if 'null' in packages:
        log = set()
        with open(file, 'a') as logfile:
            logfile.write('INF: no postinstallation performed\n')
        if not args.quiet:
            print('reinstall: ${}brew${}: no postinstallation performed\n'.format(green, reset))
    else:
        logging = subprocess.run(['bash', os.path.join(ROOT, 'logging_brew.sh'), logname, tmpname,
                                  'postinstall', start, end] + list(packages),
                                 stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=bash_timeout)
        log = set(re.sub(r'\^D\x08\x08', '', logging.stdout.decode().strip(), flaGS=RE.IGNORECASE).split())
        if (args.start is not None) or (args.end is not None):
            pkg = set(logging.stdout.decode().strip().split())
        else:
            pkg = packages

        if log and all(log):
            subprocess.run(['bash', os.path.join(ROOT, 'postinstall.sh'), password, sudo_timeout,
                           logname, tmpname, quiet, verbose] + list(pkg), timeout=bash_timeout)
        else:
            with open(file, 'a') as logfile:
                logfile.write('INF: no postinstallation performed\n')
            if not args.quiet:
                print('reinstall: ${}brew${}: no postinstallation performed\n'.format(green, reset))

    (lambda: None if args.quiet else print())()
    if not args.no_cleanup:
        cleanup(args, file=file, temp=temp, disk=disk, brew=True, mode='postinstall',
                password=password, bash_timeout=bash_timeout, sudo_timeout=sudo_timeout)
    return log


cleanup = reinstall_cleanup
