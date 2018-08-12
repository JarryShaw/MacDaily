# -*- coding: utf-8 -*-


import collections
import getpass
import os
import shlex
import shutil
import subprocess


__all__ = ['dependency_all', 'dependency_pip', 'dependency_brew']


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


def dependency_all(args, *, file, temp):
    log = collections.defaultdict(set)
    for mode in {'pip', 'brew'}:
        if not getattr(args, f'no_{mode}'):
            log[mode] = eval(f'dependency_{mode}')(args, file=file, temp=temp, retset=True)
    return log


def dependency_pip(args, *, file, temp, retset=False):
    logname = shlex.quote(file)
    tmpname = shlex.quote(temp)
    tree = str(args.tree).lower()
    packages = _merge_packages(args)

    mode = '-*- Python -*-'.center(80, ' ')
    with open(file, 'a') as logfile:
        logfile.write(f'\n\n{mode}\n\n')
    print(f'-*- {blue}Python{reset} -*-\n')

    if 'null' in packages:
        log = set()
        with open(file, 'a') as logfile:
            logfile.write('INF: no dependency showed\n')
        print(f'dependency: {green}pip{reset}: no dependency showed\n')
    else:
        flag = not ('pip' in args.mode and any((args.version, args.system, args.brew, args.cpython, args.pypy)))
        if flag and packages:
            system, brew, cpython, pypy, version = 'true', 'true', 'true', 'true', '1'
        else:
            system, brew, cpython, pypy, version = \
                str(args.system).lower(), str(args.brew).lower(), \
                str(args.cpython).lower(), str(args.pypy).lower(), str(args.version)

        logging = subprocess.run(
            ['sudo', '--user', USER, '--set-home', 'bash', os.path.join(ROOT, 'logging_pip.sh'), logname, tmpname, system, brew, cpython, pypy, version] + list(packages),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        log = set(logging.stdout.decode().strip().split())

        subprocess.run(
            ['sudo', '--user', USER, '--set-home', 'bash', os.path.join(ROOT, 'dependency_pip.sh'), logname, tmpname, system, brew, cpython, pypy, version, tree] + list(packages)
        )
        subprocess.run(
            ['sudo', '--user', USER, '--set-home', 'bash', os.path.join(ROOT, 'relink_pip.sh')],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
    print()
    return log if retset else dict(pip=log)


def dependency_brew(args, *, file, temp, retset=False):
    if shutil.which('brew') is None:
        print(
            f'dependency: {blush}{flash}brew{reset}: command not found\n'
            f'dependency: {red}brew{reset}: you may find Homebrew on {purple}{under}https://brew.sh{reset}, or install Homebrew through following command -- '
            f'`{bold}/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"{reset}`\n'
        )
        return set() if retset else dict(brew=set())

    logname = shlex.quote(file)
    tmpname = shlex.quote(temp)
    tree = str(args.tree).lower()
    packages = _merge_packages(args)

    mode = '-*- Homebrew -*-'.center(80, ' ')
    with open(file, 'a') as logfile:
        logfile.write(f'\n\n{mode}\n\n')
    print(f'-*- {blue}Homebrew{reset} -*-\n')

    if 'null' in packages:
        log = set()
        with open(file, 'a') as logfile:
            logfile.write('INF: no dependency showed\n')
        print(f'dependency: ${green}brew${reset}: no uninstallation performed\n')
    else:
        logging = subprocess.run(
            ['sudo', '--user', USER, '--set-home', 'bash', os.path.join(ROOT, 'logging_brew.sh'), logname, tmpname] + list(packages),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        log = set(logging.stdout.decode().strip().split())

        subprocess.run(
            ['sudo', '--user', USER, '--set-home', 'bash', os.path.join(ROOT, 'dependency_brew.sh'), logname, tmpname, tree] + list(packages)
        )
    print()
    return log if retset else dict(brew=log)
