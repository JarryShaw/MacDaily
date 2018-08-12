# -*- coding: utf-8 -*-


import collections
import getpass
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
green  = '\033[92m'     # bright green foreground
blue   = '\033[96m'     # bright blue foreground
blush  = '\033[101m'    # bright red background
purple = '\033[104m'    # bright purple background


# root path
ROOT = os.path.dirname(os.path.abspath(__file__))


# user name
USER = getpass.getuser()


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


def reinstall_all(args, *, file, temp, disk):
    glb = globals()
    log = collections.defaultdict(set)
    for mode in {'brew', 'cask'}:
        glb[mode] = False
        if not getattr(args, f'no_{mode}'):
            glb[mode] = True
            log[mode] = eval(f'reinstall_{mode}')(args, file=file, temp=temp, disk=disk, retset=True)

    if not args.no_cleanup:
        reinstall_cleanup(args, file=file, temp=temp, disk=disk, retset=True, brew=brew, cask=cask)
    return log


def reinstall_brew(args, *, file, temp, disk, cleanup=True, retset=False):
    if shutil.which('brew') is None:
        print(
            f'reinstall: {blush}{flash}brew{reset}: command not found\n'
            f'reinstall: {red}brew{reset}: you may find Homebrew on {purple}{under}https://brew.sh{reset}, or install Homebrew through following command -- '
            f'`{bold}/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"{reset}`\n'
        )
        return set() if retset else dict(brew=set())

    logname = shlex.quote(file)
    tmpname = shlex.quote(temp)
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
            ['sudo', '--user', USER, '--set-home', 'bash', os.path.join(ROOT, 'logging_brew.sh'), logname, tmpname, 'reinstall', start, end] + list(packages),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        log = set(logging.stdout.decode().strip().split())
        if (args.start is not None) or (args.end is not None):
            pkg = set(logging.stdout.decode().strip().split())
        else:
            pkg = packages

        if log and all(log):
            subprocess.run(
                ['sudo', '--user', USER, '--set-home', 'bash', os.path.join(ROOT, 'reinstall_brew.sh'), logname, tmpname, quiet, verbose, force] + list(pkg)
            )
        else:
            with open(file, 'a') as logfile:
                logfile.write('INF: no reinstallation performed\n')
            if not args.quiet:
                print(f'reinstall: ${green}brew${reset}: no reinstallation performed\n')

    if not args.quiet:  print()
    if not retset and not args.no_cleanup:
        reinstall_cleanup(args, file=file, temp=temp, disk=disk, brew=True, mode='reinstall')
    return log if retset else dict(brew=log)


def reinstall_cask(args, *, file, temp, disk, cleanup=True, retset=False):
    testing = subprocess.run(
        ['sudo', '--user', USER, '--set-home', 'brew', 'command', 'cask'],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    if testing.returncode:
        print(
            f'reinstall: {blush}{flash}cask{reset}: command not found\n'
            f'reinstall: {red}cask{reset}: you may find Caskroom on {under}https://caskroom.github.io{reset}, '
            f'or install Caskroom through following command -- `{bold}brew tap caskroom/cask{reset}`\n'
        )
        return set() if retset else dict(cask=set())

    logname = shlex.quote(file)
    tmpname = shlex.quote(temp)
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
            ['sudo', '--user', USER, '--set-home', 'bash', os.path.join(ROOT, 'logging_cask.sh'), logname, tmpname, 'reinstall', start, end] + list(packages),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        log = set(logging.stdout.decode().strip().split())
        if (args.start is not None) or (args.end is not None):
            pkg = set(logging.stdout.decode().strip().split())
        else:
            pkg = packages

        if log and all(log):
            subprocess.run(
                ['sudo', '--user', USER, '--set-home', 'bash', os.path.join(ROOT, 'reinstall_cask.sh'), logname, tmpname, quiet, verbose] + list(pkg)
            )
        else:
            with open(file, 'a') as logfile:
                logfile.write('INF: no reinstallation performed\n')
            if not args.quiet:
                print(f'reinstall: ${green}cask${reset}: no reinstallation performed\n')

    if not args.quiet:  print()
    if not retset and not args.no_cleanup:
        reinstall_cleanup(args, file=file, temp=temp, disk=disk, cask=True, mode='reinstall')
    return log if retset else dict(cask=log)


def reinstall_cleanup(args, *, file, temp, disk, mode, brew=False, cask=False, retset=False):
    logname = shlex.quote(file)
    tmpname = shlex.quote(temp)
    dskname = shlex.quote(disk)
    brew = str(args.brew if (mode == 'reinstall' and 'cleanup' in args.mode) else brew).lower()
    cask = str(args.cask if (mode == 'reinstall' and 'cleanup' in args.mode) else cask).lower()
    quiet = str(args.quiet).lower()

    mode = '-*- Cleanup -*-'.center(80, ' ')
    with open(file, 'a') as logfile:
        logfile.write(f'\n\n{mode}\n\n')
    if not args.quiet:
        print(f'-*- {blue}Cleanup{reset} -*-\n')

    subprocess.run(
        ['sudo', '--user', USER, '--set-home', 'bash', os.path.join(ROOT, 'cleanup.sh'), logname, tmpname, dskname, mode, brew, cask, quiet]
    )
    if not args.quiet:  print()
    return set() if retset else dict(cleanup=set())


def postinstall(args, *, file, temp, disk):
    if shutil.which('brew') is None:
        print(
            f'postinstall: {blush}{flash}brew{reset}: command not found\n'
            f'postinstall: {red}brew{reset}: you may find Homebrew on {purple}{under}https://brew.sh{reset}, or install Homebrew through following command -- '
            f'`{bold}/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"{reset}`\n'
        )
        return set() if retset else dict(brew=set())

    logname = shlex.quote(file)
    tmpname = shlex.quote(temp)
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

    if 'null' in packages:
        log = set()
        with open(file, 'a') as logfile:
            logfile.write('INF: no postinstallation performed\n')
        if not args.quiet:
            print(f'reinstall: ${green}brew${reset}: no postinstallation performed\n')
    else:
        logging = subprocess.run(
            ['sudo', '--user', USER, '--set-home', 'bash', os.path.join(ROOT, 'logging_brew.sh'), logname, tmpname, 'postinstall', start, end] + list(packages),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        log = set(logging.stdout.decode().strip().split())
        if (args.start is not None) or (args.end is not None):
            pkg = set(logging.stdout.decode().strip().split())
        else:
            pkg = packages

        if log and all(log):
            subprocess.run(
                ['sudo', '--user', USER, '--set-home', 'bash', os.path.join(ROOT, 'postinstall.sh'), logname, tmpname, quiet, verbose] + list(pkg)
            )
        else:
            with open(file, 'a') as logfile:
                logfile.write('INF: no postinstallation performed\n')
            if not args.quiet:
                print(f'reinstall: ${green}brew${reset}: no postinstallation performed\n')

    if not args.quiet:  print()
    if not args.no_cleanup:
        cleanup(args, file=file, temp=temp, disk=disk, brew=True, mode='postinstall')
    return log


cleanup = reinstall_cleanup
