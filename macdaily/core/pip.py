# -*- coding: utf-8 -*-

import abc
import collections
import contextlib
import copy
import glob
import os
import re
import sys
import traceback

from macdaily.cls.command import Command
from macdaily.util.const import bold, green, red, reset, yellow
from macdaily.util.misc import (date, get_input, make_stderr, print_info,
                                print_scpt, print_term, print_text, sudo)

try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess


class PipCommand(Command):

    @property
    def mode(self):
        return 'pip'

    @property
    def name(self):
        return 'Pip Installs Packages'

    @property
    def desc(self):
        return ('Python package', 'Python packages')

    def _check_exec(self):
        return True

    def _pkg_args(self, namespace):
        def match(version):
            return re.fullmatch(r'\d(\.\d)?', version)

        temp_ver = list()
        args_ver = namespace.get('version', list())
        for item in args_ver:
            if isinstance(item, str):
                item = filter(match, item.split(','))
            for version in map(lambda s: s.split(','), item):
                temp_ver.extend(filter(match, version))
        self._version = set(temp_ver)

        return super()._pkg_args(namespace)

    @abc.abstractmethod
    def _parse_args(self, namespace):
        super()._parse_args(namespace)
        self._brew = namespace.get('brew', False)
        self._cpython = namespace.get('cpython', False)
        self._no_cleanup = namespace.get('no_cleanup', False)
        self._pypy = namespace.get('pypy', False)
        self._system = namespace.get('system', False)
        self._verbose = namespace.get('verbose', False)

    def _loc_exec(self):
        EXEC_PATH = dict(
            source=dict(
                brew=collections.defaultdict(list),
                system=collections.defaultdict(list),
            ),
            version=collections.defaultdict(list),
            combination={
                (True, True): collections.defaultdict(list),
                (True, False): collections.defaultdict(list),
                (False, True): collections.defaultdict(list),
                (False, False): collections.defaultdict(list),
            },
            implementation=dict(
                cpython=collections.defaultdict(list),
                pypy=collections.defaultdict(list),
            ),
        )

        def _sort_glob(path, *, flag):
            implementation = 'cpython' if flag else 'pypy'
            glob_path = glob.glob(path)
            if not glob_path:
                return
            glob_path.sort(reverse=True)
            path = glob_path[0]

            try:
                ver_proc = subprocess.check_output([path, '--version'], stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError:
                return
            if re.match(rb"^Python \d\.\d", ver_proc, flags=(re.I | re.M)) is None:
                return
            ver_text = ver_proc.decode().split()[1]

            def _append_path(exec_path):
                exec_path[ver_text[:3]].append(path)
                exec_path[ver_text[0]].append(path)
                exec_path['main'].append(path)

            _append_path(EXEC_PATH['implementation'][implementation])
            _append_path(EXEC_PATH['combination'][(True, flag)])
            _append_path(EXEC_PATH['source']['brew'])
            _append_path(EXEC_PATH['version'])

        stderr = make_stderr(self._vflag, sys.stderr)
        try:
            proc = subprocess.check_output(['brew', '--prefix'], stderr=stderr)
        except subprocess.CalledProcessError:
            prefix = '/usr/local'
        else:
            prefix = proc.decode().strip()

        _sort_glob(os.path.join(prefix, 'Cellar/pypy/*/bin/pypy'), flag=False)
        _sort_glob(os.path.join(prefix, 'Cellar/pypy3/*/bin/pypy3'), flag=False)
        _sort_glob(os.path.join(prefix, 'Cellar/python@2/*/bin/python2.?'), flag=True)
        _sort_glob(os.path.join(prefix, 'Cellar/python/*/bin/python3.?'), flag=True)

        def _append_path(exec_path):
            exec_path[version[0]].append(path)
            exec_path[version].append(path)
            exec_path['main'].append(path)

        for path in glob.glob('/Library/Frameworks/Python.framework/Versions/?.?/bin/python?.?'):
            version = path[-3:]
            _append_path(EXEC_PATH['combination'][(False, True)])
            _append_path(EXEC_PATH['implementation']['cpython'])
            _append_path(EXEC_PATH['source']['system'])
            _append_path(EXEC_PATH['version'])

        def _extend_version(exec_path):
            if self._version:
                for version in self._version:
                    temp_exec.extend(exec_path[version])
            else:
                temp_exec.extend(exec_path['main'])

        temp_exec = list()
        if not any([self._brew, self._cpython, self._pypy, self._system]):
            _extend_version(EXEC_PATH['version'])
        elif (any([self._brew, self._system]) and not any([self._cpython, self._pypy])):
            if self._brew:
                _extend_version(EXEC_PATH['source']['brew'])
            if self._system:
                _extend_version(EXEC_PATH['source']['system'])
        elif (any([self._cpython, self._pypy]) and not any([self._brew, self._system])):
            if self._cpython:
                _extend_version(EXEC_PATH['implementation']['cpython'])
            if self._pypy:
                _extend_version(EXEC_PATH['implementation']['pypy'])
        else:
            if self._brew and self._cpython:
                _extend_version(EXEC_PATH['combination'][(True, True)])
            if self._brew and self._pypy:
                _extend_version(EXEC_PATH['combination'][(True, False)])
            if self._system and self._cpython:
                _extend_version(EXEC_PATH['combination'][(False, True)])
            if self._system and self._pypy:
                _extend_version(EXEC_PATH['combination'][(False, False)])
        self._exec = set(temp_exec)

    def _check_pkgs(self, path):
        _temp_pkgs = list()
        _lost_pkgs = list()

        text = 'Checking existence of specified packages'
        print_info(text, self._file, redirect=self._vflag)
        for package in self._packages:
            argv = [path, '-m', 'pip', 'show', package]

            args = ' '.join(argv)
            print_scpt(args, self._file, redirect=self._vflag)
            with open(self._file, 'a') as file:
                file.write('Script started on {}\n'.format(date()))
                file.write('command: {!r}\n'.format(args))

            try:
                proc = subprocess.check_output(argv, stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError:
                print_text(traceback.format_exc(), self._file, redirect=self._vflag)
                _lost_pkgs.append(package)
            else:
                print_text(proc.decode(), self._file, redirect=self._vflag)
                _temp_pkgs.append(package)
            finally:
                with open(self._file, 'a') as file:
                    file.write('Script done on {}\n'.format(date()))

        if _lost_pkgs:
            text = 'Listing installed {}'.format(self.desc[1])
            print_info(text, self._file, redirect=self._vflag)

            self._lost.extend(_lost_pkgs)
            argv = [path, '-m', 'pip', 'list']

            args = ' '.join(argv)
            print_scpt(args, self._file, redirect=self._vflag)
            with open(self._file, 'a') as file:
                file.write('Script started on {}\n'.format(date()))
                file.write('command: {!r}\n'.format(args))

            stderr = make_stderr(self._vflag, sys.stderr)
            try:
                proc = subprocess.check_output(argv, stderr=stderr)
            except subprocess.CalledProcessError:
                print_text(traceback.format_exc(), self._file, redirect=self._vflag)
                self._var__real_pkgs = set()
            else:
                context = proc.decode()
                print_text(context, self._file, redirect=self._vflag)
                self._var__real_pkgs = set(map(lambda pkg: pkg.split('==')[0], context.split()))
            finally:
                with open(self._file, 'a') as file:
                    file.write('Script done on {}\n'.format(date()))
        else:
            self._var__real_pkgs = set()

        self._var__lost_pkgs = set(_lost_pkgs)
        self._var__temp_pkgs = set(_temp_pkgs)

    def _proc_fixmissing(self, path):
        text = 'Checking broken {} dependencies'.format(self.desc[0])
        print_info(text, self._file, redirect=self._qflag)

        def _proc_check():
            argv = [path, '-m', 'pip', 'check']
            args = ' '.join(argv)
            print_scpt(args, self._file, redirect=self._vflag)
            with open(self._file, 'a') as file:
                file.write('Script started on {}\n'.format(date()))
                file.write('command: {!r}\n'.format(args))

            _deps_pkgs = list()
            stderr = make_stderr(self._vflag, sys.stderr)
            try:  # pip check exits with a non-zero status if any packages are missing dependencies
                proc = subprocess.run(argv, stdout=subprocess.PIPE, stderr=stderr)
            except subprocess.SubprocessError:
                print_text(traceback.format_exc(), self._file, redirect=self._vflag)
            else:
                context = proc.stdout.decode()
                print_text(context, self._file, redirect=self._vflag)

                for line in filter(None, context.strip().split('\n')):
                    if line == 'No broken requirements found.':
                        return set()
                    if 'which is not installed' in line:
                        _deps_pkgs.append(line.split()[3][:-1])
                    else:
                        _deps_pkgs.append(line.split()[4][:-1])
            finally:
                with open(self._file, 'a') as file:
                    file.write('Script done on {}\n'.format(date()))
            return set(_deps_pkgs)

        def _proc_confirm():
            pkgs = '{}, {}'.format(reset, bold).join(_deps_pkgs)
            text = 'macdaily-{}: {}pip{}: found broken dependencies: {}{}{}'.format(self.cmd, yellow, reset, bold, pkgs, reset)
            print_term(text, self._file, redirect=self._qflag)
            if self._yes or self._quiet:
                return True
            while True:
                ans = get_input(self._confirm, 'Would you like to reinstall?',
                                prefix='Found broken dependencies: {}.\n\n'.format(", ".join(_deps_pkgs)),
                                suffix=' ({}y{}/{}N{}) '.format(green, reset, red, reset))
                if re.match(r'[yY]', ans):
                    return True
                elif re.match(r'[nN]', ans):
                    return False
                else:
                    print('Invalid input.', file=sys.stderr)

        _deps_pkgs = _proc_check() - self._ignore
        if not _deps_pkgs:
            text = 'macdaily-{}: {}pip{}: no broken dependencies'.format(self.cmd, green, reset)
            print_term(text, self._file, redirect=self._qflag)
            return

        text = 'Fixing broken {} dependencies'.format(self.desc[0])
        print_info(text, self._file, redirect=self._qflag)

        if _proc_confirm():
            argv = [path, '-m', 'pip', 'reinstall']
            if self._quiet:
                argv.append('--quiet')
            if self._verbose:
                argv.append('--verbose')
            args = ' '.join(argv)

            _done_pkgs = set()
            while _deps_pkgs:
                for package in _deps_pkgs:
                    real_name = re.split(r'[<>=!]', package, maxsplit=1)[0]
                    print_scpt('{} {}'.format(args, package), self._file, redirect=self._qflag)

                    temp = copy.copy(argv)
                    temp[3] = 'uninstall'
                    print_scpt('{} {}'.format(" ".join(temp), real_name), self._file, redirect=self._qflag)
                    sudo('{} -m pip uninstall {} --yes'.format(path, real_name), self._file, self._password,
                         redirect=self._qflag, verbose=self._vflag, sethome=True, timeout=self._timeout)

                    temp = copy.copy(argv)
                    temp[3] = 'install'
                    print_scpt('{} {}'.format(" ".join(temp), package), self._file, redirect=self._qflag)
                    if not sudo('{} -m pip install {}'.format(path, package), self._file, self._password,
                                redirect=self._qflag, verbose=self._vflag, sethome=True, timeout=self._timeout):
                        with contextlib.suppress(ValueError):
                            self._pkgs.remove(real_name)
                _done_pkgs |= _deps_pkgs
                _deps_pkgs = _proc_check() - _done_pkgs - self._ignore
            text = 'macdaily-{}: {}pip{}: all broken dependencies fixed'.format(self.cmd, green, reset)
        else:
            text = 'macdaily-{}: {}pip{}: all broken dependencies remain'.format(self.cmd, red, reset)
        print_term(text, self._file, redirect=self._qflag)

    def _proc_cleanup(self):
        if self._no_cleanup:
            return

        text = 'Pruning caches and archives'
        print_info(text, self._file, redirect=self._qflag)

        argv = ['pip', 'cleanup']
        if self._verbose:
            argv.append('--verbose')
        if self._quiet:
            argv.append('--quiet')
        print_scpt(' '.join(argv), self._file, redirect=self._qflag)

        argv = ['rm', '-rf']
        if self._verbose:
            argv.append('-v')
        argv.append('')
        for path in ['/var/root/Library/Caches/pip/http/',
                     '/var/root/Library/Caches/pip/wheels/',
                     os.path.expanduser('~/Library/Caches/pip/http/'),
                     os.path.expanduser('~/Library/Caches/pip/wheels/')]:
            argv[-1] = path
            print_scpt(' '.join(argv), self._file, redirect=self._qflag)
            sudo(argv, self._file, self._password,
                 redirect=self._qflag, verbose=self._vflag)
