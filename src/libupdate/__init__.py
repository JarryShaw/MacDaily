# -*- coding: utf-8 -*-


import collections
import json
import os
import re
import shlex
import shutil
import signal
import subprocess


__all__ = [
    'update_all', 'update_apm', 'update_mas', 'update_npm', 'update_gem',
    'update_pip', 'update_brew', 'update_cask', 'update_cleanup', 'update_system'
]


# terminal display
reset  = '\033[0m'      # reset
bold   = '\033[1m'      # bold
under  = '\033[4m'      # underline
flash  = '\033[5m'      # flash
red    = '\033[91m'     # bright red foreground
blue   = '\033[96m'     # bright blue foreground
blush  = '\033[101m'    # bright red background
purple = '\033[104m'    # bright purple background


# root path
ROOT = os.path.dirname(os.path.abspath(__file__))


# brew renewed flag
BREW_RENEWED = False


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
    elif 'all' in args.mode or args.all:
        packages = {'all'}
    else:
        packages = set()
    return packages


def update_all(args, *, file, temp, disk, password):
    glb = globals()
    log = collections.defaultdict(set)
    for mode in {'apm', 'gem', 'mas', 'npm', 'pip', 'brew', 'cask', 'system'}:
        glb[mode] = False
        if not getattr(args, f'no_{mode}'):
            glb[mode] = True
            log[mode] = eval(f'update_{mode}')(args, file=file, temp=temp, disk=disk, password=password, retset=True)

    if not args.no_cleanup:
        update_cleanup(args, file=file, temp=temp, disk=disk, password=password, retset=True, gem=gem, npm=npm, pip=pip, brew=brew, cask=cask)
    return log


def update_apm(args, *, file, temp, disk, password, retset=False):
    if shutil.which('apm') is None:
        print(
            f'update: {blush}{flash}apm{reset}: command not found\n'
            f'update: {red}apm{reset}: you may download Atom from {purple}{under}https://atom.io{reset}\n'
        )
        return set() if retset else dict(apm=set())

    logname = shlex.quote(file)
    tmpname = shlex.quote(temp)
    quiet = str(args.quiet).lower()
    verbose = str(args.verbose).lower()
    yes = str(args.yes).lower()
    packages = _merge_packages(args)

    mode = '-*- Atom -*-'.center(80, ' ')
    with open(file, 'a') as logfile:
        logfile.write(f'\n\n{mode}\n\n')
    if not args.quiet:
        print(f'-*- {blue}Atom{reset} -*-\n')

    if 'all' in packages or args.all:
        logging = subprocess.run(
            ['bash', os.path.join(ROOT, 'logging_apm.sh'), logname, tmpname],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
        )
        log = set(logging.stdout.decode().strip().split())
        outdated = 'true' if log and all(log) else 'false'
    else:
        log = packages
        outdated = 'true'

    subprocess.run(
        ['bash', os.path.join(ROOT, 'update_apm.sh'), logname, tmpname, quiet, verbose, outdated, yes] + list(log),
    )
    if not args.quiet:  print()
    return log if retset else dict(apm=log)


def update_gem(args, *, file, temp, disk, password, cleanup=True, retset=False):
    if shutil.which('gem') is None:
        print(
            f'update: {blush}{flash}gem{reset}: command not found\n'
            f'update: {red}gem{reset}: you may download Ruby from {purple}{under}https://www.ruby-lang.org/{reset}\n'
        )
        return set() if retset else dict(gem=set())

    logname = shlex.quote(file)
    tmpname = shlex.quote(temp)
    quiet = str(args.quiet).lower()
    verbose = str(args.verbose).lower()
    yes = str(args.yes).lower()
    packages = _merge_packages(args)

    mode = '-*- Ruby -*-'.center(80, ' ')
    with open(file, 'a') as logfile:
        logfile.write(f'\n\n{mode}\n\n')
    if not args.quiet:
        print(f'-*- {blue}Ruby{reset} -*-\n')

    if 'all' in packages or args.all:
        logging = subprocess.run(
            ['bash', os.path.join(ROOT, 'logging_gem.sh'), logname, tmpname],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
        )
        log = set(logging.stdout.decode().strip().split())
        outdated = 'true' if log and all(log) else 'false'
    else:
        log = packages
        outdated = 'true'

    subprocess.run(
        ['bash', os.path.join(ROOT, 'update_gem.sh'), password, logname, tmpname, quiet, verbose, yes, outdated] + list(log)
    )
    if not args.quiet:  print()
    if not retset and not args.no_cleanup:
        update_cleanup(args, file=file, temp=temp, disk=disk, password=password, gem=True)
    return log if retset else dict(gem=log)


