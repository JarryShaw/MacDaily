# -*- coding: utf-8 -*-

import os
import textwrap
import time
import traceback

from macdaily.cmd.update import UpdateCommand
from macdaily.core.cask import CaskCommand
from macdaily.util.const import bold, length, reset
from macdaily.util.misc import script

try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess


class CaskUpdate(CaskCommand, UpdateCommand):

    def _parse_args(self, namespace):
        self._exhaust = namespace.pop('exhaust', False)
        self._force = namespace.pop('force', False)
        self._greedy = namespace.pop('greedy', False)
        self._merge = namespace.pop('merge', False)
        self._no_cleanup = namespace.pop('no_cleanup', False)

        self._all = namespace.pop('all', False)
        self._quiet = namespace.pop('quiet', False)
        self._verbose = namespace.pop('verbose', False)
        self._yes = namespace.pop('yes', False)

        self._logging_opts = namespace.pop('logging', str()).split()
        self._update_opts = namespace.pop('update', str()).split()

    def _check_pkgs(self, path):
        args = [path, 'cask', 'list']
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

        if self._exhaust:
            return self._exhaust_check(path)

        args = [path, 'cask', 'outdated']
        if self._quiet:
            args.append('--quiet')
        if self._verbose:
            args.append('--verbose')
        if self._greedy:
            args.append('--greedy')
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

    def _exhaust_check(self, path):
        args = ['brew', 'cask', 'outdated', '--exhaust']
        if self._quiet:
            args.append('--quiet')
        if self._verbose:
            args.append('--verbose')
        args.extend(self._logging_opts)
        self._log.write(f'+ {" ".join(args)}\n')

        args = [path, 'cask', 'list']
        if self._verbose:
            self._log.write(f'++ {" ".join(args)}')
        try:
            proc = subprocess.check_output(args, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            self._log.write(traceback.format_exc())
            _list_pkgs = set()
        else:
            context = proc.decode()
            if self._verbose:
                self._log.write(context)
            _list_pkgs = set(context.split())

        args = [path, '--prefix']
        if self._verbose:
            self._log.write(f'++ {" ".join(args)}')
        try:
            proc = subprocess.check_output(args, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            self._log.write(traceback.format_exc())
            self.__temp_pkgs = set()
            return
        else:
            context = proc.decode()
            if self._verbose:
                self._log.write(context)
            prefix = context.strip()

        _temp_pkgs = list()
        for cask in _list_pkgs:
            args = [path, 'cask', 'info', cask]
            if self._verbose:
                self._log.write(f'++ {" ".join(args)}')
            try:
                proc = subprocess.check_output(args, stderr=subprocess.DEVNULL)
            except subprocess.CalledProcessError:
                self._log.write(traceback.format_exc())
                continue

            context = proc.decode()
            if self._verbose:
                self._log.write(context)
            version = context.split(maxsplit=2)[1]

            installed = os.path.join(prefix, 'Caskroom', cask, version)
            if os.path.isdir(installed):
                _temp_pkgs.append(cask)

        self.__temp_pkgs = set(_temp_pkgs)
        if self._verbose:
            self._log.write(f'++ {path} cask outdated list\n')
        max_len = len(max(_temp_pkgs, key=lambda s: len(s)))
        context = '\n'.join(textwrap.wrap('    '.join(map(lambda s: s.ljust(max_len), self.__temp_pkgs)), length))
        self._log.write(f'{context}\n')

    def _proc_update(self, path):
        args = [path, 'cask', 'upgrade']
        if self._quiet:
            args.append('--quiet')
        if self._verbose:
            args.append('--verbose')
        if self._greedy:
            args.append('--greedy')
        if self._exhaust:
            args.append('--exhaust')
        args.extend(self._update_opts)

        args.append('')
        for package in self.__temp_pkgs:
            args[-1] = package
            argv = ' '.join(args)
            script(['echo', f'\n+ {bold}{argv}{reset}'], self._log.name)
            if script(args, self._log.name, timeout=self._timeout):
                self._fail.append(package)
            else:
                self._pkgs.append(package)
            self._log.write('\n')
        del self.__temp_pkgs
