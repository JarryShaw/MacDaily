# -*- coding: utf-8 -*-

import contextlib
import datetime
import functools
import getpass
import multiprocessing
import os
import platform
import re
import shutil
import sys
import traceback
import tty

from macdaily.util.const import (SCRIPT, SHELL, UNBUFFER, USER, blue, bold,
                                 dim, grey, length, program, purple, python,
                                 red, reset, under, yellow)
from macdaily.util.error import ChildExit, TimeExpired, UnsupportedOS

try:
    import threading
except ImportError:
    import dummy_threading as threading

if sys.version_info[:2] == (3, 4):
    import subprocess32 as subprocess
else:
    import subprocess

# error-not-raised flag
FLAG = True

# timeout interval
TIMEOUT = int(os.environ.get('TIMEOUT', '60'))


def beholder(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        global FLAG
        if platform.system() != 'Darwin':
            print_term('macdaily: error: script runs only on macOS', os.devnull)
            raise UnsupportedOS
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            if FLAG:
                FLAG = False
                print('macdaily: {}error{}: operation interrupted'.format(red, reset), file=sys.stderr)
            sys.stdout.write(reset)
            sys.tracebacklimit = 0
            raise
        except Exception:
            if FLAG:
                FLAG = False
                print('macdaily: {}error{}: operation failed'.format(red, reset), file=sys.stderr)
            sys.stdout.write(reset)
            sys.tracebacklimit = 0
            raise
    return wrapper


def retry(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if sys.stdin.isatty():
            return func(*args, **kwargs)
        else:
            QUEUE = multiprocessing.Queue(1)
            kwargs['queue'] = QUEUE
            for _ in range(3):
                proc = multiprocessing.Process(target=func, args=args, kwargs=kwargs)
                timer = threading.Timer(TIMEOUT, function=lambda: proc.kill())
                timer.start()
                proc.start()
                proc.join()
                timer.cancel()
                if proc.exitcode == 0:
                    break
                if proc.exitcode != 9:
                    print_term('macdaily: {}misc{}: function {!r} '
                               'exits with exit status {} on child process'.format(yellow, reset, func.__qualname__, proc.exitcode), os.devnull)
                    raise ChildExit
            else:
                print_term('macdaily: {}misc{}: function {!r} '
                           'retry timeout after {} seconds'.format(red, reset, func.__qualname__, TIMEOUT), os.devnull)
                raise TimeExpired
            return QUEUE.get(block=False)
    return wrapper


def date():
    now = datetime.datetime.now()
    txt = datetime.datetime.strftime(now, '%+')
    return txt


@retry
def get_input(confirm, prompt='Input: ', *, prefix='', suffix='', queue=None):
    if sys.stdin.isatty():
        try:
            return input('{}{}'.format(prompt, suffix))
        except KeyboardInterrupt:
            print(reset)
            raise
    try:
        subprocess.check_call(['osascript', confirm, '{}{}'.format(prefix, prompt)],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        RETURN = 'N'
    else:
        RETURN = 'Y'
    finally:
        if queue is not None:
            queue.put(RETURN)
        return RETURN


@retry
def get_pass(askpass, queue=None):
    if sys.stdin.isatty():
        try:
            return getpass.getpass(prompt='Password:')
        except KeyboardInterrupt:
            print(reset)
            raise
    RETURN = subprocess.check_output([askpass, '🔑 Enter your password for {}.'.format(USER)],  # pylint: disable=E1101
                                     stderr=subprocess.DEVNULL).strip().decode()
    if queue is not None:
        queue.put(RETURN)
    return RETURN


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


def print_info(text, file, redirect=False):
    flag = text.endswith(os.linesep)
    if not redirect:
        end = str() if flag else os.linesep
        print_wrap('{}{}|💼|{} {}{}{}'.format(bold, blue, reset, bold, text, reset), end=end)
    with open(file, 'a') as fd:
        context = re.sub(r'(\033\[[0-9][0-9;]*m)|(\^D\x08\x08)', r'',
                         (text if flag else '{}{}'.format(text, os.linesep)), flags=re.IGNORECASE)
        fd.write('|💼| {}'.format(context))


def print_misc(text, file, redirect=False):
    flag = text.endswith(os.linesep)
    if not redirect:
        end = str() if flag else os.linesep
        print_wrap('{}{}|📌|{} {}{}{}'.format(bold, grey, reset, bold, text, reset), end=end)
    with open(file, 'a') as fd:
        context = re.sub(r'(\033\[[0-9][0-9;]*m)|(\^D\x08\x08)', r'',
                         (text if flag else '{}{}'.format(text, os.linesep)), flags=re.IGNORECASE)
        fd.write('|📌| {}'.format(context))


def print_scpt(text, file, redirect=False):
    if not isinstance(text, str):
        text = ' '.join(text)
    flag = text.endswith(os.linesep)
    if not redirect:
        end = str() if flag else os.linesep
        print_wrap('{}{}|📜|{} {}{}{}'.format(bold, purple, reset, bold, text, reset), end=end)
    with open(file, 'a') as fd:
        context = re.sub(r'(\033\[[0-9][0-9;]*m)|(\^D\x08\x08)', r'',
                         (text if flag else '{}{}'.format(text, os.linesep)), flags=re.IGNORECASE)
        fd.write('|📜| {}'.format(context))


def print_term(text, file, redirect=False):
    flag = text.endswith(os.linesep)
    if not redirect:
        end = str() if flag else os.linesep
        print_wrap(text, end=end)
    with open(file, 'a') as fd:
        context = re.sub(r'(\033\[[0-9][0-9;]*m)|(\^D\x08\x08)', r'',
                         (text if flag else '{}{}'.format(text, os.linesep)), flags=re.IGNORECASE)
        fd.write(context)


def print_text(text, file, redirect=False):
    flag = text.endswith(os.linesep)
    if not redirect:
        end = str() if flag else os.linesep
        print_wrap('{}{}{}'.format(dim, text, reset), end=end)
    with open(file, 'a') as fd:
        context = re.sub(r'(\033\[[0-9][0-9;]*m)|(\^D\x08\x08)', r'',
                         (text if flag else '{}{}'.format(text, os.linesep)), flags=re.IGNORECASE)
        fd.write(context)


def print_wrap(text, length=length, **kwargs):
    print(wrap_text(text, length), **kwargs)


def record(file, args, today, config=None, redirect=False):
    # record program arguments
    print_misc('{} {}'.format(python, program), file, redirect)
    with open(file, 'a') as log:
        log.writelines(['TIME: {!s}\n'.format(today), 'FILE: {}\n'.format(file)])

    # record parsed arguments
    print_misc('Parsing command line arguments'.format(), file, redirect)
    with open(file, 'a') as log:
        for key, value in vars(args).items():
            if isinstance(value, dict):
                for k, v, in value.items():
                    log.write('ARG: {} -> {} = {}\n'.format(key, k, v))
            else:
                log.write('ARG: {} = {}\n'.format(key, value))

    # record parsed configuration
    if config is not None:
        print_misc('Parsing configuration file '
                   '{!r}'.format(os.path.expanduser("~/.dailyrc")), file, redirect)
        with open(file, 'a') as log:
            for key, value in config.items():
                for k, v, in value.items():
                    log.write('CFG: {} -> {} = {}\n'.format(key, k, v))


def run_script(argv, quiet=False, verbose=False, sudo=False,
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
        print_term("macdaily: {}misc{}: "
                   "command `{}{!r}{}' failed".format(red, reset, bold, ' '.join(error.cmd), reset), logfile, redirect=quiet)
        raise
    else:
        context = proc.decode()
        print_text(context, logfile, redirect=verbose)
    finally:
            with open(logfile, 'a') as file:
                file.write('Script done on {}\n'.format(date()))


def run(argv, file, *, redirect=False, password=None, yes=None, shell=False,
        prefix=None, suffix=None, timeout=None, executable=SHELL, verbose=False):
    if redirect:
        if suffix is None:
            suffix = '> /dev/null'
        else:
            suffix += ' > /dev/null'
    return script(argv, file, password=password, yes=yes, redirect=verbose, shell=shell,
                  executable=executable, timeout=timeout, prefix=prefix, suffix=suffix)


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


def _merge(argv):
    if isinstance(argv, str):
        return argv
    return ' '.join(argv)


def _replace(password):
    if password is None:
        return ''
    return (".replace({!r}, '********')".format(password))


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


def wrap_text(string, length=length):
    # text = '\n'.join(textwrap.wrap(string, length))
    # if string.endswith(os.linesep):
    #     return f'{text}{os.linesep}'
    # return text
    return string
