# -*- coding: utf-8 -*-

import re
import traceback

from macdaily.cmd.update import UpdateCommand
from macdaily.core.apm import ApmCommand
from macdaily.util.const import bold, reset
from macdaily.util.misc import date, print_info, print_scpt, print_text, run

try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess


class ApmUpdate(ApmCommand, UpdateCommand):

    def _parse_args(self, namespace):
        self._beta = namespace.pop('beta', False)

        self._all = namespace.pop('all', False)
        self._quiet = namespace.pop('quiet', False)
        self._verbose = namespace.pop('verbose', False)
        self._yes = namespace.pop('yes', False)

        self._logging_opts = namespace.pop('logging', str()).split()
        self._update_opts = namespace.pop('update', str()).split()

    def _check_pkgs(self, path):
        text = f'Listing installed {self.desc[1]}'
        print_info(text, self._file, redirect=self._vflag)

        argv = [path, 'list', '--bare', '--no-color']
        args = ' '.join(argv)
        print_scpt(args, self._file, redirect=self._vflag)
        with open(self._file, 'a') as file:
            file.write(f'Script started on {date()}\n')
            file.write(f'command: {args!r}\n')

        try:
            proc = subprocess.check_output(argv, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            print_text(traceback.format_exc(), self._file, redirect=self._vflag)
            _real_pkgs = set()
        else:
            context = proc.decode()
            print_text(context, self._file, redirect=self._vflag)

            _list_pkgs = list()
            for line in filter(None, context.strip().split('\n')):
                _list_pkgs.append(line.split('@')[0])
            _real_pkgs = set(_list_pkgs)
        finally:
            with open(self._file, 'a') as file:
                file.write(f'Script done on {date()}\n')

        text = 'Checking existence of specified packages'
        print_info(text, self._file, redirect=self._vflag)

        _temp_pkgs = list()
        _lost_pkgs = list()
        for package in self._packages:
            if package in _real_pkgs:
                _temp_pkgs.append(package)
            else:
                _lost_pkgs.append(package)

        self._tmp_real_pkgs = set(_real_pkgs)
        self._tmp_lost_pkgs = set(_lost_pkgs)
        self._tmp_temp_pkgs = set(_temp_pkgs)

    def _check_list(self, path):
        text = f'Checking outdated {self.desc[1]}'
        print_info(text, self._file, redirect=self._vflag)

        argv = [path, 'upgrade']
        argv.extend(self._logging_opts)
        argv.append('--no-color')
        argv.append('--no-json')
        argv.append('--list')
        args = ' '.join(argv)
        print_scpt(args, self._file, redirect=self._vflag)
        with open(self._file, 'a') as file:
            file.write(f'Script started on {date()}\n')
            file.write(f'command: {args!r}\n')
        try:
            proc = subprocess.check_output(argv, stderr=subprocess.DEVNULL)
        except subprocess.SubprocessError:
            print_text(traceback.format_exc(), self._file, redirect=self._vflag)
            self._tmp_temp_pkgs = set()
        else:
            context = proc.decode()
            print_text(context, self._file, redirect=self._vflag)

            _temp_pkgs = list()
            for line in filter(lambda s: '->' in s, context.strip().split('\n')):
                _temp_pkgs.append(re.sub(r'.* \(.*\)* .* -> .*', r'\1', line))
            self._tmp_temp_pkgs = set(_temp_pkgs)
        finally:
            with open(self._file, 'a') as file:
                file.write(f'Script done on {date()}\n')

    def _proc_update(self, path):
        argv = [path, 'upgrade']
        if self._yes:
            argv.append('--no-confirm')
        if self._verbose:
            argv.append('--verbose')
        if self._quiet:
            argv.append('--quiet')
        argv.extend(self._update_opts)
        argv.append('--no-list')
        argv.append('--no-json')

        argc = ' '.join(argv)
        for package in self._tmp_temp_pkgs:
            args = f'{argc} {package}'
            print_scpt(args, self._file, redirect=self._qflag)
            if self._yes:
                args = f"yes yes | {args}"
            if run(args, self._file, shell=True,
                   redirect=self._qflag, timeout=self._timeout):
                self._fail.append(package)
            else:
                self._pkgs.append(package)
        del self._tmp_temp_pkgs