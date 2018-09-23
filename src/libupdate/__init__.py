# -*- coding: utf-8 -*-

import collections
import datetime
import json
import os
import re
import shlex
import shutil
import signal
import subprocess
import sys

from macdaily.daily_utility import (blue, blush, bold, flash, make_mode,
                                    purple, red, reset, under)

__all__ = [
    'update_all', 'update_apm', 'update_mas', 'update_npm', 'update_gem',
    'update_pip', 'update_brew', 'update_cask', 'update_cleanup', 'update_system'
]

# root path
ROOT = os.path.dirname(os.path.abspath(__file__))

# brew renewed time
BREW_RENEW = None


def _merge_packages(args):
    packages = list()
    if 'package' in args and args.package:
        for pkg in map(lambda s: re.split(r'\W*,\W*', s), args.package):
            if 'all' in pkg:
                setattr(args, 'all', True)
                packages = {'all'}
                break
            packages.extend(pkg)
    elif 'all' in args.mode or args.all:
        packages = {'all'}
    return set(packages)


def update_all(args, file, temp, disk, password, bash_timeout, sudo_timeout):
    glb = globals()
    log = collections.defaultdict(set)
    for mode in {'apm', 'gem', 'mas', 'npm', 'pip', 'brew', 'cask', 'system'}:
        glb[mode] = False
        if not getattr(args, 'no_{}'.format(mode)):
            glb[mode] = True
            log[mode] = eval('update_{}'.format(mode))(args, file=file, temp=temp, disk=disk, retset=True,
                                               password=password, bash_timeout=bash_timeout, sudo_timeout=sudo_timeout)

    if not args.no_cleanup:
        update_cleanup(args, file=file, temp=temp, disk=disk, retset=True, gem=gem, npm=npm, pip=pip,
                       brew=brew, cask=cask, password=password, bash_timeout=bash_timeout, sudo_timeout=sudo_timeout)
    return log


def update_apm(args, file, temp, disk, password, bash_timeout, sudo_timeout, retset=False):
    if shutil.which('apm') is None:
        print('update: {}{}apm{}: command not found\n'
              'update: {}apm{}: you may download Atom from {}{}https://atom.io{}\n'.format(blush, flash, reset, red, reset, purple, under, reset),
              file=sys.stderr)
        return set() if retset else dict(apm=set())

    logname = shlex.quote(file)
    tmpname = shlex.quote(temp)
    quiet = str(args.quiet).lower()
    verbose = str(args.verbose).lower()
    yes = str(args.yes).lower()
    packages = _merge_packages(args)

    make_mode(args, file, 'Atom')
    if 'all' in packages or args.all:
        logging = subprocess.run(['bash', os.path.join(ROOT, 'logging_apm.sh'), logname, tmpname],
                                 stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=bash_timeout)
        log = set(re.sub(r'\^D\x08\x08', '', logging.stdout.decode().strip(), re.IGNORECASE).split())
        outdated = 'true' if log and all(log) else 'false'
    else:
        log = packages
        outdated = 'true'

    subprocess.run(['bash', os.path.join(ROOT, 'update_apm.sh'),
                   logname, tmpname, quiet, verbose, outdated, yes] + list(log), timeout=bash_timeout)

    (lambda: None if args.quiet else print())()
    return log if retset else dict(apm=log)


def update_gem(args, file, temp, disk, password, bash_timeout, sudo_timeout, cleanup=True, retset=False):
    if shutil.which('gem') is None:
        print('update: {}{}gem{}: command not found\n'
              'update: {}gem{}: you may download Ruby from '
              '{}{}https://www.ruby-lang.org/{}\n'.format(blush, flash, reset, red, reset, purple, under, reset), file=sys.stderr)
        return set() if retset else dict(gem=set())

    logname = shlex.quote(file)
    tmpname = shlex.quote(temp)
    quiet = str(args.quiet).lower()
    verbose = str(args.verbose).lower()
    yes = str(args.yes).lower()
    packages = _merge_packages(args)

    make_mode(args, file, 'Ruby')
    if 'all' in packages or args.all:
        logging = subprocess.run(['bash', os.path.join(ROOT, 'logging_gem.sh'), logname, tmpname],
                                 stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=bash_timeout)
        log = set(re.sub(r'\^D\x08\x08', '', logging.stdout.decode().strip(), re.IGNORECASE).split())
        outdated = 'true' if log and all(log) else 'false'
    else:
        log = packages
        outdated = 'true'

    subprocess.run(['bash', os.path.join(ROOT, 'update_gem.sh'), password, sudo_timeout,
                   logname, tmpname, quiet, verbose, yes, outdated] + list(log), timeout=bash_timeout)

    (lambda: None if args.quiet else print())()
    if not retset and not args.no_cleanup:
        update_cleanup(args, file=file, temp=temp, disk=disk, gem=True,
                       password=password, bash_timeout=bash_timeout, sudo_timeout=sudo_timeout)
    return log if retset else dict(gem=log)


