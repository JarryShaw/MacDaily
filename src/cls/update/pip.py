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
from macdaily.util.misc import date, print_info, print_scpt, print_text, sudo

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
        print_info(text, self._file, redirect=(not self._verbose))
        for package in self._packages:
            argv = [path, '-m', 'pip', 'show', package]

            args = ' '.join(argv)
            print_scpt(args, self._file, redirect=(not self._verbose))
            with open(self._file, 'a') as file:
                file.write(f'Script started on {date()}\n')
                file.write(f'command: {args!r}\n')

            try:
                proc = subprocess.check_call(argv, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError:
                print_text(traceback.format_exc(), self._file, redirect=(not self._verbose))
                _lost_pkgs.append(package)
            else:
                print_text(proc.stdout, self._file, redirect=(not self._verbose))
                _temp_pkgs.append(package)
            finally:
                with open(self._file, 'a') as file:
                    file.write(f'Script done on {date()}\n')

        text = f'Listing installed {self.desc[1]}'
        print_info(text, self._file, redirect=(not self._verbose))
        if _lost_pkgs:
            self._lost.extend(_lost_pkgs)
            argv = [path, '-m', 'pip', 'list']

            args = ' '.join(argv)
            print_scpt(args, self._file, redirect=(not self._verbose))
            with open(self._file, 'a') as file:
                file.write(f'Script started on {date()}\n')
                file.write(f'command: {args!r}\n')

            try:
                proc = subprocess.check_output(argv, stderr=subprocess.DEVNULL)
            except subprocess.CalledProcessError:
                print_text(traceback.format_exc(), self._file, redirect=(not self._verbose))
                self.__real_pkgs = set()
            else:
                context = proc.decode()
                print_text(context, self._file, redirect=(not self._verbose))
                self.__real_pkgs = set(map(lambda pkg: pkg.split('==')[0], context.split()))
            finally:
                with open(self._file, 'a') as file:
                    file.write(f'Script done on {date()}\n')
        else:
            self.__real_pkgs = set()

        self.__lost_pkgs = set(_lost_pkgs)
        self.__temp_pkgs = set(package)

    def _check_list(self, path):
        argv = [path, '-m', 'pip', 'list', '--outdated']
        if self._pre:
            argv.append('--pre')
        argv.extend(self._logging_opts)

        temp = copy.copy(argv)
        temp.append('--format=columns')
        args = ' '.join(temp)
        text = f'Checking outdated {self.desc[1]}'
        print_info(text, self._file, redirect=(not self._verbose))
        print_scpt(args, self._file, redirect=(not self._verbose))
        with open(self._file, 'a') as file:
            file.write(f'Script started on {date()}\n')
            file.write(f'command: {args!r}\n')

        argv.append('--format=json')
        try:
            proc = subprocess.check_output(argv, stderr=subprocess.DEVNULL)
        except subprocess.SubprocessError:
            print_text(traceback.format_exc(), self._file, redirect=(not self._verbose))
            self.__temp_pkgs = set()
        else:
            # self.__temp_pkgs = set(map(lambda pkg: pkg.split('==')[0], proc.decode().split()))
            context = json.loads(proc.decode().strip())
            self.__temp_pkgs = set(map(lambda item: item['name'], context))

            if context:
                name_len = max(7, max(map(lambda item: len(item['name']), context), default=7))
                version_len = max(7, max(map(lambda item: len(item['version']), context), default=7))
                latest_version_len = max(6, max(map(lambda item: len(item['latest_version']), context), default=6))
                latest_filetype_len = max(4, max(map(lambda item: len(item['latest_filetype']), context), default=4))

                def _pprint(package, version, latest, type):
                    text = [package.ljust(name_len), version.ljust(version_len),
                            latest.ljust(latest_version_len), type.ljust(latest_filetype_len)]
                    return ' '.join(text)

                print_text(_pprint('Package', 'Version', 'Latest', 'Type'), self._file, redirect=(not self._verbose))
                print_text(' '.join(map(lambda length: '-' * length,
                                        [name_len, version_len, latest_version_len, latest_filetype_len])),
                           self._file, redirect=(not self._verbose))
                for item in context:
                    print_text(_pprint(item['name'], item['version'],
                                       item['latest_version'], item['latest_filetype']),
                               self._file, redirect=(not self._verbose))
        finally:
            with open(self._file, 'a') as file:
                file.write(f'Script done on {date()}\n')

    def _proc_update(self, path):
        argv = [path, '-m', 'pip', 'install', '--upgrade']
        if self._pre:
            argv.append('--pre')
        if self._quiet:
            argv.append('--quiet')
        if self._verbose:
            argv.append('--verbose')
        argv.extend(self._update_opts)

        text = f'Upgrading outdated {self.desc[1]}'
        print_info(text, self._file, redirect=self._quiet)

        argc = ' '.join(argv)
        for package in self.__temp_pkgs:
            args = f'{argc} {package}'
            print_scpt(args, self._file, redirect=self._quiet)
            if sudo(args, self._file, askpass=self._askpass,
                    timeout=self._timeout, redirect=self._quiet):
                self._fail.append(package)
            else:
                self._pkgs.append(package)
        del self.__temp_pkgs

        def _proc_check():
            argv = [path, '-m', 'pip', 'check']

            args = ' '.join(argv)
            print_scpt(args, self._file, redirect=(not self._verbose))
            with open(self._file, 'a') as file:
                file.write(f'Script started on {date()}\n')
                file.write(f'command: {args!r}\n')

            _deps_pkgs = list()
            try:
                proc = subprocess.check_output(argv, stderr=subprocess.DEVNULL)
            except subprocess.SubprocessError:
                print_text(traceback.format_exc(), self._file, redirect=(not self._verbose))
            else:
                context = proc.decode()
                print_text(context, self._file, redirect=(not self._verbose))

                for line in filter(None, context.strip().split('\n')):
                    if line == 'No broken requirements found.':
                        return set()
                    if 'which is not installed' in line:
                        _deps_pkgs.append(line.split()[3][:-1])
                    else:
                        _deps_pkgs.append(line.split()[4][:-1])
            finally:
                with open(self._file, 'a') as file:
                    file.write(f'Script done on {date()}\n')
            return set(_deps_pkgs)

        def _proc_confirm():
            pkgs = f'{reset}, {bold}'.join(_deps_pkgs)
            text = f'macdaily-update: {yellow}pip{reset}: found broken dependencies: {bold}{pkgs}{reset}'
            print_text(text, self._file, redirect=self._quiet)
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

        text = f'Checking broken {self.desc[0]} dependencies'
        print_info(text, self._file, redirect=self._quiet)

        _deps_pkgs = _proc_check()
        if not _deps_pkgs:
            text = f'macdaily-update: {green}pip{reset}: no broken dependencies'
            print_text(text, self._file, redirect=self._quiet)
            return

        text = f'Fixing broken {self.desc[0]} dependencies'
        print_info(text, self._file, redirect=self._quiet)

        if _proc_confirm():
            argv = [path, '-m', 'pip', 'reinstall']
            if self._quiet:
                argv.append('--quiet')
            if self._verbose:
                argv.append('--verbose')

            args = ' '.join(argv)
            print_scpt(args, self._file, redirect=self._quiet)

            while _deps_pkgs:
                for package in _deps_pkgs:
                    real_name = re.split(r'[<>=!]', package, maxsplit=1)[0]
                    print_scpt(f'{args} {package}', self._file, redirect=self._quiet)

                    temp = copy.copy(args)
                    temp[3] = 'uninstall'
                    print_scpt(f'{" ".join(temp)} {real_name}', self._file, redirect=self._quiet)
                    sudo(f'{path} -m pip uninstall {real_name} --yes', self._file, sethome=True,
                         askpass=self._askpass, redirect=self._quiet, timeout=self._timeout)

                    temp = copy.copy(args)
                    temp[3] = 'install'
                    print_scpt(f'{" ".join(temp)} {package}', self._file, redirect=self._quiet)
                    if not sudo(f'{path} -m pip install {package}', self._file, sethome=True,
                                askpass=self._askpass, redirect=self._quiet, timeout=self._timeout):
                        with contextlib.suppress(ValueError):
                            self._pkgs.remove(real_name)
                _deps_pkgs = _proc_check()
            text = f'macdaily-update: {green}pip{reset}: all broken dependencies fixed'
        else:
            text = f'macdaily-update: {red}pip{reset}: all broken dependencies remain'
        print_text(text, self._file, redirect=self._quiet)
