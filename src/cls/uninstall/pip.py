# -*- coding: utf-8 -*-

import traceback

from macdaily.cmd.uninstall import UninstallCommand
from macdaily.core.pip import PipCommand
from macdaily.util.compat import subprocess
from macdaily.util.const.term import reset, under
from macdaily.util.tools.make import make_stderr
from macdaily.util.tools.misc import date
from macdaily.util.tools.print import print_info, print_scpt, print_text
from macdaily.util.tools.script import sudo


class PipUninstall(PipCommand, UninstallCommand):

    def _parse_args(self, namespace):
        self._brew = namespace.get('brew', False)  # pylint: disable=attribute-defined-outside-init
        self._cpython = namespace.get('cpython', False)  # pylint: disable=attribute-defined-outside-init
        self._dry_run = namespace.get('dry_run', False)  # pylint: disable=attribute-defined-outside-init
        self._ignore_deps = namespace.get('ignore_dependencies', False)  # pylint: disable=attribute-defined-outside-init
        self._no_cleanup = namespace.get('no_cleanup', False)  # pylint: disable=attribute-defined-outside-init
        self._pre = namespace.get('pre', False)  # pylint: disable=attribute-defined-outside-init
        self._pypy = namespace.get('pypy', False)  # pylint: disable=attribute-defined-outside-init
        self._system = namespace.get('system', False)  # pylint: disable=attribute-defined-outside-init

        self._all = namespace.get('all', False)  # pylint: disable=attribute-defined-outside-init
        self._quiet = namespace.get('quiet', False)  # pylint: disable=attribute-defined-outside-init
        self._verbose = namespace.get('verbose', False)  # pylint: disable=attribute-defined-outside-init
        self._yes = namespace.get('yes', False)  # pylint: disable=attribute-defined-outside-init

        self._logging_opts = namespace.get('logging', str()).split()  # pylint: disable=attribute-defined-outside-init
        self._uninstall_opts = namespace.get('uninstall', str()).split()  # pylint: disable=attribute-defined-outside-init

    def _check_list(self, path):
        argv = [path, '-m', 'pip', 'freeze']
        argv.extend(self._logging_opts)

        text = f'Checking outdated {self.desc[1]}'
        print_info(text, self._file, redirect=self._vflag)

        try:
            proc = subprocess.check_output(argv, stderr=make_stderr(self._vflag))
        except subprocess.SubprocessError:
            print_text(traceback.format_exc(), self._file, redirect=self._vflag)
            self._var__temp_pkgs = set()  # pylint: disable=attribute-defined-outside-init
        else:
            context = proc.decode()
            print_text(context, self._file, redirect=self._qflag)

            _temp_pkgs = list()
            for line in filter(None, context.strip().splitlines()):
                _temp_pkgs.append(line.split('==')[0])
            self._var__temp_pkgs = set(_temp_pkgs)  # pylint: disable=attribute-defined-outside-init
        finally:
            with open(self._file, 'a') as file:
                file.write(f'Script done on {date()}\n')

    def _proc_uninstall(self, path):
        text = f'Uninstalling specified {self.desc[1]}'
        print_info(text, self._file, redirect=self._qflag)

        def _proc_dependency(package, _know_pkgs):
            _deps_pkgs = {package}
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
                proc = subprocess.check_output(argv, stderr=make_stderr(self._vflag))
            except subprocess.CalledProcessError:
                print_text(traceback.format_exc(), self._file, redirect=self._vflag)
            else:
                context = proc.decode()
                print_text(context, self._file, redirect=self._vflag)

                for line in filter(lambda s: s.startswith('Requires: '), context.strip().splitlines()):
                    _temp_pkgs = set(map(lambda s: s.rstrip(','), line.split()[1:])) - _know_pkgs
                    _deps_pkgs |= _temp_pkgs
                    break
            finally:
                with open(self._file, 'a') as file:
                    file.write(f'Script done on {date()}\n')

            for pkg in _temp_pkgs:
                _temp_pkgs = _proc_dependency(pkg, _know_pkgs)
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
            for package in (_deps_pkgs - _done_pkgs):  # pylint: disable=superfluous-parens
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
