# -*- coding: utf-8 -*-

import contextlib
import getpass
import os
import re
import sys
import traceback
import tty

from macdaily.util.const.macro import SCRIPT, SHELL, UNBUFFER, USER
from macdaily.util.const.term import bold, dim, red, reset, under, yellow
from macdaily.util.tools.make import make_stderr
from macdaily.util.tools.misc import date
from macdaily.util.tools.print import print_term, print_text

if sys.version_info[:2] <= (3, 4):
    import subprocess32 as subprocess
else:
    import subprocess


def script(argv=SHELL, file='typescript', *, password=None, yes=None, prefix=None,
           redirect=False, timeout=None, shell=False, executable=SHELL, suffix=None):
    if isinstance(argv, str):
        argv = [argv]
    else:
        argv = list(argv)

    with open(file, 'a') as typescript:
        args = " ".join(argv)
        if password is not None:
            args = args.replace(password, '********')
        typescript.write(f'Script started on {date()}\n')
        typescript.write(f'command: {args!r}\n')

    if UNBUFFER is not None:
        returncode = _unbuffer(argv, file, password, yes, redirect, executable, prefix, suffix, timeout)
    elif SCRIPT is not None:
        returncode = _script(argv, file, password, yes, redirect, executable, prefix, suffix, timeout)
    else:
        returncode = _spawn(argv, file, password, yes, redirect, executable, prefix, suffix, timeout, shell)

    with open(file, 'a') as typescript:
        # print('Before:', typescript.tell())
        typescript.write(f'Script done on {date()}\n')
        # print('After:', typescript.tell())
    sys.stdout.write(reset)
    return returncode


def run(argv, file, *, redirect=False, password=None, yes=None, shell=False,
        prefix=None, suffix=None, timeout=None, executable=SHELL, verbose=False):
    if redirect:
        if suffix is None:
            suffix = '> /dev/null'
        else:
            suffix += ' > /dev/null'
    return script(argv, file, password=password, yes=yes, redirect=verbose, shell=shell,
                  executable=executable, timeout=timeout, prefix=prefix, suffix=suffix)


def sudo(argv, file, password, *, askpass=None, sethome=False, yes=None,
         redirect=False, verbose=False, timeout=None, executable=SHELL, suffix=None):
    def make_prefix(argv, askpass, sethome):
        if not isinstance(argv, str):
            argv = ' '.join(argv)
        if getpass.getuser() == 'root':
            return None
        nonlocal yes

        sudo_argv = f"echo {password!r} | sudo --stdin --validate --prompt='Password:\n' &&"
        if yes is not None:
            if UNBUFFER is not None or SCRIPT is None:
                sudo_argv = f'{sudo_argv} yes {yes} |'
                yes = None
        if askpass is not None:
            sudo_argv = f'{sudo_argv} SUDO_ASKPASS={askpass!r} '

        sudo_argv = f'{sudo_argv} sudo'
        if sethome:
            sudo_argv = f'{sudo_argv} --set-home'
        if askpass is not None:
            sudo_argv = f"{sudo_argv} --askpass --prompt='🔑 Enter your password for {USER}.'"
        return sudo_argv
    return run(argv, file, password=password, redirect=redirect, timeout=timeout, shell=True, yes=yes,
               prefix=make_prefix(argv, askpass, sethome), executable=executable, verbose=verbose, suffix=suffix)


def _unbuffer(argv=SHELL, file='typescript', password=None, yes=None, redirect=False,
              executable=SHELL, prefix=None, suffix=None, timeout=None):
    if suffix is not None:
        argv = f'{_merge(argv)} {suffix}'
    argv = f'unbuffer -p {_merge(argv)} | tee -a >({_ansi2text(password)} | col -b >> {file}) | {_text2dim(password)}'
    # argv = f'unbuffer -p {_merge(argv)} | {text2dim(password)} | tee -a >({ansi2text(password)} | col -b >> {file})'
    if yes is not None:
        argv = f'yes {yes} | {argv}'
    if prefix is not None:
        argv = f'{prefix} {argv}'
    # argv = f'set -x; {argv}'

    mode = None
    with contextlib.suppress(tty.error):
        mode = tty.tcgetattr(0)

    try:
        returncode = subprocess.check_call(argv, shell=True, executable=SHELL,
                                           timeout=timeout, stderr=make_stderr(redirect))
    except subprocess.SubprocessError as error:
        if mode is not None:
            with contextlib.suppress(tty.error):
                if tty.tcgetattr(0) != mode:
                    tty.tcsetattr(0, tty.TCSAFLUSH, mode)

        text = traceback.format_exc()
        if password is not None:
            text = text.replace(password, '********')
        print_text(text, file, redirect=redirect)
        returncode = getattr(error, 'returncode', 1)
    # if password is not None:
    #     with contextlib.suppress(subprocess.SubprocessError):
    #         subprocess.run(['chown', getpass.getuser(), file], stdout=subprocess.DEVNULL)
    return returncode


