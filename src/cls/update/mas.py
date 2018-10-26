# -*- coding: utf-8 -*-

import traceback

from macdaily.cmd.update import UpdateCommand
from macdaily.core.mas import MasCommand
from macdaily.util.const import bold, reset
from macdaily.util.misc import date, print_info, print_scpt, print_text, sudo

try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess


class MasUpdate(UpdateCommand):

    def _parse_args(self, namespace):
        self._all = namespace.pop('all', False)
        self._quiet = namespace.pop('quiet', False)
        self._yes = namespace.pop('yes', False)

        self._logging_opts = namespace.pop('logging', str()).split()
        self._update_opts = namespace.pop('update', str()).split()

    def _check_pkgs(self, path):
        text = f'Listing installed {self.desc[1]}'
        print_info(text, self._file, redirect=self._vflag)

        argv = [path, 'list']
        args = ' '.join(argv)
        print_scpt(args, self._file, redirect=self._vflag)
        with open(self._file, 'a') as file:
            file.write(f'Script started on {date()}\n')
            file.write(f'command: {args!r}\n')

        try:
            proc = subprocess.check_output(argv, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            print_text(traceback.format_exc(), self._file, redirect=self._vflag)
            _real_pkgs = set()
        else:
            context = proc.decode()
            print_text(context, self._file, redirect=self._vflag)

            _list_pkgs = dict()
            for line in context.strip().split('\n'):
                content = line.split()
                _list_pkgs[content[1:-1]] = content[0]
            _real_pkgs = set(_list_pkgs.keys())
        finally:
            with open(self._file, 'a') as file:
                file.write(f'Script done on {date()}\n')

        text = 'Checking existence of specified packages'
        print_info(text, self._file, redirect=self._vflag)

        _temp_pkgs = list()
        _lost_pkgs = list()
        for package in self._packages:
            if package in _real_pkgs:
                _temp_pkgs.append((_list_pkgs[package], package))
            else:
                _lost_pkgs.append(package)
        self._lost.extend(_lost_pkgs)

        self.__real_pkgs = set(_real_pkgs)
        self.__lost_pkgs = set(_lost_pkgs)
        self.__temp_pkgs = set(_temp_pkgs)

    def _check_list(self, path):
        text = f'Checking outdated {self.desc[1]}'
        print_info(text, self._file, redirect=self._vflag)

        argv = [path, 'outdated']
        argv.extend(self._logging_opts)
        args = ' '.join(argv)
        print_scpt(args, self._file, redirect=self._vflag)
        with open(self._file, 'a') as file:
            file.write(f'Script started on {date()}\n')
            file.write(f'command: {args!r}\n')

        try:
            proc = subprocess.check_output(argv, stderr=subprocess.DEVNULL)
        except subprocess.SubprocessError:
            print_text(traceback.format_exc(), self._file, redirect=self._vflag)
            self.__temp_pkgs = set()
        else:
            context = proc.decode()
            print_text(context, self._file, redirect=self._vflag)

            _temp_pkgs = list()
            for line in context.strip().split('\n'):
                content = line.split()
                _temp_pkgs.append((content[0], content[1:-1]))
            self.__temp_pkgs = set(_temp_pkgs)
        finally:
            with open(self._file, 'a') as file:
                file.write(f'Script done on {date()}\n')

    def _proc_update(self, path):
        text = f'Upgrading outdated {self.desc[1]}'
        print_info(text, self._file, redirect=self._qflag)

        argv = [path, 'upgrade']
        argv.append(self._update_opts)

        argc = ' '.join(argv)
        for (code, package) in self.__temp_pkgs:
            print_scpt(f'{argc} {package} [{code}]', self._file, redirect=self._qflag)
            if sudo(f'{argc} {code}', self._file, redirect=self._qflag,
                    askpass=self._askpass, timeout=self._timeout):
                self._fail.append(package)
            else:
                self._pkgs.append(package)
        del self.__temp_pkgs