def update_mas(args, *, file, temp, disk, password, retset=False):
    if shutil.which('mas') is None:
        print(
            f'update: {blush}{flash}mas{reset}: command not found\n'
            f'update: {red}cask{reset}: you may download MAS through following command --`{bold}brew install mas{reset}`\n'
        )
        return set() if retset else dict(mas=set())

    logname = shlex.quote(file)
    tmpname = shlex.quote(temp)
    quiet = str(args.quiet).lower()
    verbose = str(args.verbose).lower()
    packages = _merge_packages(args)

    mode = '-*- Mac App Store -*-'.center(80, ' ')
    with open(file, 'a') as logfile:
        logfile.write(f'\n\n{mode}\n\n')
    if not args.quiet:
        print(f'-*- {blue}Mac App Store{reset} -*-\n')

    logging = subprocess.run(
        ['bash', os.path.join(ROOT, 'logging_mas.sh'), logname, tmpname],
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
    )
    if 'all' in packages or args.all:
        log = set(re.split('[\r\n]', logging.stdout.decode().strip()))
        outdated = 'true' if log and all(log) else 'false'
    else:
        log = packages
        outdated = 'true'

    subprocess.run(
        ['bash', os.path.join(ROOT, 'update_mas.sh'), password, logname, tmpname, quiet, verbose, outdated] + list(packages)
    )
    if not args.quiet:  print()
    return log if retset else dict(mas=log)


def update_npm(args, *, file, temp, disk, password, cleanup=True, retset=False):
    if shutil.which('npm') is None:
        print(
            f'update: {blush}{flash}npm{reset}: command not found\n'
            f'update: {red}npm{reset}: you may download Node.js from {purple}{under}https://nodejs.org/{reset}\n'
        )
        return set() if retset else dict(npm=set())

    logname = shlex.quote(file)
    tmpname = shlex.quote(temp)
    quiet = str(args.quiet).lower()
    verbose = str(args.verbose).lower()
    packages = _merge_packages(args)

    mode = '-*- Node.js -*-'.center(80, ' ')
    with open(file, 'a') as logfile:
        logfile.write(f'\n\n{mode}\n\n')
    if not args.quiet:
        print(f'-*- {blue}Node.js{reset} -*-\n')

    if 'all' in packages or args.all:
        allflag = 'true'
        logging = subprocess.run(
            ['bash', os.path.join(ROOT, 'logging_npm.sh'), logname, tmpname],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
        )
        start = logging.stdout.find(b'{')
        end = logging.stdout.rfind(b'}')
        if start == -1 or end == -1:
            stdout = str()
        else:
            stdout = logging.stdout[start:end+1].decode().strip()
        stdict = json.loads(stdout) if stdout else dict()
        log = set(stdict.keys())
        pkg = { f'{name}@{value["wanted"]}' for name, value in stdict.items() }
        outdated = 'true' if log and all(log) else 'false'
    else:
        allflag = 'false'
        log = pkg = packages
        outdated = 'true'

    subprocess.run(
        ['bash', os.path.join(ROOT, 'update_npm.sh'), password, logname, tmpname, allflag, quiet, verbose, outdated] + list(pkg)
    )
    if not args.quiet:  print()
    if not retset and not args.no_cleanup:
        update_cleanup(args, file=file, temp=temp, disk=disk, password=password, npm=True)
    return log if retset else dict(npm=log)


