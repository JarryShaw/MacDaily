#!/usr/bin/python3
# -*- coding: utf-8 -*-


import json
import os
import re
import shlex
import shutil
import subprocess
import time


__all__ = [
    'update_all', 'update_apm', 'update_npm', 'update_pip',
    'update_brew', 'update_cask', 'update_cleanup', 'update_appstore'
]


# terminal display
red = 'tput setaf 1'    # blush / red
blue = 'tput setaf 14'  # blue
bold = 'tput bold'      # bold
under = 'tput smul'     # underline
reset = 'tput sgr0'     # reset


def _merge_packages(args):
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
    elif 'all' in args.mode:
        packages = {'all'}
    else:
        packages = {'null'}
    return packages


def update_cleanup(args, *, file, date, brew=False, cask=False):
    brew = str((not args.brew) if 'cleanup' in args.mode else brew).lower()
    cask = str((not args.cask) if 'cleanup' in args.mode else cask).lower()
    quiet = str(args.quiet).lower()

    mode = '-*- Cleanup -*-'.center(80, ' ')
    with open(file, 'a') as logfile:
        logfile.write(f'\n\n{mode}\n\n')

    if not args.quiet:
        os.system(f'echo "-*- $({blue})Cleanup$({reset}) -*-"; echo ;')

    subprocess.run(
        ['bash', 'libupdate/cleanup.sh', date, brew, cask, quiet]
    )

    if not args.quiet:
        time.sleep(5)
        os.system('tput clear')


