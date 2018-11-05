# -*- coding: utf-8 -*-

import traceback

from macdaily.cmd.uninstall import UninstallCommand
from macdaily.core.pip import PipCommand
from macdaily.util.const import reset, under
from macdaily.util.misc import date, print_info, print_scpt, print_text, sudo

try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess


class PipUninstall(PipCommand, UninstallCommand):

    def _parse_args(self, namespace):
        self._brew = namespace.pop('brew', False)
        self._cpython = namespace.pop('cpython', False)
        self._ignore_deps = namespace.pop('ignore_dependencies', False)
        self._pre = namespace.pop('pre', False)
        self._pypy = namespace.pop('pypy', False)
        self._system = namespace.pop('system', False)

        self._all = namespace.pop('all', False)
        self._quiet = namespace.pop('quiet', False)
        self._verbose = namespace.pop('verbose', False)
        self._yes = namespace.pop('yes', False)

        self._logging_opts = namespace.pop('logging', str()).split()
        self._uninstall_opts = namespace.pop('uninstall', str()).split()

    def _check_list(self, path):
        argv = [path, 'freeze']
        argv.extend(self._logging_opts)

        text = f'Checking outdated {self.desc[1]}'
        print_info(text, self._file, redirect=self._vflag)

        try:
            proc = subprocess.check_output(argv, stderr=subprocess.DEVNULL)
        except subprocess.SubprocessError:
            print_text(traceback.format_exc(), self._file, redirect=self._vflag)
            self._var__temp_pkgs = set()
        else:
            context = proc.decode()
            print_text(context, self._file, redirect=self._qflag)

            _temp_pkgs = list()
            for line in filter(None, context.strip().split('\n')):
                _temp_pkgs.append(line.split('==')[0])
            self._var__temp_pkgs = set(_temp_pkgs)
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

            argv = [path, '-m', 'pip', 'show', package]
            args = ' '.join(argv)
            print_scpt(args, self._file, redirect=self._vflag)
            with open(self._file, 'a') as file:
                file.write(f'Script started on {date()}\n')
                file.write(f'command: {args!r}\n')

            _temp_pkgs = set()
            try:
                proc = subprocess.check_output(argv, stderr=subprocess.DEVNULL)
            except subprocess.CalledProcessError:
                print_text(traceback.format_exc(), self._file, redirect=self._vflag)
            else:
                context = proc.decode()
                print_text(context, self._file, redirect=self._vflag)

                for line in filter(lambda s: s.startswith('Requires: '), context.strip().split('\n')):
                    _temp_pkgs = set(map(lambda s: s.rstrip(','), line.split()[1:]))
                    _deps_pkgs |= _temp_pkgs
                    break
            finally:
                with open(self._file, 'a') as file:
                    file.write(f'Script done on {date()}\n')

            for package in _temp_pkgs:
                if package in ('pip', 'wheel', 'setuptools'):
                    continue
                _deps_pkgs |= _proc_dependency(package)
            return _deps_pkgs

        argv = [path, '-m', 'pip', 'uninstall']
        if self._yes:
            argv.append('--yes')
        if self._quiet:
            argv.append('--quiet')
        if self._verbose:
            argv.append('--verbose')
        argv.extend(self._uninstall_opts)

        argv.append('')
        for item in self._var__temp_pkgs:
            for package in _proc_dependency(item):
                if package in self._ignore:
                    continue
                if package in ('pip', 'wheel', 'setuptools'):
                    continue
                argv[-1] = package
                print_scpt(' '.join(argv), self._file, redirect=self._qflag)
                if sudo(argv, self._file, self._password, sethome=True,
                        timeout=self._timeout, redirect=self._qflag, verbose=self._vflag):
                    self._fail.append(package)
                else:
                    self._pkgs.append(package)
        del self._var__temp_pkgs
