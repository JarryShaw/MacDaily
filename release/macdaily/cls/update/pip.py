# -*- coding: utf-8 -*-

import contextlib
import copy
import json
import re
import sys
import traceback

from macdaily.cmd.update import UpdateCommand
from macdaily.core.pip import PipCommand
from macdaily.util.const import bold, green, red, reset, yellow
from macdaily.util.misc import (date, print_info, print_scpt, print_term,
                                print_text, sudo)

try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess


class PipUpdate(PipCommand, UpdateCommand):

    def _parse_args(self, namespace):
        self._brew = namespace.pop('brew', False)
        self._cpython = namespace.pop('cpython', False)
        self._no_cleanup = namespace.pop('no_cleanup', False)
        self._pre = namespace.pop('pre', False)
        self._pypy = namespace.pop('pypy', False)
        self._system = namespace.pop('system', False)

        self._all = namespace.pop('all', False)
        self._quiet = namespace.pop('quiet', False)
        self._verbose = namespace.pop('verbose', False)
        self._yes = namespace.pop('yes', False)

        self._logging_opts = namespace.pop('logging', str()).split()
        self._update_opts = namespace.pop('update', str()).split()

    def _check_pkgs(self, path):
        _temp_pkgs = list()
        _lost_pkgs = list()

        text = 'Checking existence of specified packages'
        print_info(text, self._file, redirect=self._vflag)
        for package in self._packages:
            argv = [path, '-m', 'pip', 'show', package]

            args = ' '.join(argv)
            print_scpt(args, self._file, redirect=self._vflag)
            with open(self._file, 'a') as file:
                file.write('Script started on {}\n'.format(date()))
                file.write('command: {!r}\n'.format(args))

            try:
                proc = subprocess.check_call(argv, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError:
                print_text(traceback.format_exc(), self._file, redirect=self._vflag)
                _lost_pkgs.append(package)
            else:
                print_text(proc.stdout, self._file, redirect=self._vflag)
                _temp_pkgs.append(package)
            finally:
                with open(self._file, 'a') as file:
                    file.write('Script done on {}\n'.format(date()))

        if _lost_pkgs:
            text = 'Listing installed {}'.format(self.desc[1])
            print_info(text, self._file, redirect=self._vflag)

            self._lost.extend(_lost_pkgs)
            argv = [path, '-m', 'pip', 'list']

            args = ' '.join(argv)
            print_scpt(args, self._file, redirect=self._vflag)
            with open(self._file, 'a') as file:
                file.write('Script started on {}\n'.format(date()))
                file.write('command: {!r}\n'.format(args))

            try:
                proc = subprocess.check_output(argv, stderr=subprocess.DEVNULL)
            except subprocess.CalledProcessError:
                print_text(traceback.format_exc(), self._file, redirect=self._vflag)
                self._var__real_pkgs = set()
            else:
                context = proc.decode()
                print_text(context, self._file, redirect=self._vflag)
                self._var__real_pkgs = set(map(lambda pkg: pkg.split('==')[0], context.split()))
            finally:
                with open(self._file, 'a') as file:
                    file.write('Script done on {}\n'.format(date()))
        else:
            self._var__real_pkgs = set()

        self._var__lost_pkgs = set(_lost_pkgs)
        self._var__temp_pkgs = set(package)

    def _check_list(self, path):
        argv = [path, '-m', 'pip', 'list', '--outdated']
        if self._pre:
            argv.append('--pre')
        argv.extend(self._logging_opts)

        text = 'Checking outdated {}'.format(self.desc[1])
        print_info(text, self._file, redirect=self._vflag)

        temp = copy.copy(argv)
        temp.append('--format=columns')
        args = ' '.join(temp)
        print_scpt(args, self._file, redirect=self._vflag)
        with open(self._file, 'a') as file:
            file.write('Script started on {}\n'.format(date()))
            file.write('command: {!r}\n'.format(args))

        argv.append('--format=json')
        try:
            proc = subprocess.check_output(argv, stderr=subprocess.DEVNULL)
        except subprocess.SubprocessError:
            print_text(traceback.format_exc(), self._file, redirect=self._vflag)
            self._var__temp_pkgs = set()
        else:
            # self._var__temp_pkgs = set(map(lambda pkg: pkg.split('==')[0], proc.decode().split()))
            text = proc.decode()
            start = text.rfind('[')
            stop = text.rfind(']') + 1
            context = json.loads(text[start:stop])
            self._var__temp_pkgs = set(map(lambda item: item['name'], context))

            prefix = text[:start]
            if prefix:
                print_text(prefix, self._file, redirect=self._vflag)
            if context:
                name_len = max(7, max(map(lambda item: len(item['name']), context), default=7))
                version_len = max(7, max(map(lambda item: len(item['version']), context), default=7))
                latest_version_len = max(6, max(map(lambda item: len(item['latest_version']), context), default=6))
                latest_filetype_len = max(4, max(map(lambda item: len(item['latest_filetype']), context), default=4))

                def _pprint(package, version, latest, type):
                    text = [package.ljust(name_len), version.ljust(version_len),
                            latest.ljust(latest_version_len), type.ljust(latest_filetype_len)]
                    return ' '.join(text)

                print_text(_pprint('Package', 'Version', 'Latest', 'Type'), self._file, redirect=self._vflag)
                print_text(' '.join(map(lambda length: '-' * length,
                                        [name_len, version_len, latest_version_len, latest_filetype_len])),
                           self._file, redirect=self._vflag)
                for item in context:
                    print_text(_pprint(item['name'], item['version'],
                                       item['latest_version'], item['latest_filetype']),
                               self._file, redirect=self._vflag)
        finally:
            with open(self._file, 'a') as file:
                file.write('Script done on {}\n'.format(date()))

    def _proc_update(self, path):
        argv = [path, '-m', 'pip', 'install', '--upgrade']
        if self._pre:
            argv.append('--pre')
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
            if sudo(args, self._file, sethome=True, askpass=self._askpass,
                    timeout=self._timeout, redirect=self._qflag):
                self._fail.append(package)
            else:
                self._pkgs.append(package)
        del self._var__temp_pkgs

        def _proc_check():
            argv = [path, '-m', 'pip', 'check']

            args = ' '.join(argv)
            print_scpt(args, self._file, redirect=self._vflag)
            with open(self._file, 'a') as file:
                file.write('Script started on {}\n'.format(date()))
                file.write('command: {!r}\n'.format(args))

            _deps_pkgs = list()
            try:
                proc = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            except subprocess.SubprocessError:
                print_text(traceback.format_exc(), self._file, redirect=self._vflag)
            else:
                context = proc.stdout.decode()
                print_text(context, self._file, redirect=self._vflag)

                for line in filter(None, context.strip().split('\n')):
                    if line == 'No broken requirements found.':
                        return set()
                    if 'which is not installed' in line:
                        _deps_pkgs.append(line.split()[3][:-1])
                    else:
                        _deps_pkgs.append(line.split()[4][:-1])
            finally:
                with open(self._file, 'a') as file:
                    file.write('Script done on {}\n'.format(date()))
            return set(_deps_pkgs)

        def _proc_confirm():
            pkgs = '{}, {}'.format(reset, bold).join(_deps_pkgs)
            text = 'macdaily-update: {}pip{}: found broken dependencies: {}{}{}'.format(yellow, reset, bold, pkgs, reset)
            print_term(text, self._file, redirect=self._qflag)
            if self._yes or self._quiet:
                return True
            while True:
                ans = input('Would you like to reinstall? (y/N)')
                if re.match(r'[yY]', ans):
                    return True
                elif re.match(r'[nN]', ans):
                    return False
                else:
                    print('Invalid input.', file=sys.stderr)

        text = 'Checking broken {} dependencies'.format(self.desc[0])
        print_info(text, self._file, redirect=self._qflag)

        _deps_pkgs = _proc_check()
        if not _deps_pkgs:
            text = 'macdaily-update: {}pip{}: no broken dependencies'.format(green, reset)
            print_term(text, self._file, redirect=self._qflag)
            return

        text = 'Fixing broken {} dependencies'.format(self.desc[0])
        print_info(text, self._file, redirect=self._qflag)

        if _proc_confirm():
            argv = [path, '-m', 'pip', 'reinstall']
            if self._quiet:
                argv.append('--quiet')
            if self._verbose:
                argv.append('--verbose')

            args = ' '.join(argv)
            print_scpt(args, self._file, redirect=self._qflag)

            _done_pkgs = set()
            while _deps_pkgs:
                for package in _deps_pkgs:
                    real_name = re.split(r'[<>=!]', package, maxsplit=1)[0]
                    print_scpt('{} {}'.format(args, package), self._file, redirect=self._qflag)

                    temp = copy.copy(argv)
                    temp[3] = 'uninstall'
                    print_scpt('{} {}'.format(" ".join(temp), real_name), self._file, redirect=self._qflag)
                    sudo('{} -m pip uninstall {} --yes'.format(path, real_name), self._file, sethome=True,
                         askpass=self._askpass, redirect=self._qflag, timeout=self._timeout)

                    temp = copy.copy(argv)
                    temp[3] = 'install'
                    print_scpt('{} {}'.format(" ".join(temp), package), self._file, redirect=self._qflag)
                    if not sudo('{} -m pip install {}'.format(path, package), self._file, sethome=True,
                                askpass=self._askpass, redirect=self._qflag, timeout=self._timeout):
                        with contextlib.suppress(ValueError):
                            self._pkgs.remove(real_name)
                _done_pkgs |= _deps_pkgs
                _deps_pkgs = _proc_check() - _done_pkgs
            text = 'macdaily-update: {}pip{}: all broken dependencies fixed'.format(green, reset)
        else:
            text = 'macdaily-update: {}pip{}: all broken dependencies remain'.format(red, reset)
        print_term(text, self._file, redirect=self._qflag)