def update_pip(args, *, file, temp, disk, password, cleanup=True, retset=False):
    logname = shlex.quote(file)
    tmpname = shlex.quote(temp)
    quiet = str(args.quiet).lower()
    verbose = str(args.verbose).lower()
    yes = str(args.yes).lower()
    pre = str(args.pre).lower()
    packages = _merge_packages(args)

    mode = '-*- Python -*-'.center(80, ' ')
    with open(file, 'a') as logfile:
        logfile.write(f'\n\n{mode}\n\n')
    if not args.quiet:
        print(f'-*- {blue}Python{reset} -*-\n')

    flag = not ('pip' in args.mode and any((args.version, args.system, args.brew, args.cpython, args.pypy)))
    if flag and packages:
        system, brew, cpython, pypy, version = 'true', 'true', 'true', 'true', '1'
    else:
        system, brew, cpython, pypy, version = \
            str(args.system).lower(), str(args.brew).lower(), \
            str(args.cpython).lower(), str(args.pypy).lower(), str(args.version)

    logging = subprocess.run(
        ['bash', os.path.join(ROOT, 'logging_pip.sh'), logname, tmpname, system, brew, cpython, pypy, version, pre] + list(packages),
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
    )
    log = set(logging.stdout.decode().strip().split())
    if 'macdaily' in log:
        os.kill(os.getpid(), signal.SIGUSR1)

    subprocess.run(
        ['bash', os.path.join(ROOT, 'update_pip.sh'), password, logname, tmpname, system, brew, cpython, pypy, version, yes, quiet, verbose, pre] + list(packages)
    )
    subprocess.run(
        ['bash', os.path.join(ROOT, 'relink_pip.sh')],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    if not args.quiet:  print()
    if not retset and not args.no_cleanup:
        update_cleanup(args, file=file, temp=temp, disk=disk, password=password, pip=True)
    return log if retset else dict(pip=log)


def update_brew(args, *, file, temp, disk, password, cleanup=True, retset=False):
    if shutil.which('brew') is None:
        print(
            f'update: {blush}{flash}brew{reset}: command not found\n'
            f'update: {red}brew{reset}: you may find Homebrew on {purple}{under}https://brew.sh{reset}, or install Homebrew through following command -- '
            f'`{bold}/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"{reset}`\n'
        )
        return set() if retset else dict(brew=set())

    logname = shlex.quote(file)
    tmpname = shlex.quote(temp)
    quiet = str(args.quiet).lower()
    verbose = str(args.verbose).lower()
    force = str(args.force).lower()
    merge = str(args.merge).lower()
    packages = _merge_packages(args)

    mode = '-*- Homebrew -*-'.center(80, ' ')
    with open(file, 'a') as logfile:
        logfile.write(f'\n\n{mode}\n\n')
    if not args.quiet:
        print(f'-*- {blue}Homebrew{reset} -*-\n')

    global BREW_RENEWED
    if not BREW_RENEWED:
        subprocess.run(
            ['bash', os.path.join(ROOT, 'renew_brew.sh'), logname, tmpname, quiet, verbose, force, merge]
        )
        BREW_RENEWED = True

    if 'all' in packages or args.all:
        logging = subprocess.run(
            ['bash', os.path.join(ROOT, 'logging_brew.sh'), logname, tmpname],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
        )
        log = set(logging.stdout.decode().strip().split())
        outdated = 'true' if log and all(log) else 'false'
    else:
        log = packages
        outdated = 'true'

    subprocess.run(
        ['bash', os.path.join(ROOT, 'update_brew.sh'), password, logname, tmpname, quiet, verbose, outdated] + list(log)
    )
    if not args.quiet:  print()
    if not retset and not args.no_cleanup:
        update_cleanup(args, file=file, temp=temp, disk=disk, password=password, brew=True)
    return log if retset else dict(brew=log)


def update_cask(args, *, file, temp, disk, password, cleanup=True, retset=False):
    testing = subprocess.run(
        ['brew', 'command', 'cask'],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    if testing.returncode:
        print(
            f'update: {blush}{flash}cask{reset}: command not found\n'
            f'update: {red}cask{reset}: you may find Caskroom on {purple}{under}https://caskroom.github.io{reset}, '
            f'or install Caskroom through following command -- `{bold}brew tap homebrew/cask{reset}`\n'
        )
        return set() if retset else dict(cask=set())

    logname = shlex.quote(file)
    tmpname = shlex.quote(temp)
    quiet = str(args.quiet).lower()
    verbose = str(args.verbose).lower()
    force = str(args.force).lower()
    merge = str(args.merge).lower()
    greedy = str(args.greedy).lower()
    packages = _merge_packages(args)

    mode = '-*- Caskroom -*-'.center(80, ' ')
    with open(file, 'a') as logfile:
        logfile.write(f'\n\n{mode}\n\n')
    if not args.quiet:
        print(f'-*- {blue}Caskroom{reset} -*-\n')

    global BREW_RENEWED
    if not BREW_RENEWED:
        subprocess.run(
            ['bash', os.path.join(ROOT, 'renew_brew.sh'), logname, tmpname, quiet, verbose, force, merge]
        )
        BREW_RENEWED = True

    if 'all' in packages or args.all:
        logging = subprocess.run(
            ['bash', os.path.join(ROOT, 'logging_cask.sh'), logname, tmpname, greedy, force],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
        )
        log = set(logging.stdout.decode().strip().split())
        outdated = 'true' if log and all(log) else 'false'
    else:
        log = packages
        outdated = 'true'

    subprocess.run(
        ['bash', os.path.join(ROOT, 'update_cask.sh'), password, logname, tmpname, quiet, verbose, force, greedy, outdated] + list(log)
    )
    if not args.quiet:  print()
    if not retset and not args.no_cleanup:
        update_cleanup(args, file=file, temp=temp, disk=disk, password=password, cask=True)
    return log if retset else dict(cask=log)


def update_system(args, *, file, temp, disk, password, retset=False):
    if shutil.which('softwareupdate') is None:
        print(
            f'update: {blush}{flash}system{reset}: command not found\n'
            f"update: {red}system{reset}: you may add `softwareupdate' to $PATH through the following command -- "
            f"`{bold}echo export PATH='/usr/sbin:$PATH' >> ~/.bash_profile{reset}'\n"
        )
        return set() if retset else dict(system=set())

    logname = shlex.quote(file)
    tmpname = shlex.quote(temp)
    quiet = str(args.quiet).lower()
    verbose = str(args.verbose).lower()
    restart = str(args.restart).lower()
    packages = _merge_packages(args)

    mode = '-*- System -*-'.center(80, ' ')
    with open(file, 'a') as logfile:
        logfile.write(f'\n\n{mode}\n\n')
    if not args.quiet:
        print(f'-*- {blue}System{reset} -*-\n')

    logging = subprocess.run(
        ['bash', os.path.join(ROOT, 'logging_system.sh'), logname, tmpname],
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
    )
    if 'all' in packages or args.all:
        log = set(re.split('[\n\r]', logging.stdout.decode().strip()))
        outdated = 'true' if log and all(log) else 'false'
    else:
        log = packages
        outdated = 'true'

    subprocess.run(
        ['bash', os.path.join(ROOT, 'update_system.sh'), password, logname, tmpname, quiet, verbose, restart, outdated] + list(packages)
    )
    if not args.quiet:  print()
    return log if retset else dict(system=log)


def update_cleanup(args, *, file, temp, disk, password, gem=False, npm=False, pip=False, brew=False, cask=False, retset=False):
    logname = shlex.quote(file)
    tmpname = shlex.quote(temp)
    dskname = shlex.quote(disk)
    gem = str(args.gem if 'cleanup' in args.mode else gem).lower()
    npm = str(args.npm if 'cleanup' in args.mode else npm).lower()
    pip = str(args.pip if 'cleanup' in args.mode else pip).lower()
    brew = str(args.brew if 'cleanup' in args.mode else brew).lower()
    cask = str(args.cask if 'cleanup' in args.mode else cask).lower()
    quiet = str(args.quiet).lower()

    mode = '-*- Cleanup -*-'.center(80, ' ')
    with open(file, 'a') as logfile:
        logfile.write(f'\n\n{mode}\n\n')
    if not args.quiet and any((gem, npm, pip, brew, cask)):
        print(f'-*- {blue}Cleanup{reset} -*-\n')

    subprocess.run(
        ['bash', os.path.join(ROOT, 'cleanup.sh'), password, logname, tmpname, dskname, gem, npm, pip, brew, cask, quiet]
    )
    if not args.quiet:  print()
    return set() if retset else dict(cleanup=set())
