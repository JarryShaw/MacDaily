# -*- coding: utf-8 -*-

import contextlib
import copy
import json
import re
import traceback

from macdaily.cmd.update import UpdateCommand
from macdaily.core.pip import PipCommand
from macdaily.util.colour import bold, green, red, reset, yellow
from macdaily.util.tool import script

try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess


class PipUpdate(PipCommand, UpdateCommand):

    def _parse_args(self, namespace):
        self._brew = namespace.pop('brew', False)
        self._cpython = namespace.pop('cpython', False)
        self._no_cleanup = namespace.pop('no_cleanup', False)
        self._pre = namespace.pop('pre', False)
        self._pypy = namespace.pop('pypy', False)
        self._system = namespace.pop('system', False)

        self._all = namespace.pop('all', False)
        self._quiet = namespace.pop('quiet', False)
        self._verbose = namespace.pop('verbose', False)
        self._yes = namespace.pop('yes', False)

        self._logging_opts = namespace.pop('logging', str()).split()
        self._update_opts = namespace.pop('update', str()).split()

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
            proc = subprocess.check_output(args, stderr=subprocess.DEVNULL)
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
                proc = subprocess.check_output([path], '-m', 'pip', 'check', stderr=subprocess.DEVNULL)
            except subprocess.SubprocessError:
                return set()

            _deps_pkgs = list()
            for line in filter(None, proc.decode().strip().split('\n')):
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
            args = [path, '-m', 'pip', 'reinstall']
            if self._quiet:
                args.append('--quiet')
            if self._verbose:
                args.append('--verbose')

            while _deps_pkgs:
                for package in _deps_pkgs:
                    real_name = re.split(r'[<>=!]', package, maxsplit=1)[0]
                    script(['echo', '-e', f'\n+ {bold}{" ".join(args)} {package}{reset}'], self._log.name)

                    args[3] = 'uninstall'
                    script(['echo', '-e', f'++ {bold}{" ".join(args)} {real_name}{reset}'], self._log.name)
                    script(f'yes {self._password} | sudo --set-home --stdin --prompt="" '
                           f'{path} -m pip uninstall {real_name} --yes', self._log.name, shell=True)

                    args[3] = 'install'
                    script(['echo', '-e', f'++ {bold}{" ".join(args)} {package}{reset}'], self._log.name)
                    if not script(f'yes {self._password} | sudo --set-home --stdin --prompt="" '
                                  f'{path} -m pip install {package}', self._log.name,
                                  shell=True, timeout=self._timeout):
                        with contextlib.suppress(ValueError):
                            self._pkgs.remove(real_name)
                    self._log.write('\n')
                _deps_pkgs = _proc_check()
            print(f'macdaily-update: {green}pip{reset}: all broken dependencies fixed')
        else:
            print(f'macdaily-update: {red}pip{reset}: all broken dependencies remain')
