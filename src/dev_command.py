# -*- coding: utf-8 -*-

import abc
import collections
import glob
import re
import subprocess


class Command(metaclass=abc.ABCMeta):
    """Base command.

    1. keep namespace
    2. decide executable
    3. enumerate and start processors

    """
    @property
    @abc.abstractmethod
    def mode(self):
        return NotImplemented

    @property
    def packages(self):
        return set(self._pkgs)

    def __init__(self, args):
        self._pkg_args(args)
        self._loc_exec()
        self._run_proc()

    def _pkg_args(self, args):
        self._args = args
        namespace = vars(args)

        self._merge_packages(namespace)
        self._parse_args(namespace)

    def _merge_packages(self, namespace):
        temp_pkg = list()
        args_pkg = namespace.pop(f'{self.mode}_pkgs', list())
        for pkgs in args_pkg:
            temp_pkg.extend(filter(None, pkgs.split(',')))
        self._packages = set(temp_pkg)

    @abc.abstractmethod
    def _parse_args(self, namespace):
        pass

    @abc.abstractmethod
    def _loc_exec(self):
        self._exec = list()

    @abc.abstractmethod
    def _run_proc(self):
        self._pkgs = list()


class UpdateCommand(Command):

    @property
    def failed(self):
        return set(self._fail)

    def _run_proc(self):
        self._pkgs = list()
        self._fail = list()
        for path in self._exec:
            self._proc_logging(path)
            self._proc_update(path)

    def _proc_logging(self, path):
        if self._packages:
            self._check_pkgs(path)
        else:
            self._check_list(path)

    @abc.abstractmethod
    def _check_pkgs(self, path):
        self.__temp_pkgs = self._packages

    @abc.abstractmethod
    def _check_list(self, path):
        self.__temp_pkgs = set()

    @abc.abstractmethod
    def _proc_update(self, path):
        pass


class PipUpdate(UpdateCommand):

    @property
    def mode(self):
        return 'pip'

    def _pkg_args(self, args):
        super()._pkg_args(args)

        def match(version):
            return re.fullmatch(r'\d(\.\d)?', version)

        temp_ver = list()
        args_ver = getattr(args, 'version', list())
        for item in args_ver:
            temp_ver.extend(filter(match, item.split(',')))
        self._version = set(temp_ver)

    def _parse_args(self, namespace):
        self._brew = namespace.pop('brew', False)
        self._cpython = namespace.pop('cpython', False)
        self._pre = namespace.pop('pre', False)
        self._pypy = namespace.pop('pypy', False)
        self._quiet = namespace.pop('quiet', False)
        self._show_log = namespace.pop('show_log', False)
        self._system = namespace.pop('system', False)
        self._verbose = namespace.pop('verbose', False)
        self._yes = namespace.pop('yes', False)

        self._logging_opts = namespace.pop('logging', str()).split()
        self._update_opts = namespace.pop('update', str()).split()

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
            glob_path.sort()
            path = glob_path[-1]

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

        _sort_glob('/usr/local/Cellar/pypy/*/bin/pypy', flag=False)
        _sort_glob('/usr/local/Cellar/pypy3/*/bin/pypy3', flag=False)
        _sort_glob('/usr/local/Cellar/python@2/*/bin/python2.?', flag=True)
        _sort_glob('/usr/local/Cellar/python/*/bin/python3.?', flag=True)

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
                _extend_version(EXEC_PATH['brew'])
            if self._system:
                _extend_version(EXEC_PATH['system'])
        elif (any([self._cpython, self._pypy]) and not any([self._brew, self._system])):
            if self._cpython:
                _extend_version(EXEC_PATH['cpython'])
            if self._pypy:
                _extend_version(EXEC_PATH['pypy'])
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

        import pprint
        pprint.pprint(self._exec)

    def _check_pkgs(self, path):
        temp_pkgs = list()
        for package in self._packages:
            try:
                subprocess.check_call([path, 'show', package], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except subprocess.CalledProcessError:
                continue
            temp_pkgs.append(package)
        self.__temp_pkgs = set(package)

    def _check_list(self, path):
        args = [path, '-m', 'pip', 'list', '--format=freeze', '--outdated']
        if self._pre:
            args.append('--pre')
        args.extend(self._logging_opts)

        try:
            proc = subprocess.check_output(args, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            self.__temp_pkgs = set()
        else:
            self.__temp_pkgs = set(map(lambda pkg: pkg.split('==')[0], proc.decode().split()))

    def _proc_update(self, path):
        args = ['sudo', '--set-home', path, '-m', 'pip', 'install', '--upgrade']
        if self._pre:
            args.append('--pre')
        if self._quiet:
            args.append('--quiet')
        if self._verbose:
            args.append('--verbose')
        args.extend(self._update_opts)

        for package in self.__temp_pkgs:
            args.append(package)
            try:
                subprocess.check_call(args)
            except subprocess.CalledProcessError:
                self._fail.append(package)
            else:
                self._pkgs.append(package)
        del self.__temp_pkgs


if __name__ == '__main__':
    import argparse
    arg = argparse.Namespace()
    cmd = PipUpdate(arg)
    print(cmd.packages, cmd.failed)
