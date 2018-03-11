#!/usr/bin/python3
# -*- coding: utf-8 -*-


import os
import shlex
import shutil
import subprocess


__all__ = ['logging_apm', 'logging_appstore', 'logging_brew', 'logging_cask', 'logging_dotapp', 'logging_macapp', 'logging_pip']


def logging_apm(args, *, file):
    if shutil.which('apm') is not None:
        subprocess.run(['bash', 'liblogging/logging_apm.sh', file])
        if not args.quiet:
            os.system(f'echo "Atom packges logged in {file}."')


def logging_appstore(args, *, file):
    if shutil.which('apm') is not None:
        subprocess.run(['bash', 'liblogging/logging_appstore.sh', file])
        if not args.quiet:
            os.system(f'echo "Applications installed through Mac App Store logged in {file}."')


def logging_brew(args, *, file):
    if shutil.which('brew') is not None:
        subprocess.run(['bash', 'liblogging/logging_brew.sh', file])
        if not args.quiet:
            os.system(f'echo "Homebrew packges logged in {file}."')


def logging_cask(args, *, file):
    testing = subprocess.run(
        shlex.split('brew cask'),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    if not testing.returncode:
        subprocess.run(['bash', 'liblogging/logging_cask.sh', file])
        if not args.quiet:
            os.system(f'echo "Caskroom applications logged in {file}."')


def logging_dotapp(args, *, file):
    if shutil.which('find') is not None:
        subprocess.run(['sudo', '-H', 'bash', 'liblogging/logging_dotapp.sh', file])
        if not args.quiet:
            os.system(f'echo "All applications (*.app) logged in {file}."')


def logging_macapp(args, *, file):
    if shutil.which('find') is not None:
        subprocess.run(['bash', 'liblogging/logging_macapp.sh', file])
        if not args.quiet:
            os.system(f'echo "Applications installed in /Application folder logged in {file}."')


def logging_pip(args, *, file):
    if (args.version == 1 or not any((args.system, args.brew, args.cpython, args.pypy))):
        system, brew, cpython, pypy, version = 'true', 'true', 'true', 'true', '1'
    else:
        system, brew, cpython, pypy, version = \
            str(args.system).lower(), str(args.brew).lower(), \
            str(args.cpython).lower(), str(args.pypy).lower(), str(args.version or 1)

    subprocess.run(
        ['bash', 'liblogging/logging_pip.sh', file, system, brew, cpython, pypy, version]
    )
    if not args.quiet:
        os.system(f'echo "Python packages logged in {file}."')
