# -*- coding: utf-8 -*-

import copy
import json
import sys
import traceback

from macdaily.cmd.update import UpdateCommand
from macdaily.core.pip import PipCommand
from macdaily.util.misc import (date, make_stderr, print_info, print_scpt,
                                print_text, sudo)

try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess


class PipUpdate(PipCommand, UpdateCommand):

    def _parse_args(self, namespace):
        self._brew = namespace.get('brew', False)
        self._cpython = namespace.get('cpython', False)
        self._no_cleanup = namespace.get('no_cleanup', False)
        self._pre = namespace.get('pre', False)
        self._pypy = namespace.get('pypy', False)
        self._system = namespace.get('system', False)
        self._user = namespace.get('user', False)

        self._all = namespace.get('all', False)
        self._quiet = namespace.get('quiet', False)
        self._verbose = namespace.get('verbose', False)
        self._yes = namespace.get('yes', False)

        self._logging_opts = namespace.get('logging', str()).split()
        self._update_opts = namespace.get('update', str()).split()

    def _check_list(self, path):
        argv = [path, '-m', 'pip', 'list', '--outdated']
        if self._pre:
            argv.append('--pre')
        argv.extend(self._logging_opts)

        text = f'Checking outdated {self.desc[1]}'
        print_info(text, self._file, redirect=self._vflag)

        temp = copy.copy(argv)
        temp.append('--format=columns')
        args = ' '.join(temp)
        print_scpt(args, self._file, redirect=self._vflag)
        with open(self._file, 'a') as file:
            file.write(f'Script started on {date()}\n')
            file.write(f'command: {args!r}\n')

        argv.append('--format=json')
        try:
            proc = subprocess.check_output(argv, stderr=make_stderr(self._vflag))
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
                file.write(f'Script done on {date()}\n')

    def _proc_update(self, path):
        text = f'Upgrading outdated {self.desc[1]}'
        print_info(text, self._file, redirect=self._qflag)

        argv = [path, '-m', 'pip', 'install', '--upgrade']
        if self._pre:
            argv.append('--pre')
        if self._user:
            argv.append('--user')
        if self._quiet:
            argv.append('--quiet')
        if self._verbose:
            argv.append('--verbose')
        argv.extend(self._update_opts)

        argc = ' '.join(argv)
        for package in self._var__temp_pkgs:
            args = f'{argc} {package}'
            print_scpt(args, self._file, redirect=self._qflag)
            if sudo(args, self._file, self._password, timeout=self._timeout,
                    redirect=self._qflag, verbose=self._vflag, sethome=True):
                self._fail.append(package)
            else:
                self._pkgs.append(package)
        del self._var__temp_pkgs
