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
        if 'all' in args.mode:
            packages = {'all'}
        else:
            packages = {'null'}
    else:   # 'postinstall'
        if args.all:
            packages = {'all'}
        else:
            packages = {'null'}
    return packages


def reinstall_cleanup(args, *, file, date, mode, brew=False, cask=False):
    brew = str((not args.brew) if (mode == 'reinstall' and 'cleanup' in args.mode) else brew).lower()
    cask = str((not args.cask) if (mode == 'reinstall' and 'cleanup' in args.mode) else cask).lower()
    quiet = str(args.quiet).lower()

    mode = '-*- Cleanup -*-'.center(80, ' ')
    with open(file, 'a') as logfile:
        logfile.write(f'\n\n{mode}\n\n')

    if not args.quiet:
        os.system(f'echo "-*- $({blue})Cleanup$({reset}) -*-"; echo ;')

    subprocess.run(
        ['bash', 'libupdate/cleanup.sh', date, mode, brew, cask, quiet]
    )

    if not args.quiet:
        time.sleep(5)
        os.system('tput clear')


def reinstall_brew(args, *, file, date, cleanup=True, retset=False):
    if shutil.which('brew') is None:
        os.system(f'''
                echo "reinstall: $({red})brew$({reset}): command not found";
                echo "You may find Homebrew on $({under})https://brew.sh$({reset}), or install Homebrew through following command:"
                echo $({bold})'/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"'$({reset})
        ''')
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
        os.system(f'echo "-*- $({blue})Homebrew$({reset}) -*-"; echo ;')

    if 'null' in packages:
        log = set()
        if not args.quiet:
            os.system(f'echo "reinstall: $({green})brew$({reset}): no reinstallation performed"')
        with open(file, 'a') as logfile:
            logfile.write('INF: No reinstallation performed.\n')
    else:
        logging = subprocess.run(
            ['bash', 'libprinstall/logging_brew.sh', date, 'reinstall', start, end] + list(packages),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        log = set(logging.stdout.decode().split())
        if (args.start is not None) or (args.end is not None):
            pkg = set(logging.stdout.decode().split())
        else:
            pkg = packages

        if log:
            subprocess.run(
                ['bash', 'libprinstall/reinstall_brew.sh', date, quiet, verbose, force] + list(pkg)
            )
        else:
            if not args.quiet:
                os.system(f'echo "reinstall: $({green})brew$({reset}): no reinstallation performed"')
            with open(file, 'a') as logfile:
                logfile.write('INF: No reinstallation performed.\n')

    if not args.quiet:
        time.sleep(5)
        os.system('tput clear')
    if not retset and not args.no_cleanup:
        reinstall_cleanup(args, file=file, date=date, brew=True, mode='reinstall')
    return log if retset else dict(brew=log)


def reinstall_cask(args, *, file, date, cleanup=True, retset=False):
    testing = subprocess.run(
        shlex.split('brew cask'),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    if testing.returncode:
        os.system(f'''
                echo "reinstall: $({red})cask$({reset}): command not found";
                echo "You may find Caskroom on $({under})https://caskroom.github.io$({reset}), or install Caskroom through following command:"
                echo $({bold})'brew tap caskroom/cask'$({reset})
        ''')
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
        os.system(f'echo "-*- $({blue})Caskroom$({reset}) -*-"; echo ;')

    if 'null' in packages:
        log = set()
        if not args.quiet:
            os.system(f'echo "reinstall: $({green})brew$({reset}): no reinstallation performed"')
        with open(file, 'a') as logfile:
            logfile.write('INF: No reinstallation performed.\n')
    else:
        logging = subprocess.run(
            ['bash', 'libprinstall/logging_cask.sh', date, 'reinstall', start, end] + list(packages),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        log = set(logging.stdout.decode().split())
        if (args.start is not None) or (args.end is not None):
            pkg = set(logging.stdout.decode().split())
        else:
            pkg = packages

        if log:
            subprocess.run(
                ['bash', 'libprinstall/reinstall_cask.sh', date, quiet, verbose] + list(pkg)
            )
        else:
            if not args.quiet:
                os.system(f'echo "reinstall: $({green})brew$({reset}): no reinstallation performed"')
            with open(file, 'a') as logfile:
                logfile.write('INF: No reinstallation performed.\n')

    if not args.quiet:
        time.sleep(5)
        os.system('tput clear')
    if not retset and not args.no_cleanup:
        reinstall_cleanup(args, file=file, date=date, cask=True, mode='reinstall')
    return log if retset else dict(cask=log)


def reinstall_all(args, *, file, date):
    log = dict(
        brew = set(),
        cask = set(),
    )
    for mode in ('brew', 'cask'):
        if not args.__getattribute__(f'no_{mode}'):
            log[mode] = eval(f'reinstall_{mode}')(args, retset=True, file=file, date=date)

    if not args.no_cleanup:
        reinstall_cleanup(args, file=file, date=date, brew=True, cask=True)
    return log


def postinstall(args, *, file, date):
    if shutil.which('brew') is None:
        os.system(f'''
                echo "postinstall: $({red})brew$({reset}): command not found";
                echo "You may find Homebrew on $({under})https://brew.sh$({reset}), or install Homebrew through following command:"
                echo $({bold})'/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"'$({reset})
        ''')
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
        os.system(f'echo "-*- $({blue})Homebrew$({reset}) -*-"; echo ;')

    if ('all' in packages) or (args.start is not None) or (args.end is not None):
        logging = subprocess.run(
            ['bash', 'libprinstall/logging_brew.sh', date, 'postinstall', start, end] + list(packages),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        log = set(logging.stdout.replace(b'\x1b', b'').decode().split())
    else:
        log = packages

    if log:
        subprocess.run(
            ['bash', 'libprinstall/postinstall.sh', date, quiet, verbose] + list(log)
        )
    else:
        if not args.quiet:
            os.system(f'echo "postinstall: $({green})brew$({reset}): no postinstallation performed"')
        with open(file, 'a') as logfile:
            logfile.write('INF: No postinstallation performed.\n')

    if not args.quiet:
        time.sleep(5)
        os.system('tput clear')
    if not args.no_cleanup:
        reinstall_cleanup(args, file=file, date=date, brew=True, mode='postinstall')
    return log
