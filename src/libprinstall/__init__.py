# -*- coding: utf-8 -*-


import collections
import os
import shlex
import shutil
import subprocess


__all__ = ['reinstall_all', 'reinstall_brew', 'reinstall_cask', 'reinstall_cleanup']


# terminal display
reset  = '\033[0m'      # reset
bold   = '\033[1m'      # bold
under  = '\033[4m'      # underline
flash  = '\033[5m'      # flash
red    = '\033[91m'     # bright red foreground
blue   = '\033[96m'     # bright blue foreground
blush  = '\033[101m'    # bright red background
purple = '\033[104m'    # bright purple background


def _merge_packages(args, *, mode):
    if 'package' in args and args.package:
        allflag = False
        nullflag = False
        packages = set()
        for pkg in args.package:
            if allflag: break
            mapping = map(shlex.split, pkg.split(','))
            for list_ in mapping:
                if 'all' in list_:
                    packages = {'all'}
                    allflag = True; break
                if 'null' in list_:
                    packages = {'null'}
                    nullflag = True; break
                packages = packages.union(set(list_))
    elif mode == 'reinstall':
        if 'all' in args.mode or args.all:
            packages = {'all'}
        else:
            packages = {'null'}
    else:   # 'postinstall'
        if args.all:
            packages = {'all'}
        else:
            packages = {'null'}
    return packages


def reinstall_cleanup(args, *, file, date, time, mode, brew=False, cask=False):
    brew = str(args.brew if (mode == 'reinstall' and 'cleanup' in args.mode) else brew).lower()
    cask = str(args.cask if (mode == 'reinstall' and 'cleanup' in args.mode) else cask).lower()
    quiet = str(args.quiet).lower()

    mode = '-*- Cleanup -*-'.center(80, ' ')
    with open(file, 'a') as logfile:
        logfile.write(f'\n\n{mode}\n\n')
    if not args.quiet:
        print(f'-*- {blue}Cleanup{reset} -*-\n')

    subprocess.run(
        ['bash', 'libupdate/cleanup.sh', date, time, mode, brew, cask, quiet]
    )
    if not args.quiet:  print()
    return set() if retset else dict(cleanup=set())


