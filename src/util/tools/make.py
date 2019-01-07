# -*- coding: utf-8 -*-

import contextlib
import os
import sys

if sys.version_info[:2] <= (3, 4):
    import subprocess32 as subprocess
else:
    import subprocess


def make_context(redirect=False, devnull=open(os.devnull, 'w')):
    if redirect:
        return contextlib.redirect_stdout(devnull)
    return contextlib.nullcontext()


def make_description(command):
    def desc(singular):
        if singular:
            return command.desc[0]
        else:
            return command.desc[1]
    return desc


def make_namespace(args):
    if not isinstance(args, dict):
        args = vars(args)
    namespace = dict()
    for key, value in args.items():
        if value is None:
            continue
        namespace[key] = value
    return namespace


def make_pipe(password, redirect=False, devnull=subprocess.DEVNULL):
    return subprocess.Popen(['yes', password],
                            stdout=subprocess.PIPE,
                            stderr=make_stderr(redirect, devnull))


def make_stderr(redirect=False, devnull=subprocess.DEVNULL):
    if redirect:
        return devnull
    return None
