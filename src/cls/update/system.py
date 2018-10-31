# -*- coding: utf-8 -*-

import os
import re
import traceback

from macdaily.cmd.update import UpdateCommand
from macdaily.core.system import SystemCommand
from macdaily.util.const import bold, reset
from macdaily.util.misc import date, print_info, print_scpt, print_text, sudo

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
        self._verbose = namespace.pop('verbose', False)
        self._yes = namespace.pop('yes', False)

        self._logging_opts = namespace.pop('logging', str()).split()
        self._update_opts = namespace.pop('update', str()).split()

    def _check_pkgs(self, path):
        self._check_list(path)
        text = 'Checking existence of specified packages'
        print_info(text, self._file, redirect=self._vflag)

        _rcmd_pkgs = list()
        _norm_pkgs = list()
        _lost_pkgs = list()
        for package in self._packages:
            if package in self._tmp_rcmd_pkgs:
                _rcmd_pkgs.append(package)
            elif package in self._tmp_norm_pkgs:
                _norm_pkgs.append(package)
            else:
                _lost_pkgs.append(package)
        self._lost.extend(_lost_pkgs)

        self._tmp_real_pkgs = self._tmp_rcmd_pkgs | self._tmp_norm_pkgs
        self._tmp_lost_pkgs = set(_lost_pkgs)
        self._tmp_rcmd_pkgs = set(_rcmd_pkgs)
        self._tmp_norm_pkgs = set(_norm_pkgs)
        self._tmp_temp_pkgs = self._tmp_rcmd_pkgs | self._tmp_norm_pkgs

    def _check_list(self, path):
        text = f'Checking outdated {self.desc[1]}'
        print_info(text, self._file, redirect=self._vflag)

        argv = [path, '--list']
        argv.extend(self._logging_opts)
        args = ' '.join(argv)
        print_scpt(args, self._file, redirect=self._vflag)
        with open(self._file, 'a') as file:
            file.write(f'Script started on {date()}\n')
            file.write(f'command: {args!r}\n')
        try:
            proc = subprocess.check_output(argv, stderr=subprocess.DEVNULL)
        except subprocess.SubprocessError:
            print_text(traceback.format_exc(), self._file, redirect=self._vflag)
            self._tmp_rcmd_pkgs = set()
            self._tmp_norm_pkgs = set()
        else:
            context = proc.decode()
            print_text(context, self._file, redirect=self._vflag)

            _rcmd_pkgs = list()
            _norm_pkgs = list()
            for package in filter(lambda s: re.match(r'^\W*[-*]', s), context.strip().split('\n')):
                flag, name = package.split(maxsplit=1)
                if flag == '*':
                    _rcmd_pkgs.append(name)
                if flag == '-':
                    _norm_pkgs.append(name)

            self._tmp_rcmd_pkgs = set(_rcmd_pkgs)
            self._tmp_norm_pkgs = set(_norm_pkgs)
        finally:
            with open(self._file, 'a') as file:
                file.write(f'Script done on {date()}\n')
        self._tmp_temp_pkgs = self._tmp_rcmd_pkgs | self._tmp_norm_pkgs

    def _proc_update(self, path):
        if self._tmp_temp_pkgs:
            if self._recommend:
                _temp_pkgs = self._tmp_rcmd_pkgs
            else:
                _temp_pkgs = self._tmp_rcmd_pkgs | self._tmp_norm_pkgs
        else:
            _temp_pkgs = set()

        argv = [path, '--install', '--no-scan']
        if self._restart:
            argv.append('--restart')
        if self._quiet:
            argv.append('--quiet')
        argv.extend(self._update_opts)

        text = f'Upgrading outdated {self.desc[1]}'
        print_info(text, self._file, redirect=self._qflag)

        argc = ' '.join(argv)
        for package in _temp_pkgs:
            args = f'{argc} {package!r}'
            print_scpt(args, self._file, redirect=self._qflag)
            if sudo(args, self._file, askpass=self._askpass,
                    timeout=self._timeout, redirect=self._qflag):
                self._fail.append(package)
            else:
                self._pkgs.append(package)
        del self._tmp_rcmd_pkgs
        del self._tmp_norm_pkgs
        del self._tmp_temp_pkgs
