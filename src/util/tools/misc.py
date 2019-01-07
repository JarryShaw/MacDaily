# -*- coding: utf-8 -*-

import datetime
import os
import sys
import traceback

from macdaily.util.const.macro import PROGRAM, PYTHON
from macdaily.util.const.term import bold, red, reset
from macdaily.util.tools.make import make_pipe, make_stderr
from macdaily.util.tools.print import (print_misc, print_scpt, print_term,
                                       print_text)

if sys.version_info[:2] <= (3, 4):
    import subprocess32 as subprocess
else:
    import subprocess


def date():
    now = datetime.datetime.now()
    txt = datetime.datetime.strftime(now, '%+')
    return txt


def record(file, args, today, config=None, redirect=False):
    # record program arguments
    print_misc(f'{PYTHON} {PROGRAM}', file, redirect)
    with open(file, 'a') as log:
        log.writelines([f'TIME: {today!s}\n', f'FILE: {file}\n'])

    # record parsed arguments
    print_misc(f'Parsing command line arguments', file, redirect)
    with open(file, 'a') as log:
        for key, value in vars(args).items():
            if isinstance(value, dict):
                for k, v, in value.items():
                    log.write(f'ARG: {key} -> {k} = {v}\n')
            else:
                log.write(f'ARG: {key} = {value}\n')

    # record parsed configuration
    if config is not None:
        print_misc(f'Parsing configuration file '
                   f'{os.path.expanduser("~/.dailyrc")!r}', file, redirect)
        with open(file, 'a') as log:
            for key, value in config.items():
                for k, v, in value.items():
                    log.write(f'CFG: {key} -> {k} = {v}\n')


def run_script(argv, quiet=False, verbose=False, sudo=False,
               password=None, logfile=os.devnull, env=os.environ):
    args = ' '.join(argv)
    print_scpt(args, logfile, verbose)
    with open(logfile, 'a') as file:
        file.write(f'Script started on {date()}\n')
        file.write(f'command: {args!r}\n')

    try:
        if sudo:
            if password is not None:
                sudo_argv = ['sudo', '--stdin', '--prompt=Password:\n']
                sudo_argv.extend(argv)
                with make_pipe(password, verbose) as pipe:
                    proc = subprocess.check_output(sudo_argv, stdin=pipe.stdout,
                                                   stderr=make_stderr(verbose), env=env)
            else:
                sudo_argv = ['sudo']
                sudo_argv.extend(argv)
                proc = subprocess.check_output(sudo_argv, stderr=make_stderr(verbose), env=env)
        else:
            proc = subprocess.check_output(argv, stderr=make_stderr(verbose), env=env)
    except subprocess.CalledProcessError as error:
        print_text(traceback.format_exc(), logfile, redirect=verbose)
        print_term(f"macdaily: {red}misc{reset}: "
                   f"command `{bold}{' '.join(error.cmd)!r}{reset}' failed", logfile, redirect=quiet)
        raise
    else:
        context = proc.decode()
        print_text(context, logfile, redirect=verbose)
    finally:
            with open(logfile, 'a') as file:
                file.write(f'Script done on {date()}\n')
