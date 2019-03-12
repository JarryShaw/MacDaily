# -*- coding: utf-8 -*-

import contextlib
import datetime
import os
import traceback
import warnings

from ptyng import _fetch_child  # pylint: disable=E0611

from macdaily.util.compat import subprocess
from macdaily.util.const.macro import PROGRAM, PYTHON, ROOT
from macdaily.util.const.term import bold, red, reset
from macdaily.util.tools.make import make_pipe, make_stderr
from macdaily.util.tools.print import print_misc, print_scpt, print_term, print_text


def date():
    now = datetime.datetime.now()
    txt = datetime.datetime.strftime(now, '%+')
    return txt


def kill(pid, signal):
    """Kill a process with a signal."""
    for chld in reversed(_fetch_child(pid)[1:]):
        try:
            os.kill(chld, signal)
        except OSError as error:
            with contextlib.suppress(OSError):
                os.kill(chld, signal.SIGTERM)
            message = f'failed to send signal to process {chld} with error message: {error!r}'
            warnings.showwarning(message, ResourceWarning, __file__, 29)


def predicate(filename):
    if os.path.basename(filename) == 'macdaily':
        return True
    return (ROOT in os.path.realpath(filename))  # pylint: disable=superfluous-parens


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


def run_script(argv, quiet=False, verbose=False, sudo=False,  # pylint: disable=dangerous-default-value
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
        print_term(f"macdaily: {red}error{reset}: "
                   f"command `{bold}{' '.join(error.cmd)!r}{reset}' failed", logfile, redirect=quiet)
        raise
    else:
        context = proc.decode()
        print_text(context, logfile, redirect=verbose)
    finally:
        with open(logfile, 'a') as file:
            file.write(f'Script done on {date()}\n')
