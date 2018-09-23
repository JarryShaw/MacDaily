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
    lcl = locals()
    log = collections.defaultdict(set)
    for mode in {'brew', 'cask'}:
        lcl[mode] = False
        if not getattr(args, f'no_{mode}'):
            lcl[mode] = True
            log[mode] = eval(f'reinstall_{mode}')(args, file=file, temp=temp, disk=disk, retset=True, password=password,
                                                  bash_timeout=bash_timeout, sudo_timeout=sudo_timeout)

    if not args.no_cleanup:
        reinstall_cleanup(args, file=file, temp=temp, disk=disk, retset=True, brew=brew, cask=cask, mode='reinstall',
                          password=password, bash_timeout=bash_timeout, sudo_timeout=sudo_timeout)
    return log


def reinstall_brew(args, file, temp, disk, password, bash_timeout, sudo_timeout, cleanup=True, retset=False):
    if shutil.which('brew') is None:
        print(f'reinstall: {blush}{flash}brew{reset}: command not found\n'
              f'reinstall: {red}brew{reset}: you may find Homebrew on {purple}{under}https://brew.sh{reset}, '
              f'or install Homebrew through following command -- `{bold}/usr/bin/ruby -e '
              f'"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"{reset}`\n',
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
            print(f'reinstall: ${green}brew${reset}: no reinstallation performed\n')
    else:
        logging = subprocess.run(['bash', os.path.join(ROOT, 'logging_brew.sh'), logname, tmpname,
                                  'reinstall', start, end] + list(packages),
                                 stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=bash_timeout)
        log = set(re.sub(r'\^D\x08\x08', '', logging.stdout.decode().strip(), re.IGNORECASE).split())
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
                print(f'reinstall: ${green}brew${reset}: no reinstallation performed\n')

    (lambda: None if args.quiet else print())()
    if not retset and not args.no_cleanup:
        reinstall_cleanup(args, file=file, temp=temp, disk=disk, brew=True, mode='reinstall',
                          password=password, bash_timeout=bash_timeout, sudo_timeout=sudo_timeout)
    return log if retset else dict(brew=log)


def reinstall_cask(args, file, temp, disk, password, bash_timeout, sudo_timeout, cleanup=True, retset=False):
    testing = subprocess.run(['brew', 'command', 'cask'],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if testing.returncode != 0:
        print(f'reinstall: {blush}{flash}cask{reset}: command not found\n'
              f'reinstall: {red}cask{reset}: you may find Caskroom on {under}https://caskroom.github.io{reset}, '
              f'or install Caskroom through following command -- `{bold}brew tap caskroom/cask{reset}`\n',
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
            print(f'reinstall: ${green}cask${reset}: no reinstallation performed\n')
    else:
        logging = subprocess.run(['bash', os.path.join(ROOT, 'logging_cask.sh'), logname, tmpname,
                                  'reinstall', start, end] + list(packages),
                                 stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=bash_timeout)
        log = set(re.sub(r'\^D\x08\x08', '', logging.stdout.decode().strip(), re.IGNORECASE).split())
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
                print(f'reinstall: ${green}cask${reset}: no reinstallation performed\n')

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
        print(f'postinstall: {blush}{flash}brew{reset}: command not found\n'
              f'postinstall: {red}brew{reset}: you may find Homebrew on {purple}{under}https://brew.sh{reset}, '
              'or install Homebrew through following command -- `{bold}/usr/bin/ruby -e '
              f'"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"{reset}`\n',
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
            print(f'reinstall: ${green}brew${reset}: no postinstallation performed\n')
    else:
        logging = subprocess.run(['bash', os.path.join(ROOT, 'logging_brew.sh'), logname, tmpname,
                                  'postinstall', start, end] + list(packages),
                                 stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=bash_timeout)
        log = set(re.sub(r'\^D\x08\x08', '', logging.stdout.decode().strip(), re.IGNORECASE).split())
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
                print(f'reinstall: ${green}brew${reset}: no postinstallation performed\n')

    (lambda: None if args.quiet else print())()
    if not args.no_cleanup:
        cleanup(args, file=file, temp=temp, disk=disk, brew=True, mode='postinstall',
                password=password, bash_timeout=bash_timeout, sudo_timeout=sudo_timeout)
    return log


cleanup = reinstall_cleanup
