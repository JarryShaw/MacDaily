# -*- coding: utf-8 -*-

import glob
import os
import shutil
import sys
import traceback

from macdaily.cmd.update.command import UpdateCommand
from macdaily.util.colours import blush, bold, flash, purple, red, reset, under
from macdaily.util.helpers import SHELL
from macdaily.util.tools import script

try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess


class GemUpdate(UpdateCommand):

    @property
    def mode(self):
        return 'gem'

    @property
    def name(self):
        return 'RubyGems'

    @property
    def desc(self):
        return ('Ruby gem', 'Ruby gems')

    def _check_exec(self):
        self.__exec_path = shutil.which('gem')
        flag = (self.__exec_path is None)
        if flag:
            print(f'update: {blush}{flash}gem{reset}: command not found\n', file=sys.stderr)
            print(f'update: {red}gem{reset}: you may download RubyGems from '
                  f'{purple}{under}https://rubygems.org{reset}\n')
        return flag

    def _parse_args(self, namespace):
        self._all = namespace.pop('all', False)
        self._brew = namespace.pop('brew', False)
        self._quiet = namespace.pop('quiet', False)
        self._show_log = namespace.pop('show_log', False)
        self._system = namespace.pop('system', False)
        self._verbose = namespace.pop('verbose', False)
        self._yes = namespace.pop('yes', False)

        self._logging_opts = namespace.pop('logging', str()).split()
        self._update_opts = namespace.pop('update', str()).split()

    def _loc_exec(self):
        if not (self._brew and self._system):
            self._exec = {self.__exec_path}
        else:
            _exec_path = list()
            if self._brew:
                try:
                    proc = subprocess.check_output(['brew', '--prefix'], stderr=subprocess.DEVNULL)
                except subprocess.CalledProcessError:
                    prefix = '/usr/local'
                else:
                    prefix = proc.decode().strip()

                _glob_path = glob.glob(os.path.join(prefix, 'Cellar/ruby/*/bin/gem'))
                _glob_path.sort(reverse=True)
                _exec_path.append(_glob_path[0])
            if self._system and os.path.exists('/usr/bin/gem'):
                _exec_path.append('/usr/bin/gem')
            self._exec = set(_exec_path)
        del self.__exec_path

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
