#!/usr/bin/python3
# -*- coding: utf-8 -*-


import os
import re
import shlex
import shutil
import subprocess
import time


# change working directory
os.chdir(os.path.dirname(__file__))


# terminal display
red = 'tput setaf 1'    # blush / red
green = 'tput setaf 2'  # green
blue = 'tput setaf 14'  # blue
reset = 'tput sgr0'     # reset
bold = 'tput bold'      # bold
under = 'tput smul'     # underline


def _merge_packages(args):
    if 'package' in args and args.package:
        allflag = False
        nullflag = False
        packages = set()
        for pkg in args.package:
            if allflag or nullflag: break
            mapping = map(shlex.split, pkg.split(','))
            for list_ in mapping:
                if 'all' in list_:
                    packages = {'all'}
                    allflag = True; break
                if 'null' in list_:
                    packages = {'null'}
                    nullflag = True; break
                packages = packages.union(set(list_))
    elif args.all:
        packages = {'all'}
    else:
        packages = {'null'}
    return packages


def uninstall_pip(args, *, file, date, retset=False):
    quiet = str(args.quiet).lower()
    verbose = str(args.verbose).lower()
    yes = str(args.yes).lower()
    idep = str(args.idep).lower()
    packages = _merge_packages(args)

    mode = '-*- Python -*-'.center(80, ' ')
    with open(file, 'a') as logfile:
        logfile.write(f'\n\n{mode}\n\n')

    if not args.quiet:
        os.system(f'echo "-*- $({blue})Python$({reset}) -*-"; echo ;')

    if 'null' in packages:
        log = set()
        if not args.quiet:
            os.system(f'echo "$({green})No uninstallation performed.$({reset})"; echo ;')
        with open(file, 'a') as logfile:
            logfile.write('INF: No uninstallation performed.\n')
    else:
        flag = True if args.mode is None else (args.version == 1 or not any((args.system, args.brew, args.cpython, args.pypy)))
        if ('all' in packages and flag) or args.package is not None:
            system, brew, cpython, pypy, version = 'true', 'true', 'true', 'true', '1'
        else:
            system, brew, cpython, pypy, version = \
                str(args.system).lower(), str(args.brew).lower(), \
                str(args.cpython).lower(), str(args.pypy).lower(), str(args.version or 1)

        logging = subprocess.run(
            ['bash', './logging_pip.sh', date, system, brew, cpython, pypy, version, idep] + list(packages),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        log = set(logging.stdout.decode().split())

        subprocess.run(
            ['bash', './uninstall_pip.sh', date, system, brew, cpython, pypy, version, quiet, verbose, yes, idep] + list(packages)
        )

    if not args.quiet:
        time.sleep(5)
        os.system('tput clear')
    return log if retset else dict(pip=log)


def uninstall_brew(args, *, file, date, cleanup=True, retset=False):
    quiet = str(args.quiet).lower()
    verbose = str(args.verbose).lower()
    force = str(args.force).lower()
    yes = str(args.yes).lower()
    idep = str(args.idep).lower()
    packages = _merge_packages(args)

    if shutil.which('brew') is None:
        os.system(f'''
                echo "$({red})brew$({reset}): Command not found.";
                echo "You may find Homebrew on $({under})https://brew.sh$({reset}), or install Homebrew through following command:";
                echo $({bold})'/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"'$({reset})
        ''')
        return set() if retset else dict(brew=set())

    mode = '-*- Homebrew -*-'.center(80, ' ')
    with open(file, 'a') as logfile:
        logfile.write(f'\n\n{mode}\n\n')

    if not args.quiet:
        os.system(f'echo "-*- $({blue})Homebrew$({reset}) -*-"; echo ;')

    if 'null' in packages:
        log = set()
        if not args.quiet:
            os.system(f'echo "$({green})No uninstallation performed.$({reset})"; echo ;')
        with open(file, 'a') as logfile:
            logfile.write('INF: No uninstallation performed.\n')
    else:
        logging = subprocess.run(
            ['bash', './logging_brew.sh', date, idep] + list(packages),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        log = set(logging.stdout.decode().split())

        subprocess.run(
            ['bash', './uninstall_brew.sh', date, force, quiet, verbose, idep, yes] + list(packages)
        )

    if not args.quiet:
        time.sleep(5)
        os.system('tput clear')
    return log if retset else dict(brew=log)


def uninstall_cask(args, *, file, date, cleanup=True, retset=False):
    quiet = str(args.quiet).lower()
    verbose = str(args.verbose).lower()
    force = str(args.force).lower()
    packages = _merge_packages(args)

    testing = subprocess.run(
        shlex.split('brew cask'),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    if testing.returncode:
        os.system(f'''
                echo "$({red})cask$({reset}): Command not found.";
                echo "You may find Caskroom on $({under})https://caskroom.github.io$({reset}), or install Caskroom through following command:";
                echo $({bold})'brew tap caskroom/cask'$({reset})
        ''')
        return set() if retset else dict(cask=set())

    mode = '-*- Caskroom -*-'.center(80, ' ')
    with open(file, 'a') as logfile:
        logfile.write(f'\n\n{mode}\n\n')

    if not args.quiet:
        os.system(f'echo "-*- $({blue})Caskroom$({reset}) -*-"; echo ;')

    if 'null' in packages:
        log = set()
        if not args.quiet:
            os.system(f'echo "$({green})No uninstallation performed.$({reset})"; echo ;')
        with open(file, 'a') as logfile:
            logfile.write('INF: No uninstallation performed.\n')
    else:
        logging = subprocess.run(
            ['bash', './logging_cask.sh', date] + list(packages),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        log = set(logging.stdout.decode().split())

        subprocess.run(
            ['bash', './uninstall_cask.sh', date, quiet, verbose, force] + list(packages)
        )

    if not args.quiet:
        time.sleep(5)
        os.system('tput clear')
    return log if retset else dict(cask=log)


def uninstall_all(args, *, file, date):
    log = dict(
        pip = uninstall_pip(args, retset=True, file=file, date=date),
        brew = uninstall_brew(args, retset=True, file=file, date=date),
        cask = uninstall_cask(args, retset=True, file=file, date=date),
    )
    return log
