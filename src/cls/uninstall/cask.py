# -*- coding: utf-8 -*-

import traceback

from macdaily.cmd.uninstall import UninstallCommand
from macdaily.core.cask import CaskCommand
from macdaily.util.misc import date, print_info, print_scpt, print_text, run

try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess


class CaskUninstall(CaskCommand, UninstallCommand):

    def _parse_args(self, namespace):
        self._dry_run = namespace.pop('dry_run', False)
        self._force = namespace.pop('force', False)

        self._all = namespace.pop('all', False)
        self._quiet = namespace.pop('quiet', False)
        self._verbose = namespace.pop('verbose', False)
        self._yes = namespace.pop('yes', False)

        self._logging_opts = namespace.pop('logging', str()).split()
        self._uninstall_opts = namespace.pop('uninstall', str()).split()

    def _check_pkgs(self, path):
        super()._check_pkgs(path)

        if self._force:
            self._var__temp_pkgs |= self._var__lost_pkgs
            self._var__lost_pkgs = set()

    def _check_list(self, path):
        text = f'Checking installed {self.desc[1]}'
        print_info(text, self._file, redirect=self._vflag)

        argv = [path, 'cask', 'list']
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
            self._var__temp_pkgs = set()
        else:
            context = proc.decode()
            self._var__temp_pkgs = set(context.strip().split())
            print_text(context, self._file, redirect=self._vflag)
        finally:
            with open(self._file, 'a') as file:
                file.write(f'Script done on {date()}\n')

    def _proc_uninstall(self, path):
        text = f'Uninstalling specified {self.desc[1]}'
        print_info(text, self._file, redirect=self._qflag)

        argv = [path, 'cask', 'uninstall']
        if self._force:
            argv.append('--force')
        if self._quiet:
            argv.append('--quiet')
        if self._verbose:
            argv.append('--verbose')
        if self._dry_run:
            argv.append('--dry-run')
        argv.extend(self._uninstall_opts)

        argv.append('')
        for package in self._var__temp_pkgs:
            argv[-1] = package
            print_scpt(' '.join(argv), self._file, redirect=self._qflag)
            if self._dry_run:
                continue
            if run(argv, self._file, timeout=self._timeout,
                   redirect=self._qflag, verbose=self._vflag):
                self._fail.append(package)
            else:
                self._pkgs.append(package)
        del self._var__temp_pkgs