def reinstall_brew(args, *, file, date, time, cleanup=True, retset=False):
    if shutil.which('brew') is None:
        print(
            f'reinstall: {blush}{flash}brew{reset}: command not found\n'
            f'reinstall: {red}brew{reset}: you may find Homebrew on {purple}{under}https://brew.sh{reset}, or install Homebrew through following command -- '
            f'`{bold}/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"{reset}`\n'
        )
        return set() if retset else dict(brew=set())

    quiet = str(args.quiet).lower()
    verbose = str(args.verbose).lower()
    force = str(args.force).lower()
    start = str(args.start).lower()
    end = str(args.end).lower()
    packages = _merge_packages(args, mode='reinstall')

    mode = '-*- Homebrew -*-'.center(80, ' ')
    with open(file, 'a') as logfile:
        logfile.write(f'\n\n{mode}\n\n')
    if not args.quiet:
        print(f'-*- {blue}Homebrew{reset} -*-\n')

    if 'null' in packages:
        log = set()
        with open(file, 'a') as logfile:
            logfile.write('INF: no reinstallation performed\n')
        if not args.quiet:
            print(f'reinstall: ${green}brew${reset}: no reinstallation performed\n')
    else:
        logging = subprocess.run(
            ['bash', 'libprinstall/logging_brew.sh', date, time, 'reinstall', start, end] + list(packages),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        log = set(logging.stdout.decode().strip().split())
        if (args.start is not None) or (args.end is not None):
            pkg = set(logging.stdout.decode().strip().split())
        else:
            pkg = packages

        if log and all(log):
            subprocess.run(
                ['bash', 'libprinstall/reinstall_brew.sh', date, time, quiet, verbose, force] + list(pkg)
            )
        else:
            with open(file, 'a') as logfile:
                logfile.write('INF: no reinstallation performed\n')
            if not args.quiet:
                print(f'reinstall: ${green}brew${reset}: no reinstallation performed\n')

    if not args.quiet:  print()
    if not retset and not args.no_cleanup:
        reinstall_cleanup(args, file=file, date=date, time=time, brew=True, mode='reinstall')
    return log if retset else dict(brew=log)


def reinstall_cask(args, *, file, date, time, cleanup=True, retset=False):
    testing = subprocess.run(
        shlex.split('brew cask'),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    if testing.returncode:
        print(
            f'reinstall: {blush}{flash}cask{reset}: command not found\n'
            f'reinstall: {red}cask{reset}: you may find Caskroom on {under}https://caskroom.github.io{reset}, '
            f'or install Caskroom through following command -- `{bold}brew tap caskroom/cask{reset}`\n'
        )
        return set() if retset else dict(cask=set())

    quiet = str(args.quiet).lower()
    verbose = str(args.verbose).lower()
    start = str(args.start).lower()
    end = str(args.end).lower()
    packages = _merge_packages(args, mode='reinstall')

    mode = '-*- Caskroom -*-'.center(80, ' ')
    with open(file, 'a') as logfile:
        logfile.write(f'\n\n{mode}\n\n')
    if not args.quiet:
        print(f'-*- {blue}Caskroom{reset} -*-\n')

    if 'null' in packages:
        log = set()
        with open(file, 'a') as logfile:
            logfile.write('INF: no reinstallation performed\n')
        if not args.quiet:
            print(f'reinstall: ${green}cask${reset}: no reinstallation performed\n')
    else:
        logging = subprocess.run(
            ['bash', 'libprinstall/logging_cask.sh', date, time, 'reinstall', start, end] + list(packages),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        log = set(logging.stdout.decode().strip().split())
        if (args.start is not None) or (args.end is not None):
            pkg = set(logging.stdout.decode().strip().split())
        else:
            pkg = packages

        if log and all(log):
            subprocess.run(
                ['bash', 'libprinstall/reinstall_cask.sh', date, time, quiet, verbose] + list(pkg)
            )
        else:
            with open(file, 'a') as logfile:
                logfile.write('INF: no reinstallation performed\n')
            if not args.quiet:
                print(f'reinstall: ${green}cask${reset}: no reinstallation performed\n')

    if not args.quiet:  print()
    if not retset and not args.no_cleanup:
        reinstall_cleanup(args, file=file, date=date, time=time, cask=True, mode='reinstall')
    return log if retset else dict(cask=log)


def reinstall_all(args, *, file, date):
    log = collections.defaultdict(set)
    for mode in ('brew', 'cask'):
        globals()[mode] = False
        if not args.__getattribute__(f'no_{mode}'):
            globals()[mode] = True
            log[mode] = eval(f'reinstall_{mode}')(args, retset=True, file=file, date=date, time=time)

    if not args.no_cleanup:
        update_cleanup(args, file=file, date=date, time=time, retset=True, brew=brew, cask=cask)
    return log


def postinstall(args, *, file, date):
    if shutil.which('brew') is None:
        print(
            f'postinstall: {blush}{flash}brew{reset}: command not found\n'
            f'postinstall: {red}brew{reset}: you may find Homebrew on {purple}{under}https://brew.sh{reset}, or install Homebrew through following command -- '
            f'`{bold}/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"{reset}`\n'
        )
        return set() if retset else dict(brew=set())

    quiet = str(args.quiet).lower()
    verbose = str(args.verbose).lower()
    start = str(args.start).lower()
    end = str(args.end).lower()
    packages = _merge_packages(args, mode='postinstall')

    mode = '-*- Homebrew -*-'.center(80, ' ')
    with open(file, 'a') as logfile:
        logfile.write(f'\n\n{mode}\n\n')
    if not args.quiet:
        print(f'-*- {blue}Homebrew{reset} -*-\n')

    if ('all' in packages) or (args.start is not None) or (args.end is not None):
        logging = subprocess.run(
            ['bash', 'libprinstall/logging_brew.sh', date, time, 'postinstall', start, end] + list(packages),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        log = set(logging.stdout.replace(b'\x1b', b'').decode().strip().split())
    else:
        log = packages

    if log and all(log):
        subprocess.run(
            ['bash', 'libprinstall/postinstall.sh', date, time, quiet, verbose] + list(log)
        )
    else:
        with open(file, 'a') as logfile:
            logfile.write('INF: no postinstallation performed\n')
        if not args.quiet:
            print(f'postinstall: ${green}brew${reset}: no postinstallation performed\n')

    if not args.quiet:  print()
    if not args.no_cleanup:
        reinstall_cleanup(args, file=file, date=date, time=time, brew=True, mode='postinstall')
    return log
