# -*- coding: utf-8 -*-

import time
import traceback

from macdaily.cmd.update import UpdateCommand
from macdaily.core.brew import BrewCommand
from macdaily.util.colour import bold, reset
from macdaily.util.tool import script

try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess


class BrewUpdate(BrewCommand, UpdateCommand):

    def _parse_args(self, namespace):
        self._force = namespace.pop('force', False)
        self._merge = namespace.pop('merge', False)
        self._no_cleanup = namespace.pop('no_cleanup', False)

        self._all = namespace.pop('all', False)
        self._quiet = namespace.pop('quiet', False)
        self._verbose = namespace.pop('verbose', False)
        self._yes = namespace.pop('yes', False)

        self._logging_opts = namespace.pop('logging', str()).split()
        self._update_opts = namespace.pop('update', str()).split()

    def _check_pkgs(self, path):
        args = [path, 'list']
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
        if (self._brew_renew is None or
                time.time() - self._brew_renew >= 300):
            self._proc_renew(path)
            self._brew_renew = time.time()

        args = [path, 'outdated']
        if self._quiet:
            args.append('--quiet')
        if self._verbose:
            args.append('--verbose')
        args.extend(self._logging_opts)

        self._log.write(f'+ {" ".join(args)}\n')
        try:
            proc = subprocess.check_output(args, stderr=subprocess.DEVNULL)
        except subprocess.SubprocessError:
            self._log.write(traceback.format_exc())
            self.__temp_pkgs = set()
        else:
            context = proc.decode()
            self._log.write(context)

            _temp_pkgs = list()
            for line in context.strip().split('\n'):
                _temp_pkgs.append(line.split(maxsplit=1)[0])
            self.__temp_pkgs = set(_temp_pkgs)
        finally:
            self._log.write('\n')

    def _proc_update(self, path):
        args = [path, 'upgrade']
        if self._quiet:
            args.append('--quiet')
        if self._verbose:
            args.append('--verbose')
        args.extend(self._update_opts)

        args.append('')
        for package in self.__temp_pkgs:
            args[-1] = package
            argv = ' '.join(args)
            script(['echo', '-e', f'\n+ {bold}{argv}{reset}'], self._log.name)
            if script(args, self._log.name, timeout=self._timeout):
                self._fail.append(package)
            else:
                self._pkgs.append(package)
            self._log.write('\n')
        del self.__temp_pkgs
