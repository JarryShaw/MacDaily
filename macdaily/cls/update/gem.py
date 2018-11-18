# -*- coding: utf-8 -*-

import re
import sys
import traceback

from macdaily.cmd.update import UpdateCommand
from macdaily.core.gem import GemCommand
from macdaily.util.misc import (date, make_stderr, print_info, print_scpt,
                                print_text, sudo)

try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess


class GemUpdate(GemCommand, UpdateCommand):

    def _parse_args(self, namespace):
        self._brew = namespace.get('brew', False)
        self._system = namespace.get('system', False)

        self._all = namespace.get('all', False)
        self._quiet = namespace.get('quiet', False)
        self._verbose = namespace.get('verbose', False)
        self._yes = namespace.get('yes', False)

        self._logging_opts = namespace.get('logging', str()).split()
        self._update_opts = namespace.get('update', str()).split()

    def _check_list(self, path):
        text = 'Updating RubyGems database'
        print_info(text, self._file, redirect=self._qflag)

        argv = [path, 'update', '--system']
        if self._quiet:
            argv.append('--quiet')
        if self._verbose:
            argv.append('--verbose')
        args = ' '.join(argv)
        print_scpt(args, self._file, redirect=self._qflag)
        sudo(argv, self._file, self._password,
             redirect=self._qflag, verbose=self._vflag)

        text = 'Checking outdated {}'.format(self.desc[1])
        print_info(text, self._file, redirect=self._vflag)

        argv = [path, 'outdated']
        if self._quiet:
            argv.append('--quiet')
        if self._verbose:
            argv.append('--verbose')
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
            self._var__temp_pkgs = set()
        else:
            context = proc.decode()
            print_text(context, self._file, redirect=self._vflag)

            _temp_pkgs = list()
            for item in filter(lambda s: re.match(r'\w* \(.*\)', s), context.strip().split('\n')):
                _temp_pkgs.append(item.split()[0])
            self._var__temp_pkgs = set(_temp_pkgs)
            # self._var__temp_pkgs = set(map(lambda s: s.split()[0], filter(None, context.strip().split('\n'))))
        finally:
            with open(self._file, 'a') as file:
                file.write('Script done on {}\n'.format(date()))

    def _proc_update(self, path):
        argv = [path, 'update']
        if self._quiet:
            argv.append('--quiet')
        if self._verbose:
            argv.append('--verbose')
        argv.extend(self._update_opts)

        text = 'Upgrading outdated {}'.format(self.desc[1])
        print_info(text, self._file, redirect=self._qflag)

        argc = ' '.join(argv)
        for package in self._var__temp_pkgs:
            args = '{} {}'.format(argc, package)
            print_scpt(args, self._file, redirect=self._qflag)
            yes = 'y' if self._yes else None
            if sudo(argv, self._file, self._password, timeout=self._timeout,
                    redirect=self._qflag, verbose=self._vflag, yes=yes):
                self._fail.append(package)
            else:
                self._pkgs.append(package)
        del self._var__temp_pkgs