def update_mas(args, file, temp, disk, password, bash_timeout, sudo_timeout, retset=False):
    if shutil.which('mas') is None:
        print('update: {}{}mas{}: command not found\n'
              'update: {}cask{}: you may download MAS through following command -- '
              '`{}brew install mas{}`\n'.format(blush, flash, reset, red, reset, bold, reset), file=sys.stderr)
        return set() if retset else dict(mas=set())

    logname = shlex.quote(file)
    tmpname = shlex.quote(temp)
    quiet = str(args.quiet).lower()
    verbose = str(args.verbose).lower()
    packages = _merge_packages(args)

    make_mode(args, file, 'Mac App Store')
    logging = subprocess.run(['bash', os.path.join(ROOT, 'logging_mas.sh'), logname, tmpname],
                             stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=bash_timeout)
    if 'all' in packages or args.all:
        log = set(re.split(r'[\r\n]', re.sub(r'\^D\x08\x08', '', logging.stdout.decode().strip(), re.IGNORECASE)))
        outdated = 'true' if log and all(log) else 'false'
    else:
        log = packages
        outdated = 'true'

    subprocess.run(['bash', os.path.join(ROOT, 'update_mas.sh'), password, sudo_timeout,
                   logname, tmpname, quiet, verbose, outdated] + list(packages), timeout=bash_timeout)

    (lambda: None if args.quiet else print())()
    return log if retset else dict(mas=log)


def update_npm(args, file, temp, disk, password, bash_timeout, sudo_timeout, cleanup=True, retset=False):
    if shutil.which('npm') is None:
        print('update: {}{}npm{}: command not found\n'
              'update: {}npm{}: you may download Node.js from '
              '{}{}https://nodejs.org/{}\n'.format(blush, flash, reset, red, reset, purple, under, reset), file=sys.stderr)
        return set() if retset else dict(npm=set())

    logname = shlex.quote(file)
    tmpname = shlex.quote(temp)
    quiet = str(args.quiet).lower()
    verbose = str(args.verbose).lower()
    packages = _merge_packages(args)

    make_mode(args, file, 'Node.js')
    if 'all' in packages or args.all:
        allflag = 'true'
        logging = subprocess.run(['bash', os.path.join(ROOT, 'logging_npm.sh'), logname, tmpname],
                                 stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=bash_timeout)
        start = logging.stdout.find(b'{')
        end = logging.stdout.rfind(b'}')
        if start == -1 or end == -1:
            stdict = dict()
        else:
            stdict = json.loads(re.sub(r'\^D\x08\x08', '', logging.stdout[start:end+1].decode().strip(), re.IGNORECASE))
        log = set(stdict.keys())
        pkg = {'{}@{}'.format(name, value["wanted"]) for name, value in stdict.items()}
        outdated = 'true' if log and all(log) else 'false'
    else:
        allflag = 'false'
        log = pkg = packages
        outdated = 'true'

    subprocess.run(['bash', os.path.join(ROOT, 'update_npm.sh'), password, sudo_timeout,
                   logname, tmpname, allflag, quiet, verbose, outdated] + list(pkg), timeout=bash_timeout)

    (lambda: None if args.quiet else print())()
    if not retset and not args.no_cleanup:
        update_cleanup(args, file=file, temp=temp, disk=disk, npm=True,
                       password=password, bash_timeout=bash_timeout, sudo_timeout=sudo_timeout)
    return log if retset else dict(npm=log)