def update_apm(args, *, file, date, retset=False):
    if shutil.which('apm') is None:
        os.system(f'''
                echo "update: $({red})apm$({reset}): command not found";
                echo "You may download Atom from $({under})https://atom.io$({reset}).";
        ''')
        return set() if retset else dict(apm=set())

    quiet = str(args.quiet).lower()
    verbose = str(args.verbose).lower()
    packages = _merge_packages(args)

    mode = '-*- Atom -*-'.center(80, ' ')
    with open(file, 'a') as logfile:
        logfile.write(f'\n\n{mode}\n\n')

    if not args.quiet:
        os.system(f'echo "-*- $({blue})Atom$({reset}) -*-"; echo ;')

    if 'all' in packages:
        logging = subprocess.run(
            ['bash', 'libupdate/logging_apm.sh', date],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        log = set(logging.stdout.decode().split())
        outdated = 'true' if logging.stdout.decode() else 'false'
    else:
        log = packages
        outdated = 'true'

    subprocess.run(
        ['bash', 'libupdate/update_apm.sh', date, quiet, verbose, outdated] + list(log)
    )

    if not args.quiet:
        time.sleep(5)
        os.system('tput clear')
    return log if retset else dict(apm=log)


def update_npm(args, *, file, date, retset=False):
    if shutil.which('npm') is None:
        os.system(f'''
                echo "update: $({red})npm$({reset}): command not found";
                echo "You may download Node.js from $({under})https://nodejs.org/$({reset}).";
        ''')
        return set() if retset else dict(apm=set())

    quiet = str(args.quiet).lower()
    verbose = str(args.verbose).lower()
    packages = _merge_packages(args)

    mode = '-*- Node.js -*-'.center(80, ' ')
    with open(file, 'a') as logfile:
        logfile.write(f'\n\n{mode}\n\n')

    if not args.quiet:
        os.system(f'echo "-*- $({blue})Node.js$({reset}) -*-"; echo ;')

    if 'all' in packages:
        logging = subprocess.run(
            ['bash', 'libupdate/logging_npm.sh', date],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout = json.loads(logging.stdout.decode())
        log = set(stdout.keys())
        pkg = { f'{name}@{value["wanted"]}' for name, value in stdout.items() }
        outdated = 'true' if stdout else 'false'
    else:
        log = pkg = packages
        outdated = 'true'

    subprocess.run(
        ['bash', 'libupdate/update_npm.sh', date, quiet, verbose, outdated] + list(pkg)
    )

    if not args.quiet:
        time.sleep(5)
        os.system('tput clear')
    return log if retset else dict(npm=log)


def update_pip(args, *, file, date, retset=False):
    quiet = str(args.quiet).lower()
    verbose = str(args.verbose).lower()
    packages = _merge_packages(args)

    mode = '-*- Python -*-'.center(80, ' ')
    with open(file, 'a') as logfile:
        logfile.write(f'\n\n{mode}\n\n')

    if not args.quiet:
        os.system(f'echo "-*- $({blue})Python$({reset}) -*-"; echo ;')

    flag = ('all' in args.mode) or args.all or (args.version == 1 or not any((args.system, args.brew, args.cpython, args.pypy)))
    if ('all' in packages and flag) or args.package is not None:
        system, brew, cpython, pypy, version = 'true', 'true', 'true', 'true', '1'
    else:
        system, brew, cpython, pypy, version = \
            str(args.system).lower(), str(args.brew).lower(), \
            str(args.cpython).lower(), str(args.pypy).lower(), str(args.version or 1)

    logging = subprocess.run(
        ['bash', 'libupdate/logging_pip.sh', date, system, brew, cpython, pypy, version] + list(packages),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    log = set(logging.stdout.decode().split())

    subprocess.run(
        ['sudo', '-H', 'bash', 'libupdate/update_pip.sh', date, system, brew, cpython, pypy, version, quiet, verbose] + list(packages)
    )
    subprocess.run(
        ['bash', 'libupdate/relink_pip.sh'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    if not args.quiet:
        time.sleep(5)
        os.system('tput clear')
    return log if retset else dict(pip=log)


def update_brew(args, *, file, date, cleanup=True, retset=False):
    if shutil.which('brew') is None:
        os.system(f'''
                echo "update: $({red})brew$({reset}): command not found";
                echo "You may find Homebrew on $({under})https://brew.sh$({reset}), or install Homebrew through following command:";
                echo $({bold})'/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"'$({reset});
        ''')
        return set() if retset else dict(brew=set())

    quiet = str(args.quiet).lower()
    verbose = str(args.verbose).lower()
    force = str(args.force).lower()
    merge = str(args.merge).lower()
    packages = _merge_packages(args)

    mode = '-*- Homebrew -*-'.center(80, ' ')
    with open(file, 'a') as logfile:
        logfile.write(f'\n\n{mode}\n\n')

    if not args.quiet:
        os.system(f'echo "-*- $({blue})Homebrew$({reset}) -*-"; echo ;')

    subprocess.run(
        ['bash', 'libupdate/renew_brew.sh', date, quiet, verbose, force, merge]
    )

    if 'all' in packages:
        logging = subprocess.run(
            ['bash', 'libupdate/logging_brew.sh', date],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        log = set(logging.stdout.decode().split())
        outdated = 'true' if logging.stdout.decode() else 'false'
    else:
        log = packages
        outdated = 'true'

    subprocess.run(
        ['bash', 'libupdate/update_brew.sh', date, quiet, verbose, outdated] + list(log)
    )

    if not args.quiet:
        time.sleep(5)
        os.system('tput clear')
    if not retset and not args.no_cleanup:
        update_cleanup(args, file=file, date=date, brew=True)
    return log if retset else dict(brew=log)


def update_cask(args, *, file, date, cleanup=True, retset=False):
    testing = subprocess.run(
        shlex.split('brew cask'),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    if testing.returncode:
        os.system(f'''
                echo "update: $({red})cask$({reset}): command not found";
                echo "You may find Caskroom on $({under})https://caskroom.github.io$({reset}), or install Caskroom through following command:"
                echo $({bold})'brew tap caskroom/cask'$({reset})
        ''')
        return set() if retset else dict(cask=set())

    quiet = str(args.quiet).lower()
    verbose = str(args.verbose).lower()
    force = str(args.force).lower()
    greedy = str(args.greedy).lower()
    packages = _merge_packages(args)

    mode = '-*- Caskroom -*-'.center(80, ' ')
    with open(file, 'a') as logfile:
        logfile.write(f'\n\n{mode}\n\n')

    if not args.quiet:
        os.system(f'echo "-*- $({blue})Caskroom$({reset}) -*-"; echo ;')

    if 'all' in packages:
        logging = subprocess.run(
            ['bash', 'libupdate/logging_cask.sh', date, greedy],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        log = set(logging.stdout.decode().split())
        outdated = 'true' if log else 'false'
    else:
        log = packages
        outdated = 'true'

    subprocess.run(
        ['bash', 'libupdate/update_cask.sh', date, quiet, verbose, force, greedy, outdated] + list(log)
    )

    if not args.quiet:
        time.sleep(5)
        os.system('tput clear')
    if not retset and not args.no_cleanup:
        update_cleanup(args, file=file, date=date, cask=True)
    return log if retset else dict(cask=log)


def update_appstore(args, *, file, date, retset=False):
    if shutil.which('softwareupdate') is None:
        os.system(f'echo "update: $({red})appstore$({reset}): command not found"')
        return set() if retset else dict(appstore=set())

    quiet = str(args.quiet).lower()
    verbose = str(args.verbose).lower()
    packages = _merge_packages(args)

    mode = '-*- App Store -*-'.center(80, ' ')
    with open(file, 'a') as logfile:
        logfile.write(f'\n\n{mode}\n\n')

    if not args.quiet:
        os.system(f'echo "-*- $({blue})App Store$({reset}) -*-"; echo ;')

    logging = subprocess.run(
        ['bash', 'libupdate/logging_appstore.sh', date],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    if 'all' in packages:
        log = set(re.split('[\n\r]', logging.stdout.decode().strip()))
        outdated = 'true' if log else 'false'
    else:
        log = packages
        outdated = 'true'

    subprocess.run(
        ['sudo', 'bash', 'libupdate/update_appstore.sh', date, quiet, verbose, outdated] + list(packages)
    )

    if not args.quiet:
        time.sleep(5)
        os.system('tput clear')
    return log if retset else dict(appstore=log)


def update_all(args, *, file, date):
    log = dict(
        apm = set(),
        npm = set(),
        pip = set(),
        brew = set(),
        cask = set(),
        appstore = set(),
    )
    for mode in ('apm', 'npm', 'pip', 'brew', 'cask', 'appstore'):
        if not args.__getattribute__(f'no_{mode}'):
            log[mode] = eval(f'update_{mode}')(args, retset=True, file=file, date=date)

    if not args.no_cleanup:
        update_cleanup(args, file=file, date=date, brew=True, cask=True)
    return log
