# -*- coding: utf-8 -*-

import copy
import traceback

from macdaily.cmd.uninstall import UninstallCommand
from macdaily.core.brew import BrewCommand
from macdaily.util.const import reset, under
from macdaily.util.misc import date, print_info, print_scpt, print_text, run

try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess


class BrewUninstall(BrewCommand, UninstallCommand):

    def _parse_args(self, namespace):
        self._dry_run = namespace.pop('dry_run', False)
        self._force = namespace.pop('force', False)
        self._ignore_deps = namespace.pop('ignore_dependencies', False)
        self._include_build = namespace.pop('include_build', False)
        self._include_optional = namespace.pop('include_optional', False)
        self._include_requirements = namespace.pop('include_requirements', False)
        self._include_test = namespace.pop('include_test', False)
        self._skip_recommended = namespace.pop('skip_recommended', False)

        self._all = namespace.pop('all', False)
        self._quiet = namespace.pop('quiet', False)
        self._verbose = namespace.pop('verbose', False)
        self._yes = namespace.pop('yes', False)

        self._logging_opts = namespace.pop('logging', str()).split()
        self._uninstall_opts = namespace.pop('uninstall', str()).split()

    def _check_list(self, path):
        text = f'Checking installed {self.desc[1]}'
        print_info(text, self._file, redirect=self._vflag)

        argv = [path, 'list']
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

        def _proc_dependency(package):
            _deps_pkgs = [package]
            if self._ignore_deps:
                return _deps_pkgs

            text = f'Searching dependencies of {self.desc[0]} {under}{package}{reset}'
            print_info(text, self._file, redirect=self._vflag)

            argv = [path, 'deps', '--installed', '-n']
            if self._include_build:
                argv.append('--include-build')
            if self._include_optional:
                argv.append('--include-optional')
            if self._include_test:
                argv.append('--include-test')
            if self._skip_recommended:
                argv.append('--skip-recommended')
            if self._include_requirements:
                argv.append('--include-requirements')
            argv.append(package)

            args = ' '.join(argv)
            print_scpt(args, self._file, redirect=self._vflag)
            with open(self._file, 'a') as file:
                file.write(f'Script started on {date()}\n')
                file.write(f'command: {args!r}\n')

            try:
                proc = subprocess.check_output(argv, stderr=subprocess.DEVNULL)
            except subprocess.CalledProcessError:
                print_text(traceback.format_exc(), self._file, redirect=self._vflag)
            else:
                context = proc.decode()
                _deps_pkgs.extend(reversed(context.strip().split()))
                print_text(context, self._file, redirect=self._vflag)
            finally:
                with open(self._file, 'a') as file:
                    file.write(f'Script done on {date()}\n')
            return _deps_pkgs

        argv = [path, 'uninstall']
        if self._force:
            argv.append('--force')
        if self._quiet:
            argv.append('--quiet')
        if self._verbose:
            argv.append('--verbose')
        if self._dry_run:
            argv.append('--dry-run')
        argv.extend(self._uninstall_opts)

        temp = copy.copy(argv)
        if self._ignore_deps:
            temp.append('--ignore-dependencies')
        args = ' '.join(temp)
        argv.append('--ignore-dependencies')

        argv.append('')
        _done_pkgs = list()
        for item in self._var__temp_pkgs:
            if item in _done_pkgs:
                continue
            for package in _proc_dependency(item):
                if package in self._ignore:
                    continue
                if package in _done_pkgs:
                    continue
                _done_pkgs.append(package)
                argv[-1] = package
                print_scpt(f'{args} {package}', self._file, redirect=self._qflag)
                if self._dry_run:
                    continue
                if run(argv, self._file, timeout=self._timeout,
                       redirect=self._qflag, verbose=self._vflag):
                    self._fail.append(package)
                else:
                    self._pkgs.append(package)
        del self._var__temp_pkgs