def update_pip(args, file, temp, disk, password, bash_timeout, sudo_timeout, cleanup=True, retset=False):
    logname = shlex.quote(file)
    tmpname = shlex.quote(temp)
    quiet = str(args.quiet).lower()
    verbose = str(args.verbose).lower()
    yes = str(args.yes).lower()
    pre = str(args.pre).lower()
    packages = _merge_packages(args)

    make_mode(args, file, 'Python')
    flag = not ('pip' in args.mode and any((args.version, args.system, args.brew, args.cpython, args.pypy)))
    if flag and packages:
        system, brew, cpython, pypy, version = 'true', 'true', 'true', 'true', '1'
    else:
        system, brew, cpython, pypy, version = \
            str(args.system).lower(), str(args.brew).lower(), \
            str(args.cpython).lower(), str(args.pypy).lower(), str(args.version)

    logging = subprocess.run(['bash', os.path.join(ROOT, 'logging_pip.sh'), logname, tmpname,
                              system, brew, cpython, pypy, version, pre] + list(packages),
                             stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=bash_timeout)
    log = set(re.sub(r'\^D\x08\x08', '', logging.stdout.decode().strip(), re.IGNORECASE).split())
    if 'macdaily' in log:
        os.kill(os.getpid(), signal.SIGUSR1)

    subprocess.run(['bash', os.path.join(ROOT, 'update_pip.sh'), password, sudo_timeout,
                    logname, tmpname, system, brew, cpython, pypy, version,
                    yes, quiet, verbose, pre] + list(packages), timeout=bash_timeout)
    subprocess.run(['bash', os.path.join(ROOT, 'relink_pip.sh')],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=bash_timeout)

    (lambda: None if args.quiet else print())()
    if not retset and not args.no_cleanup:
        update_cleanup(args, file=file, temp=temp, disk=disk, pip=True,
                       password=password, bash_timeout=bash_timeout, sudo_timeout=sudo_timeout)
    return log if retset else dict(pip=log)


def update_brew(args, file, temp, disk, password, bash_timeout, sudo_timeout, cleanup=True, retset=False):
    if shutil.which('brew') is None:
        print('update: {}{}brew{}: command not found\n'
              'update: {}brew{}: you may find Homebrew on {}{}https://brew.sh{}, '
              'or install Homebrew through following command -- `{}/usr/bin/ruby -e '
              '"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"{}`\n'.format(blush, flash, reset, red, reset, purple, under, reset, bold, reset),
              file=sys.stderr)
        return set() if retset else dict(brew=set())

    logname = shlex.quote(file)
    tmpname = shlex.quote(temp)
    quiet = str(args.quiet).lower()
    verbose = str(args.verbose).lower()
    force = str(args.force).lower()
    merge = str(args.merge).lower()
    packages = _merge_packages(args)

    make_mode(args, file, 'Homebrew')
    global BREW_RENEW
    if BREW_RENEW is None or (datetime.datetime.now() - BREW_RENEW).total_seconds() > 300:
        subprocess.run(['bash', os.path.join(ROOT, 'renew_brew.sh'), logname, tmpname,
                        quiet, verbose, force, merge], timeout=bash_timeout)
        BREW_RENEW = datetime.datetime.now()

    if 'all' in packages or args.all:
        logging = subprocess.run(['bash', os.path.join(ROOT, 'logging_brew.sh'), logname, tmpname],
                                 stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=bash_timeout)
        log = set(re.sub(r'\^D\x08\x08', '', logging.stdout.decode().strip(), re.IGNORECASE).split())
        outdated = 'true' if log and all(log) else 'false'
    else:
        log = packages
        outdated = 'true'

    subprocess.run(['bash', os.path.join(ROOT, 'update_brew.sh'), password, sudo_timeout,
                   logname, tmpname, quiet, verbose, outdated] + list(log), timeout=bash_timeout)

    (lambda: None if args.quiet else print())()
    if not retset and not args.no_cleanup:
        update_cleanup(args, file=file, temp=temp, disk=disk, brew=True,
                       password=password, bash_timeout=bash_timeout, sudo_timeout=sudo_timeout)
    return log if retset else dict(brew=log)


