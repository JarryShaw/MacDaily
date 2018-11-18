# -*- coding: utf-8 -*-

import re
import sys
import traceback

from macdaily.cmd.update import UpdateCommand
from macdaily.core.apm import ApmCommand
from macdaily.util.misc import (date, make_stderr, print_info, print_scpt,
                                print_text, run)

try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess


class ApmUpdate(ApmCommand, UpdateCommand):

    def _parse_args(self, namespace):
        self._beta = namespace.get('beta', False)

        self._all = namespace.get('all', False)
        self._quiet = namespace.get('quiet', False)
        self._verbose = namespace.get('verbose', False)
        self._yes = namespace.get('yes', False)

        self._logging_opts = namespace.get('logging', str()).split()
        self._update_opts = namespace.get('update', str()).split()

    def _check_list(self, path):
        text = 'Checking outdated {}'.format(self.desc[1])
        print_info(text, self._file, redirect=self._vflag)

        argv = [path, 'upgrade']
        argv.extend(self._logging_opts)
        argv.append('--no-color')
        argv.append('--no-json')
        argv.append('--list')
        args = ' '.join(argv)
        print_scpt(args, self._file, redirect=self._vflag)
        with open(self._file, 'a') as file:
            file.write('Script started on {}\n'.format(date()))
            file.write('command: {!r}\n'.format(args))

        stderr = make_stderr(self._vflag, sys.stderr)
        try:
            proc = subprocess.check_output(argv, stderr=stderr)
        except subprocess.SubprocessError:
            print_text(traceback.format_exc(), self._file, redirect=self._vflag)
            self._var__temp_pkgs = set()
        else:
            context = proc.decode()
            print_text(context, self._file, redirect=self._vflag)

            _temp_pkgs = list()
            for line in filter(lambda s: '->' in s, context.strip().split('\n')):
                _temp_pkgs.append(re.sub(r'.* (.*) .* -> .*', r'\1', line))
            self._var__temp_pkgs = set(_temp_pkgs)
        finally:
            with open(self._file, 'a') as file:
                file.write('Script done on {}\n'.format(date()))

    def _proc_update(self, path):
        argv = [path, 'upgrade']
        argv.extend(self._update_opts)
        if self._yes:
            argv.append('--no-confirm')
        if self._verbose:
            argv.append('--verbose')
        if self._quiet:
            argv.append('--quiet')
        argv.append('--no-list')
        argv.append('--no-json')

        argv.append('')
        for package in self._var__temp_pkgs:
            argv[-1] = package
            print_scpt(argv, self._file, redirect=self._qflag)
            if run(argv, self._file, timeout=self._timeout,
                   redirect=self._qflag, verbose=self._vflag):
                self._fail.append(package)
            else:
                self._pkgs.append(package)
        del self._var__temp_pkgs
