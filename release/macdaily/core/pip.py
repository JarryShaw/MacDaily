# -*- coding: utf-8 -*-

import abc
import collections
import glob
import itertools
import os
import re

from macdaily.cls.command import Command
from macdaily.util.const import bold, reset, yellow
from macdaily.util.misc import print_info, print_scpt, sudo

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
        return False

    def _pkg_args(self, namespace):
        def match(version):
            return re.fullmatch(r'\d(\.\d)?', version)

        temp_ver = list()
        args_ver = namespace.pop('version', list())
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
        self._brew = namespace.pop('brew', False)
        self._cpython = namespace.pop('cpython', False)
        self._no_cleanup = namespace.pop('no_cleanup', False)
        self._pypy = namespace.pop('pypy', False)
        self._system = namespace.pop('system', False)
        self._verbose = namespace.pop('verbose', False)

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

        try:
            proc = subprocess.check_output(['brew', '--prefix'], stderr=subprocess.DEVNULL)
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
        argc = ' '.join(argv)
        for path in ['/var/root/Library/Caches/pip/http/',
                     '/var/root/Library/Caches/pip/wheels/',
                     os.path.expanduser('~/Library/Caches/pip/http/'),
                     os.path.expanduser('~/Library/Caches/pip/wheels/')]:
            args = '{} {}'.format(argc, path)
            print_scpt(args, self._file, redirect=self._qflag)
            sudo(args, self._file, askpass=self._askpass, redirect=self._qflag)