def update_cask(args, file, temp, disk, password, bash_timeout, sudo_timeout, cleanup=True, retset=False):
    testing = subprocess.run(['brew', 'command', 'cask'],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if testing.returncode != 0:
        print('update: {}{}cask{}: command not found\n'
              'update: {}cask{}: you may find Caskroom on '
              '{}{}https://caskroom.github.io{}, '
              'or install Caskroom through following command -- '
              '`{}brew tap homebrew/cask{}`\n'.format(blush, flash, reset, red, reset, purple, under, reset, bold, reset), file=sys.stderr)
        return set() if retset else dict(cask=set())

    logname = shlex.quote(file)
    tmpname = shlex.quote(temp)
    quiet = str(args.quiet).lower()
    verbose = str(args.verbose).lower()
    force = str(args.force).lower()
    merge = str(args.merge).lower()
    greedy = str(args.greedy).lower()
    packages = _merge_packages(args)

    make_mode(args, file, 'Caskroom')
    global BREW_RENEW
    if BREW_RENEW is None or (datetime.datetime.now() - BREW_RENEW).total_seconds() > 300:
        subprocess.run(['bash', os.path.join(ROOT, 'renew_brew.sh'), logname, tmpname,
                        quiet, verbose, force, merge], timeout=bash_timeout)
        BREW_RENEW = datetime.datetime.now()

    if 'all' in packages or args.all:
        logging = subprocess.run(['bash', os.path.join(ROOT, 'logging_cask.sh'), logname, tmpname, greedy, force],
                                 stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=bash_timeout)
        log = set(re.sub(r'\^D\x08\x08', '', logging.stdout.decode().strip(), re.IGNORECASE).split())
        outdated = 'true' if log and all(log) else 'false'
    else:
        log = packages
        outdated = 'true'

    subprocess.run(['bash', os.path.join(ROOT, 'update_cask.sh'), password, sudo_timeout,
                   logname, tmpname, quiet, verbose, force, greedy, outdated] + list(log), timeout=bash_timeout)

    (lambda: None if args.quiet else print())()
    if not retset and not args.no_cleanup:
        update_cleanup(args, file=file, temp=temp, disk=disk, cask=True,
                       password=password, bash_timeout=bash_timeout, sudo_timeout=sudo_timeout)
    return log if retset else dict(cask=log)


def update_system(args, file, temp, disk, password, bash_timeout, sudo_timeout, retset=False):
    if shutil.which('softwareupdate') is None:
        print('update: {}{}system{}: command not found\n'
              "update: {}system{}: you may add `softwareupdate' to $PATH through the following command -- "
              "`{}echo export PATH='/usr/sbin:$PATH' >> ~/.bash_profile{}'\n".format(blush, flash, reset, red, reset, bold, reset), file=sys.stderr)
        return set() if retset else dict(system=set())

    logname = shlex.quote(file)
    tmpname = shlex.quote(temp)
    quiet = str(args.quiet).lower()
    verbose = str(args.verbose).lower()
    restart = str(args.restart).lower()
    packages = _merge_packages(args)

    make_mode(args, file, 'System')
    logging = subprocess.run(['bash', os.path.join(ROOT, 'logging_system.sh'), logname, tmpname],
                             stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=bash_timeout)
    if 'all' in packages or args.all:
        log = set(re.split(r'[\n\r]', re.sub(r'\^D\x08\x08', '', logging.stdout.decode().strip(), re.IGNORECASE)))
        outdated = 'true' if log and all(log) else 'false'
    else:
        log = packages
        outdated = 'true'

    subprocess.run(['bash', os.path.join(ROOT, 'update_system.sh'), password, sudo_timeout,
                   logname, tmpname, quiet, verbose, restart, outdated] + list(packages), timeout=bash_timeout)

    (lambda: None if args.quiet else print())()
    return log if retset else dict(system=log)


def update_cleanup(args, file, temp, disk, password, bash_timeout, sudo_timeout,
                   gem=False, npm=False, pip=False, brew=False, cask=False, retset=False):
    logname = shlex.quote(file)
    tmpname = shlex.quote(temp)
    dskname = shlex.quote(disk)

    gem = str(args.gem if 'cleanup' in args.mode else gem).lower()
    npm = str(args.npm if 'cleanup' in args.mode else npm).lower()
    pip = str(args.pip if 'cleanup' in args.mode else pip).lower()
    brew = str(args.brew if 'cleanup' in args.mode else brew).lower()
    cask = str(args.cask if 'cleanup' in args.mode else cask).lower()
    quiet = str(args.quiet).lower()

    make_mode(args, file, 'Cleanup', flag=any((gem, npm, pip, brew, cask)))
    subprocess.run(['bash', os.path.join(ROOT, 'cleanup.sh'), password, sudo_timeout,
                   logname, tmpname, dskname, gem, npm, pip, brew, cask, quiet], timeout=bash_timeout)

    (lambda: None if args.quiet else print())()
    return set() if retset else dict(cleanup=set())
