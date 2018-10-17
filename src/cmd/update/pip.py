# -*- coding: utf-8 -*-

import collections
import contextlib
import copy
import glob
import itertools
import json
import os
import re
import traceback

from macdaily.cmd.update.command import UpdateCommand
from macdaily.util.colours import bold, green, red, reset, yellow
from macdaily.util.tools import script

try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess


class PipUpdate(UpdateCommand):

    @property
    def mode(self):
        return 'pip'

    @property
    def name(self):
        return 'Python'

    @property
    def desc(self):
        return ('Python package', 'Python packages')

    def _check_exec(self):
        return False

    def _pkg_args(self, args):
        def match(version):
            return re.fullmatch(r'\d(\.\d)?', version)

        temp_ver = list()
        args_ver = getattr(args, 'version', list())
        for item in args_ver:
            temp_ver.extend(filter(match, item.split(',')))
        self._version = set(temp_ver)

        return super()._pkg_args(args)

    def _parse_args(self, namespace):
        self._all = namespace.pop('all', False)
        self._brew = namespace.pop('brew', False)
        self._cleanup = namespace.pop('cleanup', True)
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

        # import pprint  # ###
        # pprint.pprint(self._exec)  # ###

    def _check_pkgs(self, path):
        _temp_pkgs = list()
        _lost_pkgs = list()
        for package in self._packages:
            try:
                subprocess.check_call([path, '-m', 'pip', 'show', package],
                                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except subprocess.CalledProcessError:
                _lost_pkgs.append(package)
            else:
                _temp_pkgs.append(package)

        if _lost_pkgs:
            self._lost.extend(_lost_pkgs)
            try:
                proc = subprocess.check_output([path, '-m', 'pip', 'list'])
            except subprocess.CalledProcessError:
                self.__real_pkgs = set()
            else:
                self.__real_pkgs = set(map(lambda pkg: pkg.split('==')[0], proc.decode().split()))
        else:
            self.__real_pkgs = set()
        self.__lost_pkgs = set(_lost_pkgs)
        self.__temp_pkgs = set(package)

    def _check_list(self, path):
        args = [path, '-m', 'pip', 'list', '--outdated']
        if self._pre:
            args.append('--pre')
        args.extend(self._logging_opts)
        args.append('--format=json')

        temp = copy.copy(args)
        temp[-1] = '--format=columns'
        self._log.write(f'+ {" ".join(temp)}\n')

        try:
            proc = subprocess.check_output(args, stderr=subprocess.DEVNULL, timeout=self._timeout)
        except subprocess.SubprocessError:
            self._log.write(traceback.format_exc())
            self.__temp_pkgs = set()
        else:
            # self.__temp_pkgs = set(map(lambda pkg: pkg.split('==')[0], proc.decode().split()))
            context = json.loads(proc.decode().strip())
            self.__temp_pkgs = set(map(lambda item: item['name'], context))

            if context:
                name_len = max(7, max(map(lambda item: len(item['name']), context), default=7))
                version_len = max(7, max(map(lambda item: len(item['version']), context), default=7))
                latest_version_len = max(6, max(map(lambda item: len(item['latest_version']), context), default=6))
                latest_filetype_len = max(4, max(map(lambda item: len(item['latest_filetype']), context), default=4))

                def _pprint(package, version, latest, type):
                    text = [package.ljust(name_len), version.ljust(version_len),
                            latest.ljust(latest_version_len), type.ljust(latest_filetype_len)]
                    return (' '.join(text) + '\n')

                self._log.write(_pprint('Package', 'Version', 'Latest', 'Type'))
                self._log.write(' '.join(map(lambda length: '-' * length,
                                             [name_len, version_len, latest_version_len, latest_filetype_len])) + '\n')
                for item in context:
                    self._log.write(_pprint(item['name'], item['version'],
                                            item['latest_version'], item['latest_filetype']))
        finally:
            self._log.write('\n')

    def _proc_update(self, path):
        args = [path, '-m', 'pip', 'install', '--upgrade']
        if self._pre:
            args.append('--pre')
        if self._quiet:
            args.append('--quiet')
        if self._verbose:
            args.append('--verbose')
        args.extend(self._update_opts)

        argc = ' '.join(args)
        for package in self.__temp_pkgs:
            argv = f'{argc} {package}'
            script(['echo', '-e', f'\n+ {bold}{argv}{reset}'], self._log.name)
            if script(f"yes {self._password} | sudo --set-home --stdin --prompt='' {argv}",
                      self._log.name, shell=True, timeout=self._timeout):
                self._fail.append(package)
            else:
                self._pkgs.append(package)
            self._log.write('\n')
        del self.__temp_pkgs

        def _proc_check():
            try:
                proc = subprocess.check_output([path], '-m', 'pip', 'check',
                                               stderr=subprocess.DEVNULL, timeout=self._timeout)
            except subprocess.SubprocessError:
                return set()

            _deps_pkgs = list()
            for line in filter(None, proc.decode().split('\n')):
                if line == 'No broken requirements found.':
                    return set()
                if 'which is not installed' in line:
                    _deps_pkgs.append(line.split()[3][:-1])
                else:
                    _deps_pkgs.append(line.split()[4][:-1])
            return set(_deps_pkgs)

        def _proc_confirm():
            pkgs = f'{reset}, {bold}'.join(_deps_pkgs)
            print(f'macdaily-update: {yellow}pip{reset}: found broken dependencies: {bold}{pkgs}{reset}')
            if self._yes or self._quiet:
                return True
            while True:
                ans = input('Would you like to reinstall? (y/N)')
                if re.match(r'[yY]', ans):
                    return True
                elif re.match(r'[nN]', ans):
                    return False
                else:
                    print('Invalid input.')

        _deps_pkgs = _proc_check()
        if not _deps_pkgs:
            return

        if _proc_confirm():
            while _deps_pkgs:
                for package in _deps_pkgs:
                    argv = f'{argc} {package}'
                    script(['echo', '-e', f'\n+ {bold}{argv}{reset}'], self._log.name)
                    returncode = script(f"yes {self._password} | sudo --set-home --stdin --prompt='' {argv}",
                                        self._log.name, shell=True, timeout=self._timeout)
                    if returncode == 0:
                        with contextlib.suppress(ValueError):
                            self._pkgs.remove(re.split(r'[<>=!]', package, maxsplit=1)[0])
                    self._log.write('\n')
                _deps_pkgs = _proc_check()
            print(f'macdaily-update: {green}pip{reset}: all broken dependencies fixed')
        else:
            print(f'macdaily-update: {red}pip{reset}: all broken dependencies remain')

    def _proc_cleanup(self):
        if not self._cleanup:
            return

        args = ['pip', 'cleanup']
        if self._verbose:
            args.append('--verbose')
        if self._quiet:
            args.append('--quiet')
        argv = ' '.join(args)
        script(['echo', '-e', f'\n+ {bold}{argv}{reset}'], self._log.name)

        args = ['rm', '-rf']
        if self._verbose:
            args.append('-v')
        argc = ' '.join(args)
        for path in itertools.chain(glob.glob('/var/root/Library/Caches/pip/*/'),
                                    glob.glob(os.path.expanduser('~/Library/Caches/pip/*/'))):
            argv = f'{argc} {path}'
            script(['echo', '-e', f'++ {argv}'], self._log.name)
            script(f'yes {self._password} | sudo --stdin --prompt="" {argv}', self._log.name, shell=True)
