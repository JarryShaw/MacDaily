# -*- coding: utf-8 -*-

import re
import shutil
import sys
import traceback

from macdaily.cmd.update.command import UpdateCommand
from macdaily.util.colours import blush, bold, flash, purple, red, reset, under
from macdaily.util.tools import script

try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess


class ApmUpdate(UpdateCommand):

    @property
    def mode(self):
        return 'apm'

    @property
    def name(self):
        return 'Atom Package Manager'

    @property
    def desc(self):
        return ('Atom plug-in', 'Atom plug-ins')

    def _check_exec(self):
        self.__exec_path = (shutil.which('apm'), shutil.which('apm-beta'))
        flag = (self.__exec_path == (None, None))
        if flag:
            print(f'macdaily-update: {blush}{flash}apm{reset}: command not found', file=sys.stderr)
            print(f'macdaily-update: {red}apm{reset}: you may download Atom from '
                  f'{purple}{under}https://atom.io{reset}\n')
        return flag

    def _pkg_args(self, args):
        if self._beta and self.__exec_path[1] is None:
            return True
        return super()._pkg_args(args)

    def _parse_args(self, namespace):
        self._all = namespace.pop('all', False)
        self._beta = namespace.pop('beta', False)
        self._quiet = namespace.pop('quiet', False)
        self._show_log = namespace.pop('show_log', False)
        self._verbose = namespace.pop('verbose', False)
        self._yes = namespace.pop('yes', False)

        self._logging_opts = namespace.pop('logging', str()).split()
        self._update_opts = namespace.pop('update', str()).split()

    def _loc_exec(self):
        if self._beta:
            if self.__exec_path[1] is None:
                self._exec = set()
            else:
                self._exec = {self.__exec_path[1]}
        else:
            self._exec = set(filter(None, self.__exec_path))
        del self.__exec_path

    def _check_pkgs(self, path):
        args = [path, 'list', '--bare', '--no-color']
        try:
            proc = subprocess.check_output(args, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            _real_pkgs = set()
        else:
            _list_pkgs = list()
            for line in filter(None, proc.decode().strip().split('\n')):
                _list_pkgs.append(line.split('@')[0])
            _real_pkgs = set(_list_pkgs)

        _temp_pkgs = list()
        _lost_pkgs = list()
        for package in self._packages:
            if package in _real_pkgs:
                _temp_pkgs.append(package)
            else:
                _lost_pkgs.append(package)

        self.__real_pkgs = set(_real_pkgs)
        self.__lost_pkgs = set(_lost_pkgs)
        self.__temp_pkgs = set(_temp_pkgs)

    def _check_list(self, path):
        args = [path, 'upgrade']
        args.extend(self._logging_opts)
        args.append('--no-color')
        args.append('--no-json')
        args.append('--list')

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
            for line in filter(lambda s: '->' in s, context.strip().split('\n')):
                _temp_pkgs.append(re.sub(r'.* \(.*\)* .* -> .*', r'\1', line))
            self.__temp_pkgs = set(_temp_pkgs)
        finally:
            self._log.write('\n')

    def _proc_update(self, path):
        args = [path, 'upgrade']
        if self._yes:
            args.append('--no-confirm')
        if self._verbose:
            args.append('--verbose')
        if self._quiet:
            args.append('--quiet')
        args.extend(self._update_opts)
        args.append('--no-list')
        args.append('--no-json')

        argc = ' '.join(args)
        for package in self.__temp_pkgs:
            argv = f'{argc} {package}'
            script(['echo', '-e', f'\n+ {bold}{argv}{reset}'], self._log.name)
            if self._yes:
                argv = f"yes yes | {argv}"
            if script(argv, self._log.name, shell=True, timeout=self._timeout):
                self._fail.append(package)
            else:
                self._pkgs.append(package)
            self._log.write('\n')
        del self.__temp_pkgs
