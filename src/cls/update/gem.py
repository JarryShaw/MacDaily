# -*- coding: utf-8 -*-

import traceback

from macdaily.cmd.update import UpdateCommand
from macdaily.core.gem import GemCommand
from macdaily.util.colour import bold, reset
from macdaily.util.const import SHELL
from macdaily.util.tool import script

try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess


class GemUpdate(GemCommand, UpdateCommand):

    def _parse_args(self, namespace):
        self._brew = namespace.pop('brew', False)
        self._system = namespace.pop('system', False)

        self._all = namespace.pop('all', False)
        self._quiet = namespace.pop('quiet', False)
        self._verbose = namespace.pop('verbose', False)
        self._yes = namespace.pop('yes', False)

        self._logging_opts = namespace.pop('logging', str()).split()
        self._update_opts = namespace.pop('update', str()).split()

    def _check_pkgs(self, path):
        args = [path, 'list', '--no-versions']
        try:
            proc = subprocess.check_output(args, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            _real_pkgs = set()
        else:
            _real_pkgs = set(proc.decode().split())

        _temp_pkgs = list()
        _lost_pkgs = list()
        for package in self._packages:
            if package in _real_pkgs:
                _temp_pkgs.append(package)
            else:
                _lost_pkgs.append(package)
        self._lost.extend(_lost_pkgs)

        self.__real_pkgs = set(_real_pkgs)
        self.__lost_pkgs = set(_lost_pkgs)
        self.__temp_pkgs = set(_temp_pkgs)

    def _check_list(self, path):
        args = [path, 'update', '--system']
        if self._quiet:
            args.append('--quiet')
        if self._verbose:
            args.append('--verbose')
        argv = ' '.join(args)
        script(['echo', '-e', f'\n+ {bold}{argv}{reset}'], self._log.name)
        script(f'yes {self._password} | sudo --stdin --prompt="" {argv}', self._log.name)

        args = [path, 'outdated']
        if self._quiet:
            args.append('--quiet')
        if self._verbose:
            args.append('--verbose')
        args.extend(self._logging_opts)
        args.append('--no-versions')

        self._log.write(f'+ {" ".join(args)}\n')
        try:
            proc = subprocess.check_output(args, stderr=subprocess.DEVNULL)
        except subprocess.SubprocessError:
            self._log.write(traceback.format_exc())
            self.__temp_pkgs = set()
        else:
            context = proc.decode()
            self._log.write(context)
            self.__temp_pkgs = set(map(lambda s: s.split()[0], context.strip().split('\n')))
        finally:
            self._log.write('\n')

    def _proc_update(self, path):
        args = [path, 'update']
        if self._quiet:
            args.append('--quiet')
        if self._verbose:
            args.append('--verbose')
        args.extend(self._update_opts)

        argc = ' '.join(args)
        for package in self.__temp_pkgs:
            argv = f'{argc} {package}'
            script(['echo', '-e', f'\n+ {bold}{argv}{reset}'], self._log.name)
            if self._yes:
                argv = f'yes y | {argv}'
            if script(f'yes {self._password} | sudo --stdin --prompt="" {SHELL} -c {argv!r}',
                      self._log.name, shell=True, timeout=self._timeout):
                self._fail.append(package)
            else:
                self._pkgs.append(package)
            self._log.write('\n')
        del self.__temp_pkgs
