# -*- coding: utf-8 -*-

import sys
import traceback

from macdaily.cmd.uninstall import UninstallCommand
from macdaily.core.cask import CaskCommand
from macdaily.util.misc import (date, make_stderr, print_info, print_scpt,
                                print_text, run)

if sys.version_info[:2] == (3, 4):
    import subprocess32 as subprocess
else:
    import subprocess


class CaskUninstall(CaskCommand, UninstallCommand):

    def _parse_args(self, namespace):
        self._dry_run = namespace.get('dry_run', False)
        self._force = namespace.get('force', False)
        self._no_cleanup = namespace.get('no_cleanup', False)

        self._all = namespace.get('all', False)
        self._quiet = namespace.get('quiet', False)
        self._verbose = namespace.get('verbose', False)
        self._yes = namespace.get('yes', False)

        self._logging_opts = namespace.get('logging', str()).split()
        self._uninstall_opts = namespace.get('uninstall', str()).split()

    def _check_pkgs(self, path):
        if self._force:
            self._var__temp_pkgs = self._packages
            self._var__lost_pkgs = set()
        else:
            super()._check_pkgs(path)

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
            proc = subprocess.check_output(argv, stderr=make_stderr(self._vflag))
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
        askpass = f'SUDO_ASKPASS={self._askpass!r}'
        for package in self._var__temp_pkgs:
            argv[-1] = package
            print_scpt(' '.join(argv), self._file, redirect=self._qflag)
            if self._dry_run:
                continue
            if run(argv, self._file, shell=True, timeout=self._timeout,
                   redirect=self._qflag, verbose=self._vflag, prefix=askpass):
                self._fail.append(package)
            else:
                self._pkgs.append(package)
        del self._var__temp_pkgs
