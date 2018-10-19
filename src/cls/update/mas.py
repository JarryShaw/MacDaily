# -*- coding: utf-8 -*-

import shutil
import sys
import traceback

from macdaily.cmd.update import UpdateCommand
from macdaily.util.colour import blush, bold, flash, red, reset
from macdaily.util.tool import script

try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess


class MasUpdate(UpdateCommand):

    @property
    def mode(self):
        return 'mas'

    @property
    def name(self):
        return 'Mac App Store CLI'

    @property
    def desc(self):
        return ('macOS application', 'macOS applications')

    def _check_exec(self):
        self.__exec_path = shutil.which('mas')
        flag = (self.__exec_path is None)
        if flag:
            print(f'macdaily-update: {blush}{flash}mas{reset}: command not found', file=sys.stderr)
            print(f'macdaily-update: {red}mas{reset}: you may download MAS through following command -- '
                  f"`{bold}brew install mas{reset}'\n")
        return flag

    def _parse_args(self, namespace):
        self._all = namespace.pop('all', False)
        self._quiet = namespace.pop('quiet', False)
        self._show_log = namespace.pop('show_log', False)
        self._yes = namespace.pop('yes', False)

        self._logging_opts = namespace.pop('logging', str()).split()
        self._update_opts = namespace.pop('update', str()).split()

    def _loc_exec(self):
        self._exec = {self.__exec_path}
        del self.__exec_path

    def _check_pkgs(self, path):
        args = [path, 'list']
        try:
            proc = subprocess.check_output(args, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            _real_pkgs = set()
        else:
            _list_pkgs = dict()
            for line in proc.decode().strip().split('\n'):
                context = line.split()
                _list_pkgs[context[1:-1]] = context[0]
            _real_pkgs = set(_list_pkgs.keys())

        _temp_pkgs = list()
        _lost_pkgs = list()
        for package in self._packages:
            if package in _real_pkgs:
                _temp_pkgs.append((_list_pkgs[package], package))
            else:
                _lost_pkgs.append(package)
        self._lost.extend(_lost_pkgs)

        self.__real_pkgs = set(_real_pkgs)
        self.__lost_pkgs = set(_lost_pkgs)
        self.__temp_pkgs = set(_temp_pkgs)

    def _check_list(self, path):
        args = [path, 'outdated']
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
                content = line.split()
                _temp_pkgs.append((content[0], content[1:-1]))
            self.__temp_pkgs = set(_temp_pkgs)
        finally:
            self._log.write('\n')

    def _proc_update(self, path):
        args = [path, 'upgrade']
        args.append(self._update_opts)

        argc = ' '.join(args)
        for (code, package) in self.__temp_pkgs:
            argv = f'{argc} {code}'
            script(['echo', '-e', f'\n+ {bold}{argc} {package} [{code}]{reset}'], self._log.name)
            if script(f"yes {self._password} | sudo --stdin --prompt='' {argv}",
                      self._log.name, shell=True, timeout=self._timeout):
                self._fail.append(package)
            else:
                self._pkgs.append(package)
            self._log.write('\n')
        del self.__temp_pkgs
