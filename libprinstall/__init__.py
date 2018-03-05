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


def _merge_packages(args, *, mode):
    if 'package' in args and args.package:
        allflag = False
        packages = set()
        for pkg in args.package:
            if allflag: break
            mapping = map(shlex.split, pkg.split(','))
            for list_ in mapping:
                if 'all' in list_:
                    packages = {'all'}
                    allflag = True; break
                packages = packages.union(set(list_))
    elif mode == 'reinstall':
        if args.all:
            packages = {'all'}
        else:
            packages = {'null'}
    else:   # 'postinstall'
        packages = {'all'}
    return packages


def reinstall_brew(args, *, file, date, cleanup=True, retset=False):
    quiet = str(args.quiet).lower()
    verbose = str(args.verbose).lower()
    force = str(args.force).lower()
    start = str(args.start).lower()
    end = str(args.end).lower()
    packages = _merge_packages(args, mode='reinstall')

    if shutil.which('brew') is None:
        os.system(f'''
                echo "$({red})brew$({reset}): Command not found.";
                echo "You may find Homebrew on $({under})https://brew.sh$({reset}), or install Homebrew through following command:"
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
            os.system(f'echo "$({green})No reinstallation performed.$({reset})"; echo ;')
        with open(file, 'a') as logfile:
            logfile.write('INF: No reinstallation performed.\n')
    else:
        logging = subprocess.run(
            ['bash', './logging_brew.sh', date, 'reinstall', start, end] + list(packages),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        log = set(logging.stdout.decode().split())
        if (args.start is not None) or (args.end is not None):
            pkg = set(logging.stdout.decode().split())
        else:
            pkg = packages

        if log:
            subprocess.run(
                ['bash', './reinstall_brew.sh', date, quiet, verbose, force] + list(pkg)
            )
        else:
            if not args.quiet:
                os.system(f'echo "$({green})No reinstallation performed.$({reset})"; echo ;')
            with open(file, 'a') as logfile:
                logfile.write('INF: No reinstallation performed.\n')

    if cleanup:
        mode = '-*- Cleanup -*-'.center(80, ' ')
        with open(file, 'a') as logfile:
            logfile.write(f'\n\n{mode}\n\n')

        if not args.quiet:
            time.sleep(5)
            os.system('tput clear')
            os.system(f'echo "-*- $({blue})Cleanup$({reset}) -*-"; echo ;')

        subprocess.run(
            ['bash', './cleanup.sh', date, 'reinstall', 'true', 'false', quiet, verbose]
        )

    if not args.quiet:
        time.sleep(5)
        os.system('tput clear')
    return log if retset else dict(brew=log)


def reinstall_cask(args, *, file, date, cleanup=True, retset=False):
    quiet = str(args.quiet).lower()
    verbose = str(args.verbose).lower()
    start = str(args.start).lower()
    end = str(args.end).lower()
    packages = _merge_packages(args, mode='reinstall')

    testing = subprocess.run(
        shlex.split('brew cask'),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    if testing.returncode:
        os.system(f'''
                echo "$({red})cask$({reset}): Command not found.";
                echo "You may find Caskroom on $({under})https://caskroom.github.io$({reset}), or install Caskroom through following command:"
                echo $({bold})'brew tap caskroom/cask'$({reset})
        ''')
        return set() if retset else dict(cask=set())

    mode = '-*- Caskroom -*-'.center(80, ' ')
    with open(file, 'a') as logfile:
        logfile.write(f'\n\n{mode}\n\n')

    if not args.quiet:
        os.system(f'echo "-*- $({blue})Caskroom$({reset}) -*-"; echo ;')

    if ('all' in packages) or (args.start is not None) or (args.end is not None):
        logging = subprocess.run(
            ['bash', './logging_cask.sh', date, 'reinstall', start, end] + list(packages),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        log = set(logging.stdout.decode().split())
    else:
        log = packages

    if log:
        subprocess.run(
            ['bash', './reinstall_cask.sh', date, quiet, verbose] + list(log)
        )
    else:
        if not args.quiet:
            os.system(f'echo "$({green})No reinstallation performed.$({reset})"; echo ;')
        with open(file, 'a') as logfile:
            logfile.write('INF: No reinstallation performed.\n')

    if cleanup:
        mode = '-*- Cleanup -*-'.center(80, ' ')
        with open(file, 'a') as logfile:
            logfile.write(f'\n\n{mode}\n\n')

        if not args.quiet:
            time.sleep(5)
            os.system('tput clear')
            os.system(f'echo "-*- $({blue})Cleanup$({reset}) -*-"; echo ;')

        subprocess.run(
            ['bash', './cleanup.sh', date, 'reinstall', 'false', 'true', quiet, verbose]
        )

    if not args.quiet:
        time.sleep(5)
        os.system('tput clear')
    return log if retset else dict(cask=log)


def reinstall_all(args, *, file, date):
    quiet = str(args.quiet).lower()
    verbose = str(args.verbose).lower()

    log = dict(
        brew = reinstall_brew(args, cleanup=False, retset=True, file=file, date=date),
        cask = reinstall_cask(args, cleanup=False, retset=True, file=file, date=date),
    )

    mode = '-*- Cleanup -*-'.center(80, ' ')
    with open(file, 'a') as logfile:
        logfile.write(f'\n\n{mode}\n\n')

    if not args.quiet:
        time.sleep(5)
        os.system('tput clear')
        os.system(f'echo "-*- $({blue})Cleanup$({reset}) -*-"; echo ;')

    subprocess.run(
        ['bash', './cleanup.sh', date, 'reinstall', 'true', 'true', quiet, verbose]
    )

    if not args.quiet:
        time.sleep(5)
        os.system('tput clear')
    return log


def postinstall(args, *, file, date, cleanup=True):
    quiet = str(args.quiet).lower()
    verbose = str(args.verbose).lower()
    start = str(args.start).lower()
    end = str(args.end).lower()
    packages = _merge_packages(args, mode='postinstall')

    if shutil.which('brew') is None:
        os.system(f'''
                echo "$({red})brew$({reset}): Command not found.";
                echo "You may find Homebrew on $({under})https://brew.sh$({reset}), or install Homebrew through following command:"
                echo $({bold})'/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"'$({reset})
        ''')
        return set() if retset else dict(brew=set())

    mode = '-*- Homebrew -*-'.center(80, ' ')
    with open(file, 'a') as logfile:
        logfile.write(f'\n\n{mode}\n\n')

    if not args.quiet:
        os.system(f'echo "-*- $({blue})Homebrew$({reset}) -*-"; echo ;')

    if ('all' in packages) or (args.start is not None) or (args.end is not None):
        logging = subprocess.run(
            ['bash', './logging_brew.sh', date, 'postinstall', start, end] + list(packages),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        log = set(logging.stdout.replace(b'\x1b', b'').decode().split())
    else:
        log = packages

    if log:
        subprocess.run(
            ['bash', './postinstall.sh', date, quiet, verbose] + list(log)
        )
    else:
        if not args.quiet:
            os.system(f'echo "$({green})No postinstallation performed.$({reset})"; echo ;')
        with open(file, 'a') as logfile:
            logfile.write('INF: No postinstallation performed.\n')

    if cleanup:
        mode = '-*- Cleanup -*-'.center(80, ' ')
        with open(file, 'a') as logfile:
            logfile.write(f'\n\n{mode}\n\n')

        if not args.quiet:
            time.sleep(5)
            os.system('tput clear')
            os.system(f'echo "-*- $({blue})Cleanup$({reset}) -*-"; echo ;')

        subprocess.run(
            ['bash', './cleanup.sh', date, 'postinstall', 'true', 'false', quiet, verbose]
        )

    if not args.quiet:
        time.sleep(5)
        os.system('tput clear')
    return log
