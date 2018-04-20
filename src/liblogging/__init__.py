# -*- coding: utf-8 -*-


import os
import shlex
import shutil
import subprocess


__all__ = [
    'logging_apm', 'logging_pip', 'logging_brew', 'logging_cask',
    'logging_dotapp', 'logging_macapp', 'logging_appstore',
]


# terminal display
green = 'tput setaf 2'  # green
bold = 'tput bold'      # bold
under = 'tput smul'     # underline
reset = 'tput sgr0'     # reset


def logging_apm(args, *, file):
    if shutil.which('apm') is not None:
        subprocess.run(['bash', 'liblogging/logging_apm.sh', file])
        if not args.quiet:
            os.system(f'''
                echo "logging: $({green})apm$({reset}): $({bold})Atom$({reset}) packges logged in $({under}){file}$({reset})."
            ''')
    else:
        os.system(f'echo "logging: $({red})apm$({reset}): command not found"')


def logging_appstore(args, *, file):
    if shutil.which('find') is not None:
        subprocess.run(['bash', 'liblogging/logging_appstore.sh', file])
        if not args.quiet:
            os.system(f'''
                echo "logging: $({green})appstore$({reset}): Applications installed through $({bold})Mac App Store$({reset}) logged in $({under}){file}$({reset})."
            ''')


def logging_brew(args, *, file):
    if shutil.which('brew') is not None:
        subprocess.run(['bash', 'liblogging/logging_brew.sh', file])
        if not args.quiet:
            os.system(f'''
                echo "logging: $({green})brew$({reset}): $({bold})Homebrew$({reset}) packges logged in $({under}){file}$({reset})."
            ''')
    else:
        os.system(f'echo "logging: $({red}brew$({reset}): command not found"')


def logging_cask(args, *, file):
    testing = subprocess.run(
        shlex.split('brew cask'),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    if not testing.returncode:
        subprocess.run(['bash', 'liblogging/logging_cask.sh', file])
        if not args.quiet:
            os.system(f'''
                echo "logging: $({green})cask$({reset}): $({bold})Caskroom$({reset}) applications logged in $({under}){file}$({reset})."
            ''')
    else:
        os.system(f'echo "logging: $({red})cask$({reset}): command not found"')


def logging_dotapp(args, *, file):
    if shutil.which('find') is not None:
        subprocess.run(['sudo', '-H', 'bash', 'liblogging/logging_dotapp.sh', file])
        if not args.quiet:
            os.system(f'''
                echo "logging: $({green})dotapp$({reset}): All applications ($({bold})*.app$({reset})) logged in $({under}){file}$({reset})."
            ''')
    else:
        os.system(f'echo "logging: $({red})dotapp$({reset}): command not found"')


def logging_macapp(args, *, file):
    if shutil.which('find') is not None:
        subprocess.run(['bash', 'liblogging/logging_macapp.sh', file])
        if not args.quiet:
            os.system(f'''
                echo "logging: $({green})macapp$({reset}): Applications installed in $({bold})/Application$({reset}) folder logged in $({under}){file}$({reset})."
            ''')
    else:
        os.system(f'echo "logging: $({red})macapp$({reset}): command not found"')


def logging_pip(args, *, file):
    if args.all or (args.version == 1 or not any((args.system, args.brew, args.cpython, args.pypy))):
        system, brew, cpython, pypy, version = 'true', 'true', 'true', 'true', '1'
    else:
        system, brew, cpython, pypy, version = \
            str(args.system).lower(), str(args.brew).lower(), \
            str(args.cpython).lower(), str(args.pypy).lower(), str(args.version or 1)

    subprocess.run(
        ['bash', 'liblogging/logging_pip.sh', file, system, brew, cpython, pypy, version]
    )
    subprocess.run(
        ['bash', 'liblogging/relink_pip.sh'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    if not args.quiet:
        os.system(f'''
            echo "logging: $({green})pip$({reset}): $({bold})Python$({reset}) packages logged in $({under}){file}$({reset})."
        ''')