def _script(argv=SHELL, file='typescript', password=None, yes=None, redirect=False,
            executable=SHELL, prefix=None, suffix=None, timeout=None):
    if suffix is not None:
        argv = f'{_merge(argv)} {suffix}'
    argc = f'script -q /dev/null {SHELL} -c "'
    if yes is not None:
        argc = f'{argc} yes {yes} |'
    argv = f'{argc} {_merge(argv)}" | tee -a >({_ansi2text(password)} | col -b >> {file}) | {_text2dim(password)}'
    if prefix is not None:
        argv = f'{prefix} {argv}'
    # argv = f'set -x; {argv}'

    mode = None
    with contextlib.suppress(tty.error):
        mode = tty.tcgetattr(0)

    try:
        returncode = subprocess.check_call(argv, shell=True, executable=SHELL,
                                           timeout=timeout, stderr=make_stderr(redirect))
    except subprocess.SubprocessError as error:
        if mode is not None:
            with contextlib.suppress(tty.error):
                if tty.tcgetattr(0) != mode:
                    tty.tcsetattr(0, tty.TCSAFLUSH, mode)

        text = traceback.format_exc().replace('\n', '\\n')
        if password is not None:
            text = text.replace(password, '********')
        print_text(text, file, redirect=redirect)
        returncode = getattr(error, 'returncode', 1)
    # if password is not None:
    #     with contextlib.suppress(subprocess.SubprocessError):
    #         subprocess.run(['chown', getpass.getuser(), file], stdout=subprocess.DEVNULL)
    return returncode


def _spawn(argv=SHELL, file='typescript', password=None, yes=None, redirect=False,
           executable=SHELL, prefix=None, suffix=None, timeout=None, shell=False):
    try:
        import ptyng
    except ImportError:
        print_term(f"macdaily: {yellow}misc{reset}: `{bold}unbuffer{reset}' and `{bold}script{reset}'"
                   f'not found in your {under}PATH{reset}, {bold}PTYng{reset} not installed',
                   os.devnull, redirect=redirect)
        print(f'macdaily: {red}misc{reset}: broken dependency', file=sys.stderr)
        raise

    if suffix is not None:
        argv = f'{_merge(argv)} {suffix}'
    if prefix is not None:
        argv = f'{prefix} {_merge(argv)}'
    if shell or isinstance(argv, str):
        argv = [executable, '-c', _merge(argv)]

    if password is not None:
        bpwd = password.encode()
    bdim = dim.encode()
    repl = rb'\1' + bdim
    # test = bytes()

    def master_read_ng(fd, replace=None):
        data = os.read(fd, 1024).replace(b'^D\x08\x08', b'')
        if replace is not None:
            data = data.replace(replace, b'')
        if password is not None:
            data = data.replace(bpwd, b'********')
        data = data.replace(b'Password:', b'Password:\r\n')
        text = re.sub(rb'\033\[[0-9][0-9;]*m', rb'', data, flags=re.IGNORECASE)
        typescript.write(text)
        byte = bdim + re.sub(rb'(\033\[[0-9][0-9;]*m)', repl, data, flags=re.IGNORECASE)
        # nonlocal test
        # test = byte
        return byte

    if yes is None:
        def master_read(fd):
            return master_read_ng(fd)

        def stdin_read(fd):
            return os.read(fd, 1024)
    else:
        if isinstance(yes, str):
            yes = yes.encode()
        txt = re.sub(rb'[\r\n]*$', rb'', yes)
        old = txt + b'\r\n'
        exp = txt + b'\n'

        def master_read(fd):
            return master_read_ng(fd, replace=old)

        def stdin_read(fd):
            return exp

    with open(file, 'ab') as typescript:
        returncode = ptyng.spawn(argv, master_read, stdin_read,
                                 timeout=timeout, env=os.environ)
    # if not test.decode().endswith(os.linesep):
    #     sys.stdout.write(os.linesep)
    return returncode


def _ansi2text(password):
    return (f'{sys.executable} -c "'
            'import re, sys\n'
            'for line in sys.stdin:\n'
            "    data = line.rstrip().replace('^D\x08\x08', '')\n"
            "    temp = re.sub(r'\x1b\\[[0-9][0-9;]*m', r'', data, flags=re.IGNORECASE)\n"
            f"    text = temp.replace('Password:', 'Password:\\r\\n'){_replace(password)}\n"
            '    if text:\n'
            "        print(text, end='\\r\\n')\n"
            '"')


def _text2dim(password):
    return (f'{sys.executable} -c "'
            'import re, sys\n'
            'for line in sys.stdin:\n'
            "    data = line.rstrip().replace('^D\x08\x08', '')\n"
            f"    temp = {dim!r} + re.sub(r'(\x1b\\[[0-9][0-9;]*m)', r'\\1{dim}', data, flags=re.IGNORECASE)\n"
            f"    text = temp.replace('Password:', 'Password:\\r\\n'){_replace(password)}\n"
            '    if text:\n'
            "        print(text, end='\\r\\n')\n"
            '"')


def _merge(argv):
    if isinstance(argv, str):
        return argv
    return ' '.join(argv)


def _replace(password):
    if password is None:
        return ''
    return (f".replace({password!r}, '********')")
