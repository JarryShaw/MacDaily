# -*- coding: utf-8 -*-

import abc
import os
import shutil
import sys
import traceback

from macdaily.cls.command import Command
from macdaily.util.const import (bold, flash, purple_bg, red, red_bg, reset,
                                 under)
from macdaily.util.misc import (date, print_info, print_scpt, print_term,
                                print_text, run, sudo, make_stderr)

try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess


class NpmCommand(Command):

    @property
    def mode(self):
        return 'npm'

    @property
    def name(self):
        return 'Node.js Package Manager'

    @property
    def desc(self):
        return ('node module', 'node modules')

    def _check_exec(self):
        self._var__exec_path = shutil.which('npm')
        flag = (self._var__exec_path is not None)
        if not flag:
            print('macdaily-{}: {}{}npm{}: command not found'.format(self.cmd, red_bg, flash, reset), file=sys.stderr)
            text = ('macdaily-{}: {}npm{}: you may download Node.js from '
                    '{}{}https://nodejs.org{}'.format(self.cmd, red, reset, purple_bg, under, reset))
            print_term(text, self._file, redirect=self._qflag)
        return flag

    @abc.abstractmethod
    def _parse_args(self, namespace):
        super()._parse_args(namespace)
        self._no_cleanup = namespace.get('no_cleanup', False)
        self._quiet = namespace.get('quiet', False)
        self._verbose = namespace.get('verbose', False)

    def _loc_exec(self):
        self._exec = {self._var__exec_path}
        del self._var__exec_path

    def _check_pkgs(self, path):
        text = 'Listing installed {}'.format(self.desc[1])
        print_info(text, self._file, redirect=self._vflag)

        argv = [path, 'list', '--global', '--parseable']
        args = ' '.join(argv)
        print_scpt(args, self._file, redirect=self._vflag)
        with open(self._file, 'a') as file:
            file.write('Script started on {}\n'.format(date()))
            file.write('command: {!r}\n'.format(args))

        stderr = make_stderr(self._vflag, sys.stderr)
        try:
            proc = subprocess.check_output(argv, stderr=stderr)
        except subprocess.CalledProcessError:
            print_text(traceback.format_exc(), self._file, redirect=self._vflag)
            _real_pkgs = set()
        else:
            context = proc.decode()
            print_text(context, self._file, redirect=self._vflag)

            _list_pkgs = list()
            for line in context.strip().splitlines():
                _, name = os.path.split(line)
                _list_pkgs.append(name)
            _real_pkgs = set(_list_pkgs)
        finally:
            with open(self._file, 'a') as file:
                file.write('Script done on {}\n'.format(date()))

        text = 'Checking existence of specified packages'
        print_info(text, self._file, redirect=self._vflag)

        _temp_pkgs = list()
        _lost_pkgs = list()
        for package in self._packages:
            if package in _real_pkgs:
                _temp_pkgs.append(package)
            else:
                _lost_pkgs.append(package)
        self._lost.extend(_lost_pkgs)

        self._var__real_pkgs = set(_real_pkgs)
        self._var__lost_pkgs = set(_lost_pkgs)
        self._var__temp_pkgs = set(_temp_pkgs)

    def _proc_cleanup(self):
        if self._no_cleanup:
            return

        text = 'Pruning caches and archives'
        print_info(text, self._file, redirect=self._qflag)

        argv = ['npm', 'cleanup']
        if self._verbose:
            argv.append('--verbose')
        if self._quiet:
            argv.append('--quiet')
        print_scpt(' '.join(argv), self._file, redirect=self._qflag)

        def _cleanup(argv):
            if self._verbose:
                argv.append('--verbose')
            if self._quiet:
                argv.append('--quiet')
            args = ' '.join(argv)
            print_scpt(args, self._file, redirect=self._qflag)
            sudo(argv, self._file, self._password,
                 redirect=self._qflag, verbose=self._vflag)

        for path in self._exec:
            _cleanup([path, 'dedupe', '--global'])
            _cleanup([path, 'cache', 'clean', '--force'])
