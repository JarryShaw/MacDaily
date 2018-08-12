# -*- coding: utf-8 -*-


import collections
import getpass
import os
import shlex
import shutil
import subprocess


__all__ = ['uninstall_all', 'uninstall_pip', 'uninstall_brew', 'uninstall_cask']


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
    elif 'all' in args.mode or args.all:
        packages = {'all'}
    else:
        packages = {'null'}
    return packages


def uninstall_all(args, *, file, temp):
    log = collections.defaultdict(set)
    for mode in {'pip', 'brew', 'cask'}:
        if not getattr(args, f'no_{mode}'):
            log[mode] = eval(f'uninstall_{mode}')(args, file=file, temp=temp, retset=True)
    return log


def uninstall_pip(args, *, file, temp, retset=False):
    logname = shlex.quote(file)
    tmpname = shlex.quote(temp)
    quiet = str(args.quiet).lower()
    verbose = str(args.verbose).lower()
    yes = str(args.yes).lower()
    idep = str(args.idep).lower()
    packages = _merge_packages(args)

    mode = '-*- Python -*-'.center(80, ' ')
    with open(file, 'a') as logfile:
        logfile.write(f'\n\n{mode}\n\n')
    if not args.quiet:
        print(f'-*- {blue}Python{reset} -*-\n')

    if 'null' in packages:
        log = set()
        with open(file, 'a') as logfile:
            logfile.write('INF: no uninstallation performed\n')
        if not args.quiet:
            print(f'uninstall: ${green}pip${reset}: no uninstallation performed\n')
    else:
        flag = not ('pip' in args.mode and any((args.version, args.system, args.brew, args.cpython, args.pypy)))
        if flag and packages:
            system, brew, cpython, pypy, version = 'true', 'true', 'true', 'true', '1'
        else:
            system, brew, cpython, pypy, version = \
                str(args.system).lower(), str(args.brew).lower(), \
                str(args.cpython).lower(), str(args.pypy).lower(), str(args.version)

        logging = subprocess.run(
            ['sudo', '--user', USER, '--set-home', 'bash', os.path.join(ROOT, 'logging_pip.sh'), logname, tmpname, system, brew, cpython, pypy, version, idep] + list(packages),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        log = set(logging.stdout.decode().strip().split())

        subprocess.run(
            ['sudo', '--user', USER, '--set-home', 'bash', os.path.join(ROOT, 'uninstall_pip.sh'), logname, tmpname, system, brew, cpython, pypy, version, verbose, quiet, yes, idep] + list(packages)
        )
        subprocess.run(
            ['sudo', '--user', USER, '--set-home', 'bash', os.path.join(ROOT, 'relink_pip.sh')],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
    if not args.quiet:  print()
    return log if retset else dict(pip=log)


def uninstall_brew(args, *, file, temp, retset=False):
    if shutil.which('brew') is None:
        print(
            f'uninstall: {blush}{flash}brew{reset}: command not found\n'
            f'uninstall: {red}brew{reset}: you may find Homebrew on {purple}{under}https://brew.sh{reset}, or install Homebrew through following command -- '
            f'`{bold}/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"{reset}`\n'
        )
        return set() if retset else dict(brew=set())

    logname = shlex.quote(file)
    tmpname = shlex.quote(temp)
    quiet = str(args.quiet).lower()
    verbose = str(args.verbose).lower()
    force = str(args.force).lower()
    yes = str(args.yes).lower()
    idep = str(args.idep).lower()
    packages = _merge_packages(args)

    mode = '-*- Homebrew -*-'.center(80, ' ')
    with open(file, 'a') as logfile:
        logfile.write(f'\n\n{mode}\n\n')
    if not args.quiet:
        print(f'-*- {blue}Homebrew{reset} -*-\n')

    if 'null' in packages:
        log = set()
        with open(file, 'a') as logfile:
            logfile.write('INF: no uninstallation performed\n')
        if not args.quiet:
            print(f'uninstall: ${green}brew${reset}: no uninstallation performed\n')
    else:
        logging = subprocess.run(
            ['sudo', '--user', USER, '--set-home', 'bash', os.path.join(ROOT, 'logging_brew.sh'), logname, tmpname, idep] + list(packages),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        log = set(logging.stdout.decode().strip().split())

        subprocess.run(
            ['sudo', '--user', USER, '--set-home', 'bash', os.path.join(ROOT, 'uninstall_brew.sh'), logname, tmpname, force, quiet, verbose, idep, yes] + list(packages)
        )
    if not args.quiet:  print()
    return log if retset else dict(brew=log)


def uninstall_cask(args, *, file, temp, retset=False):
    testing = subprocess.run(
        ['sudo', '--user', USER, '--set-home', 'brew', 'command', 'cask'],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    if testing.returncode:
        print(
            f'uninstall: {blush}{flash}cask{reset}: command not found\n'
            f'uninstall: {red}cask{reset}: you may find Caskroom on {under}https://caskroom.github.io{reset}, '
            f'or install Caskroom through following command -- `{bold}brew tap caskroom/cask{reset}`\n'
        )
        return set() if retset else dict(cask=set())

    logname = shlex.quote(file)
    tmpname = shlex.quote(temp)
    quiet = str(args.quiet).lower()
    verbose = str(args.verbose).lower()
    force = str(args.force).lower()
    packages = _merge_packages(args)

    mode = '-*- Caskroom -*-'.center(80, ' ')
    with open(file, 'a') as logfile:
        logfile.write(f'\n\n{mode}\n\n')
    if not args.quiet:
        print(f'-*- {blue}Caskroom{reset} -*-\n')

    if 'null' in packages:
        log = set()
        with open(file, 'a') as logfile:
            logfile.write('INF: no uninstallation performed\n')
        if not args.quiet:
            print(f'uninstall: ${green}cask${reset}: no uninstallation performed\n')
    else:
        logging = subprocess.run(
            ['sudo', '--user', USER, '--set-home', 'bash', os.path.join(ROOT, 'logging_cask.sh'), logname, tmpname] + list(packages),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        log = set(logging.stdout.decode().strip().split())

        subprocess.run(
            ['sudo', '--user', USER, '--set-home', 'bash', os.path.join(ROOT, 'uninstall_cask.sh'), logname, tmpname, quiet, verbose, force] + list(packages)
        )
    if not args.quiet:  print()
    return log if retset else dict(cask=log)
