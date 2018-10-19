# -*- coding: utf-8 -*-

import re
import traceback

from macdaily.cmd.update import UpdateCommand
from macdaily.core.system import SystemCommand
from macdaily.util.colour import bold, reset
from macdaily.util.tool import script

try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess


class SystemUpdate(SystemCommand, UpdateCommand):

    def _parse_args(self, namespace):
        self._recommend = namespace.pop('recommended', False)
        self._restart = namespace.pop('restart', False)

        self._all = namespace.pop('all', False)
        self._quiet = namespace.pop('quiet', False)
        self._yes = namespace.pop('yes', False)

        self._logging_opts = namespace.pop('logging', str()).split()
        self._update_opts = namespace.pop('update', str()).split()

    def _check_pkgs(self, path):
        self._check_list(path)

        _rcmd_pkgs = list()
        _none_pkgs = list()
        _lost_pkgs = list()
        for package in self._packages:
            if package in self.__rcmd_pkgs:
                _rcmd_pkgs.append(package)
            elif package in self.__none_pkgs:
                _none_pkgs.append(package)
            else:
                _lost_pkgs.append(package)
        self._lost.extend(_lost_pkgs)

        self.__real_pkgs = self.__rcmd_pkgs | self.__none_pkgs
        self.__lost_pkgs = set(_lost_pkgs)
        self.__rcmd_pkgs = set(_rcmd_pkgs)
        self.__none_pkgs = set(_none_pkgs)

    def _check_list(self, path):
        args = [path, '--list']
        args.extend(self._logging_opts)

        self._log.write(f'+ {" ".join(args)}\n')
        try:
            proc = subprocess.check_output(args, stderr=subprocess.DEVNULL)
        except subprocess.SubprocessError:
            self._log.write(traceback.format_exc())
            self.__rcmd_pkgs = set()
            self.__none_pkgs = set()
        else:
            context = proc.decode()
            self._log.write(context)

            _rcmd_pkgs = list()
            _none_pkgs = list()
            for package in filter(lambda s: re.match(r'^\W*[-*]', s), context.strip().split('\n')):
                flag, name = package.split(maxsplit=1)
                if flag == '*':
                    _rcmd_pkgs.append(name)
                if flag == '-':
                    _none_pkgs.append(name)

            self.__rcmd_pkgs = set(_rcmd_pkgs)
            self.__none_pkgs = set(_none_pkgs)
        finally:
            self._log.write('\n')

    def _proc_update(self, path):
        if self._recommend:
            _temp_pkgs = self.__rcmd_pkgs
        else:
            _temp_pkgs = self.__rcmd_pkgs | self.__none_pkgs

        args = [path, '--install', '--no-scan']
        if self._restart:
            args.append('--restart')
        if self._quiet:
            args.append('--quiet')
        args.extend(self._update_opts)

        argc = ' '.join(args)
        for package in _temp_pkgs:
            argv = f'{argc} {package}'
            script(['echo', '-e', f'\n+ {bold}{argv}{reset}'], self._log.name)
            if script(f"yes {self._password} | sudo --stdin --prompt='' {argv}",
                      self._log.name, shell=True, timeout=self._timeout):
                self._fail.append(package)
            else:
                self._pkgs.append(package)
            self._log.write('\n')
        del self.__rcmd_pkgs
        del self.__none_pkgs
