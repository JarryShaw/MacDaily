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
from macdaily.util.tools.print import print_environ, print_misc, print_scpt, print_term, print_text


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
            message = 'failed to send signal to process {} with error message: {!r}'.format(chld, error)
            warnings.showwarning(message, ResourceWarning, __file__, 29)


def predicate(filename):
    if os.path.basename(filename) == 'macdaily':
        return True
    return (ROOT in os.path.realpath(filename))  # pylint: disable=superfluous-parens


def record(file, args, today, config=None, redirect=False):
    # record program arguments
    print_misc('{} {}'.format(PYTHON, PROGRAM), file, redirect)
    with open(file, 'a') as log:
        log.writelines(['TIME: {!s}\n'.format(today), 'FILE: {}\n'.format(file)])

    # record parsed arguments
    print_misc('Parsing command line arguments', file, redirect)
    with open(file, 'a') as log:
        for key, value in vars(args).items():
            if isinstance(value, dict):
                for k, v, in value.items():
                    if v is None:
                        v = 'null'
                    log.write('ARG: {} -> {} = {}\n'.format(key, k, v))
            else:
                if value is None:
                    value = 'null'
                log.write('ARG: {} = {}\n'.format(key, value))

    # record parsed configuration file
    if config is not None:
        print_misc('Parsing configuration file '
                   '{!r}'.format(os.path.expanduser("~/.dailyrc")), file, redirect)
        with open(file, 'a') as log:
            for key, value in config.items():
                for k, v, in value.items():
                    if v is None:
                        v = 'null'
                    log.write('CFG: {} -> {} = {}\n'.format(key, k, v))

    # record parsed environment variables
    print_misc('Parsing environment variables', file, redirect)
    with open(file, 'a') as log:
        print_environ(log, value_only=True, no_term=True,
                      prefix='ENV: ', suffix=' = %s')


def run_script(argv, quiet=False, verbose=False, sudo=False,  # pylint: disable=dangerous-default-value
               password=None, logfile=os.devnull, env=os.environ):
    args = ' '.join(argv)
    print_scpt(args, logfile, verbose)
    with open(logfile, 'a') as file:
        file.write('Script started on {}\n'.format(date()))
        file.write('command: {!r}\n'.format(args))

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
        print_term("macdaily: {}error{}: "
                   "command `{}{!r}{}' failed".format(red, reset, bold, ' '.join(error.cmd), reset), logfile, redirect=quiet)
        raise
    else:
        context = proc.decode()
        print_text(context, logfile, redirect=verbose)
    finally:
        with open(logfile, 'a') as file:
            file.write('Script done on {}\n'.format(date()))
