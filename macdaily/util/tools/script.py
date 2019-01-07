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
        typescript.write('Script started on {}\n'.format(date()))
        typescript.write('command: {!r}\n'.format(args))

    if UNBUFFER is not None:
        returncode = _unbuffer(argv, file, password, yes, redirect, executable, prefix, suffix, timeout)
    elif SCRIPT is not None:
        returncode = _script(argv, file, password, yes, redirect, executable, prefix, suffix, timeout)
    else:
        returncode = _spawn(argv, file, password, yes, redirect, executable, prefix, suffix, timeout, shell)

    with open(file, 'a') as typescript:
        # print('Before:', typescript.tell())
        typescript.write('Script done on {}\n'.format(date()))
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

        sudo_argv = "echo {!r} | sudo --stdin --validate --prompt='Password:\n' &&".format(password)
        if yes is not None:
            if UNBUFFER is not None or SCRIPT is None:
                sudo_argv = '{} yes {} |'.format(sudo_argv, yes)
                yes = None
        if askpass is not None:
            sudo_argv = '{} SUDO_ASKPASS={!r} '.format(sudo_argv, askpass)

        sudo_argv = '{} sudo'.format(sudo_argv)
        if sethome:
            sudo_argv = '{} --set-home'.format(sudo_argv)
        if askpass is not None:
            sudo_argv = "{} --askpass --prompt='🔑 Enter your password for {}.'".format(sudo_argv, USER)
        return sudo_argv
    return run(argv, file, password=password, redirect=redirect, timeout=timeout, shell=True, yes=yes,
               prefix=make_prefix(argv, askpass, sethome), executable=executable, verbose=verbose, suffix=suffix)


def _unbuffer(argv=SHELL, file='typescript', password=None, yes=None, redirect=False,
              executable=SHELL, prefix=None, suffix=None, timeout=None):
    if suffix is not None:
        argv = '{} {}'.format(_merge(argv), suffix)
    argv = 'unbuffer -p {} | tee -a >({} | col -b >> {}) | {}'.format(_merge(argv), _ansi2text(password), file, _text2dim(password))
    # argv = f'unbuffer -p {_merge(argv)} | {text2dim(password)} | tee -a >({ansi2text(password)} | col -b >> {file})'
    if yes is not None:
        argv = 'yes {} | {}'.format(yes, argv)
    if prefix is not None:
        argv = '{} {}'.format(prefix, argv)
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
        argv = '{} {}'.format(_merge(argv), suffix)
    argc = 'script -q /dev/null {} -c "'.format(SHELL)
    if yes is not None:
        argc = '{} yes {} |'.format(argc, yes)
    argv = '{} {}" | tee -a >({} | col -b >> {}) | {}'.format(argc, _merge(argv), _ansi2text(password), file, _text2dim(password))
    if prefix is not None:
        argv = '{} {}'.format(prefix, argv)
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
        print_term("macdaily: {}misc{}: `{}unbuffer{}' and `{}script{}'"
                   'not found in your {}PATH{}, {}PTYng{} not installed'.format(yellow, reset, bold, reset, bold, reset, under, reset, bold, reset),
                   os.devnull, redirect=redirect)
        print('macdaily: {}misc{}: broken dependency'.format(red, reset), file=sys.stderr)
        raise

    if suffix is not None:
        argv = '{} {}'.format(_merge(argv), suffix)
    if prefix is not None:
        argv = '{} {}'.format(prefix, _merge(argv))
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
    return ('{} -c "'
            'import re, sys\n'
            'for line in sys.stdin:\n'
            "    data = line.rstrip().replace('^D\x08\x08', '')\n"
            "    temp = re.sub(r'\x1b\\[[0-9][0-9;]*m', r'', data, flags=re.IGNORECASE)\n"
            "    text = temp.replace('Password:', 'Password:\\r\\n'){}\n"
            '    if text:\n'
            "        print(text, end='\\r\\n')\n"
            '"'.format(sys.executable, _replace(password)))


def _text2dim(password):
    return ('{} -c "'
            'import re, sys\n'
            'for line in sys.stdin:\n'
            "    data = line.rstrip().replace('^D\x08\x08', '')\n"
            "    temp = {!r} + re.sub(r'(\x1b\\[[0-9][0-9;]*m)', r'\\1{}', data, flags=re.IGNORECASE)\n"
            "    text = temp.replace('Password:', 'Password:\\r\\n'){}\n"
            '    if text:\n'
            "        print(text, end='\\r\\n')\n"
            '"'.format(sys.executable, dim, dim, _replace(password)))


def _merge(argv):
    if isinstance(argv, str):
        return argv
    return ' '.join(argv)


def _replace(password):
    if password is None:
        return ''
    return (".replace({!r}, '********')".format(password))
