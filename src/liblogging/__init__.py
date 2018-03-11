#!/usr/bin/python3
# -*- coding: utf-8 -*-


import os
import re
import shlex
import shutil
import subprocess
import time


__all__ = ['logging_apm', 'logging_appstore', 'logging_brew', 'logging_cask', 'logging_dotapps', 'logging_macapps', 'logging_pip']


def logging_apm(args, *, file):
    if shutil.which('apm') is not None:
        subprocess.run(['bash', 'liblogging/logging_apm.sh', file])


def logging_appstore(args, *, file):
    if shutil.which('apm') is not None:
        subprocess.run(['bash', 'liblogging/logging_appstore.sh', file])


def logging_brew(args, *, file):
    if shutil.which('brew') is not None:
        subprocess.run(['bash', 'liblogging/logging_brew.sh', file])


def logging_cask(args, *, file):
    testing = subprocess.run(
        shlex.split('brew cask'),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    if not testing.returncode:
        subprocess.run(['bash', 'liblogging/logging_cask.sh', file])


def logging_dotapps(args, *, file):
    if shutil.which('find') is not None:
        subprocess.run(['sudo', '-H', 'bash', 'liblogging/logging_dotapps.sh', file])


def logging_macapps(args, *, file):
    if shutil.which('find') is not None:
        subprocess.run(['bash', 'liblogging/logging_macapps.sh', file])


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
