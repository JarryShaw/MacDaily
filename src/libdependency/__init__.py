# -*- coding: utf-8 -*-


import os
import shlex
import shutil
import subprocess
import time


# terminal display
red = 'tput setaf 1'    # blush / red
green = 'tput setaf 2'  # green
blue = 'tput setaf 14'  # blue
bold = 'tput bold'      # bold
under = 'tput smul'     # underline
reset = 'tput sgr0'     # reset


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
    elif 'all' in args.mode:
        packages = {'all'}
    else:
        packages = {'null'}
    return packages


def dependency_pip(args, *, file, date, retset=False):
    tree = str(args.tree).lower()
    packages = _merge_packages(args)

    mode = '-*- Python -*-'.center(80, ' ')
    with open(file, 'a') as logfile:
        logfile.write(f'\n\n{mode}\n\n')


    os.system(f'echo "-*- $({blue})Python$({reset}) -*-"; echo ;')
    if 'null' in packages:
        log = set()
        os.system(f'echo "dependency: $({green})pip$({reset}): no dependency showed"')
        with open(file, 'a') as logfile:
            logfile.write('INF: No dependency showed.\n')
    else:
        flag = ('all' in args.mode) or args.all or (args.version == 1 or not any((args.system, args.brew, args.cpython, args.pypy)))
        if ('all' in packages and flag) or args.package is not None:
            system, brew, cpython, pypy, version = 'true', 'true', 'true', 'true', '1'
        else:
            system, brew, cpython, pypy, version = \
                str(args.system).lower(), str(args.brew).lower(), \
                str(args.cpython).lower(), str(args.pypy).lower(), str(args.version or 1)

        logging = subprocess.run(
            ['bash', 'libdependency/logging_pip.sh', date, system, brew, cpython, pypy, version] + list(packages),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        log = set(logging.stdout.decode().split())

        subprocess.run(
            ['sudo', '-H', 'bash', 'libdependency/dependency_pip.sh', date, system, brew, cpython, pypy, version, tree] + list(packages)
        )
        subprocess.run(
            ['bash', 'libdependency/relink_pip.sh'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

    if retset:
        time.sleep(5)
        os.system('tput clear')
    return log if retset else dict(pip=log)


def dependency_brew(args, *, file, date, retset=False):
    if shutil.which('brew') is None:
        os.system(f'''
                echo "dependency: $({red})brew$({reset}): command not found";
                echo "You may find Homebrew on $({under})https://brew.sh$({reset}), or install Homebrew through following command:";
                echo $({bold})'/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"'$({reset})
        ''')
        return set() if retset else dict(brew=set())

    tree = str(args.tree).lower()
    packages = _merge_packages(args)

    mode = '-*- Homebrew -*-'.center(80, ' ')
    with open(file, 'a') as logfile:
        logfile.write(f'\n\n{mode}\n\n')

    os.system(f'echo "-*- $({blue})Homebrew$({reset}) -*-"; echo ;')
    if 'null' in packages:
        log = set()
        os.system(f'echo "dependency: $({green})pip$({reset}): no dependency showed"')
        with open(file, 'a') as logfile:
            logfile.write('INF: No dependency showed.\n')
    else:
        logging = subprocess.run(
            ['bash', 'libdependency/logging_brew.sh', date] + list(packages),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        log = set(logging.stdout.decode().split())

        subprocess.run(
            ['bash', 'libdependency/dependency_brew.sh', date, tree] + list(packages)
        )

    return log if retset else dict(brew=log)


def dependency_all(args, *, file, date):
    log = dict(
        pip = set(),
        brew = set(),
    )
    for mode in ('pip', 'brew'):
        if not args.__getattribute__(f'no_{mode}'):
            log[mode] = eval(f'dependency_{mode}')(args, retset=True, file=file, date=date)
    return log
