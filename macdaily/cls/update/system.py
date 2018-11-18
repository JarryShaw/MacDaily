# -*- coding: utf-8 -*-

import os
import re
import sys
import traceback

from macdaily.cmd.update import UpdateCommand
from macdaily.core.system import SystemCommand
from macdaily.util.misc import (date, make_stderr, print_info, print_scpt,
                                print_text, sudo)

try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess


class SystemUpdate(SystemCommand, UpdateCommand):

    def _parse_args(self, namespace):
        self._recommend = namespace.get('recommended', False)
        self._restart = namespace.get('restart', False)

        self._all = namespace.get('all', False)
        self._quiet = namespace.get('quiet', False)
        self._verbose = namespace.get('verbose', False)
        self._yes = namespace.get('yes', False)

        self._logging_opts = namespace.get('logging', str()).split()
        self._update_opts = namespace.get('update', str()).split()

    def _check_list(self, path):
        text = 'Checking outdated {}'.format(self.desc[1])
        print_info(text, self._file, redirect=self._vflag)

        argv = [path, '--list']
        argv.extend(self._logging_opts)
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
            self._var__rcmd_pkgs = set()
            self._var__norm_pkgs = set()
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

            self._var__rcmd_pkgs = set(_rcmd_pkgs)
            self._var__norm_pkgs = set(_norm_pkgs)
        finally:
            with open(self._file, 'a') as file:
                file.write('Script done on {}\n'.format(date()))
        self._var__temp_pkgs = self._var__rcmd_pkgs | self._var__norm_pkgs

    def _proc_update(self, path):
        if self._recommend:
            _temp_pkgs = self._var__rcmd_pkgs
        else:
            _temp_pkgs = self._var__rcmd_pkgs | self._var__norm_pkgs

        argv = [path, '--install', '--no-scan']
        if self._restart:
            argv.append('--restart')
        if self._quiet:
            argv.append('--quiet')
        argv.extend(self._update_opts)

        text = 'Upgrading outdated {}'.format(self.desc[1])
        print_info(text, self._file, redirect=self._qflag)

        argc = ' '.join(argv)
        for package in _temp_pkgs:
            args = '{} {!r}'.format(argc, package)
            print_scpt(args, self._file, redirect=self._qflag)
            if sudo(args, self._file, self._password, timeout=self._timeout,
                    redirect=self._qflag, verbose=self._vflag):
                self._fail.append(package)
            else:
                self._pkgs.append(package)
        del self._var__rcmd_pkgs
        del self._var__norm_pkgs
        del self._var__temp_pkgs
