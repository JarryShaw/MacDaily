# -*- coding: utf-8 -*-

import copy
import os
import sys
import textwrap
import time
import traceback

from macdaily.cmd.update import UpdateCommand
from macdaily.core.cask import CaskCommand
from macdaily.util.const import length
from macdaily.util.misc import (date, make_stderr, print_info, print_scpt,
                                print_text, run)

try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess


class CaskUpdate(CaskCommand, UpdateCommand):

    def _parse_args(self, namespace):
        self._exhaust = namespace.get('exhaust', False)
        self._force = namespace.get('force', False)
        self._greedy = namespace.get('greedy', False)
        self._merge = namespace.get('merge', False)
        self._no_cleanup = namespace.get('no_cleanup', False)

        self._all = namespace.get('all', False)
        self._quiet = namespace.get('quiet', False)
        self._verbose = namespace.get('verbose', False)
        self._yes = namespace.get('yes', False)

        self._logging_opts = namespace.get('logging', str()).split()
        self._update_opts = namespace.get('update', str()).split()

    def _check_list(self, path):
        if (self._brew_renew is None or time.time() - self._brew_renew >= 300):
            self._proc_renew(path)
            self._brew_renew = time.time()

        if self._exhaust:
            return self._exhaust_check(path)

        text = 'Checking outdated {}'.format(self.desc[1])
        print_info(text, self._file, redirect=self._vflag)

        argv = [path, 'cask', 'outdated']
        if self._quiet:
            argv.append('--quiet')
        if self._verbose:
            argv.append('--verbose')
        if self._greedy:
            argv.append('--greedy')
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
            for line in filter(None, context.strip().split('\n')):
                _temp_pkgs.append(line.split(maxsplit=1)[0])
            self._var__temp_pkgs = set(_temp_pkgs)
        finally:
            with open(self._file, 'a') as file:
                file.write('Script done on {}\n'.format(date()))

    def _exhaust_check(self, path):
        text = 'Checking outdated {} exclusively'.format(self.desc[1])
        print_info(text, self._file, redirect=self._vflag)

        argv = ['brew', 'cask', 'outdated', '--exhaust']
        if self._quiet:
            argv.append('--quiet')
        if self._verbose:
            argv.append('--verbose')
        argv.extend(self._logging_opts)
        print_scpt(' '.join(argv), self._file, redirect=self._vflag)

        text = 'Listing installed {}'.format(self.desc[1])
        print_info(text, self._file, redirect=self._vflag)

        argv = [path, 'cask', 'list']
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
            _list_pkgs = set()
        else:
            context = proc.decode()
            _list_pkgs = set(context.split())
            print_text(context, self._file, redirect=self._vflag)
        finally:
            with open(self._file, 'a') as file:
                file.write('Script done on {}\n'.format(date()))

        text = 'Fetching Homebrew prefix'.format()
        print_info(text, self._file, redirect=self._vflag)

        argv = [path, '--prefix']
        args = ' '.join(argv)
        print_scpt(args, self._file, redirect=self._vflag)
        with open(self._file, 'a') as file:
            file.write('Script started on {}\n'.format(date()))
            file.write('command: {!r}\n'.format(args))

        fail = False
        stderr = make_stderr(self._vflag, sys.stderr)
        try:
            proc = subprocess.check_output(argv, stderr=stderr)
        except subprocess.CalledProcessError:
            print_text(traceback.format_exc(), self._file, redirect=self._vflag)
            self._var__temp_pkgs = set()
            fail = True
        else:
            context = proc.decode()
            print_text(context, self._file, redirect=self._vflag)
            prefix = context.strip()
        finally:
            with open(self._file, 'a') as file:
                file.write('Script done on {}\n'.format(date()))
        if fail:
            return

        text = 'Checking versions of installed {}'.format(self.desc[1])
        print_info(text, self._file, redirect=self._vflag)

        _temp_pkgs = list()
        for cask in _list_pkgs:
            argv = [path, 'cask', 'info', cask]
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
            else:
                context = proc.decode()
                print_text(context, self._file, redirect=self._vflag)

                version = context.split(maxsplit=2)[1]
                installed = os.path.join(prefix, 'Caskroom', cask, version)
                if os.path.isdir(installed):
                    _temp_pkgs.append(cask)
            finally:
                with open(self._file, 'a') as file:
                    file.write('Script done on {}\n'.format(date()))

        self._var__temp_pkgs = set(_temp_pkgs)
        max_len = len(max(_temp_pkgs, key=lambda s: len(s)))
        context = os.linesep.join(textwrap.wrap('    '.join(
            map(lambda s: s.ljust(max_len), self._var__temp_pkgs)), length))
        print_scpt('{} cask outdated list'.format(path), self._file, redirect=self._vflag)
        print_text(context, self._file, redirect=self._vflag)

    def _proc_update(self, path):
        text = 'Upgrading outdated {}'.format(self.desc[1])
        print_info(text, self._file, redirect=self._qflag)

        argv = [path, 'cask', 'upgrade']
        if self._quiet:
            argv.append('--quiet')
        if self._verbose:
            argv.append('--verbose')
        if self._greedy:
            argv.append('--greedy')
        argv.extend(self._update_opts)
        argv.append('')

        temp = copy.copy(argv)
        if self._exhaust:
            temp.append('--exhaust')
        args = ' '.join(temp)

        askpass = 'SUDO_ASKPASS={!r}'.format(self._askpass)
        for package in self._var__temp_pkgs:
            argv[-1] = package
            print_scpt('{} {}'.format(args, package), self._file, redirect=self._qflag)
            if run(argv, self._file, shell=True, timeout=self._timeout,
                   redirect=self._qflag, verbose=self._vflag, prefix=askpass):
                self._fail.append(package)
            else:
                self._pkgs.append(package)
        del self._var__temp_pkgs
