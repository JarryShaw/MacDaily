# -*- coding: utf-8 -*-

import sys
import traceback

from macdaily.cmd.uninstall import UninstallCommand
from macdaily.core.pip import PipCommand
from macdaily.util.const import reset, under
from macdaily.util.misc import (date, make_stderr, print_info, print_scpt,
                                print_text, sudo)

try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess


class PipUninstall(PipCommand, UninstallCommand):

    def _parse_args(self, namespace):
        self._brew = namespace.get('brew', False)
        self._cpython = namespace.get('cpython', False)
        self._dry_run = namespace.get('dry_run', False)
        self._ignore_deps = namespace.get('ignore_dependencies', False)
        self._pre = namespace.get('pre', False)
        self._pypy = namespace.get('pypy', False)
        self._system = namespace.get('system', False)

        self._all = namespace.get('all', False)
        self._quiet = namespace.get('quiet', False)
        self._verbose = namespace.get('verbose', False)
        self._yes = namespace.get('yes', False)

        self._logging_opts = namespace.get('logging', str()).split()
        self._uninstall_opts = namespace.get('uninstall', str()).split()

    def _check_list(self, path):
        argv = [path, '-m', 'pip', 'freeze']
        argv.extend(self._logging_opts)

        text = 'Checking outdated {}'.format(self.desc[1])
        print_info(text, self._file, redirect=self._vflag)

        stderr = make_stderr(self._vflag, sys.stderr)
        try:
            proc = subprocess.check_output(argv, stderr=stderr)
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
                file.write('Script done on {}\n'.format(date()))

    def _proc_uninstall(self, path):
        text = 'Uninstalling specified {}'.format(self.desc[1])
        print_info(text, self._file, redirect=self._qflag)

        def _proc_dependency(package, _know_pkgs):
            _deps_pkgs = {package}
            if self._ignore_deps:
                return _deps_pkgs

            text = 'Searching dependencies of {} {}{}{}'.format(self.desc[0], under, package, reset)
            print_info(text, self._file, redirect=self._vflag)

            argv = [path, '-m', 'pip', 'show', package]
            args = ' '.join(argv)
            print_scpt(args, self._file, redirect=self._vflag)
            with open(self._file, 'a') as file:
                file.write('Script started on {}\n'.format(date()))
                file.write('command: {!r}\n'.format(args))

            _temp_pkgs = set()
            stderr = make_stderr(self._vflag, sys.stderr)
            try:
                proc = subprocess.check_output(argv, stderr=stderr)
            except subprocess.CalledProcessError:
                print_text(traceback.format_exc(), self._file, redirect=self._vflag)
            else:
                context = proc.decode()
                print_text(context, self._file, redirect=self._vflag)

                for line in filter(lambda s: s.startswith('Requires: '), context.strip().split('\n')):
                    _temp_pkgs = set(map(lambda s: s.rstrip(','), line.split()[1:])) - _know_pkgs
                    _deps_pkgs |= _temp_pkgs
                    break
            finally:
                with open(self._file, 'a') as file:
                    file.write('Script done on {}\n'.format(date()))

            for package in _temp_pkgs:
                _temp_pkgs = _proc_dependency(package, _know_pkgs)
                _deps_pkgs |= _temp_pkgs
                _know_pkgs |= _temp_pkgs
            return _deps_pkgs

        argv = [path, '-m', 'pip', 'uninstall', '--yes']
        if self._quiet:
            argv.append('--quiet')
        if self._verbose:
            argv.append('--verbose')
        if self._dry_run:
            argv.append('--dry-run')
        argv.extend(self._uninstall_opts)

        argv.append('')
        _done_pkgs = set()
        _know_pkgs = self._ignore | {'pip', 'wheel', 'setuptools'}
        for item in self._var__temp_pkgs:
            _deps_pkgs = _proc_dependency(item, _know_pkgs)
            _know_pkgs |= _deps_pkgs
            for package in (_deps_pkgs - _done_pkgs):
                argv[-1] = package
                print_scpt(' '.join(argv), self._file, redirect=self._qflag)
                if self._dry_run:
                    continue
                if sudo(argv, self._file, self._password, sethome=True,
                        timeout=self._timeout, redirect=self._qflag, verbose=self._vflag):
                    self._fail.append(package)
                else:
                    self._pkgs.append(package)
            _done_pkgs |= _deps_pkgs
        del self._var__temp_pkgs
