# -*- coding: utf-8 -*-

import traceback

from macdaily.cmd.reinstall import ReinstallCommand
from macdaily.core.brew import BrewCommand
from macdaily.util.compat import subprocess
from macdaily.util.const.string import MAX, MIN
from macdaily.util.const.term import reset, under
from macdaily.util.tools.make import make_stderr
from macdaily.util.tools.misc import date
from macdaily.util.tools.print import print_info, print_scpt, print_text
from macdaily.util.tools.script import run


class BrewReinstall(BrewCommand, ReinstallCommand):

    def _parse_args(self, namespace):
        self._endswith = namespace.get('endswith', MAX)
        self._no_cleanup = namespace.get('no_cleanup', False)
        self._startswith = namespace.get('startswith', MIN)

        self._all = namespace.get('all', False)
        self._quiet = namespace.get('quiet', False)
        self._verbose = namespace.get('verbose', False)
        self._yes = namespace.get('yes', False)

        self._logging_opts = namespace.get('logging', str()).split()
        self._reinstall_opts = namespace.get('reinstall', str()).split()

    def _check_list(self, path):
        text = 'Checking installed {}'.format(self.desc[1])
        print_info(text, self._file, redirect=self._vflag)

        argv = [path, 'list']
        argv.extend(self._logging_opts)

        args = ' '.join(argv)
        print_scpt(args, self._file, redirect=self._vflag)
        with open(self._file, 'a') as file:
            file.write('Script started on {}\n'.format(date()))
            file.write('command: {!r}\n'.format(args))

        try:
            proc = subprocess.check_output(argv, stderr=make_stderr(self._vflag))
        except subprocess.SubprocessError:
            print_text(traceback.format_exc(), self._file, redirect=self._vflag)
            self._var__temp_pkgs = set()
        else:
            context = proc.decode()
            print_text(context, self._file, redirect=self._vflag)

            _temp_pkgs = list()
            for package in context.strip().split():
                if self._startswith <= package <= self._endswith:
                    _temp_pkgs.append(package)
            self._var__temp_pkgs = set(_temp_pkgs)
        finally:
            with open(self._file, 'a') as file:
                file.write('Script done on {}\n'.format(date()))

    def _proc_reinstall(self, path):
        text = 'Reinstalling specified {}'.format(self.desc[1])
        print_info(text, self._file, redirect=self._qflag)

        argv = [path, 'reinstall']
        if self._quiet:
            argv.append('--quiet')
        if self._verbose:
            argv.append('--verbose')
        argv.extend(self._reinstall_opts)

        argv.append('')
        for package in self._var__temp_pkgs:
            argv[-1] = package
            print_scpt(' '.join(argv), self._file, redirect=self._qflag)
            if run(argv, self._file, timeout=self._timeout,
                   redirect=self._qflag, verbose=self._vflag):
                self._fail.append(package)
            else:
                self._pkgs.append(package)
        del self._var__temp_pkgs
