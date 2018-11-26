# -*- coding: utf-8 -*-

import abc
import shutil
import sys
import traceback

from macdaily.cls.command import Command
from macdaily.util.const import flash, purple_bg, red, red_bg, reset, under
from macdaily.util.misc import (date, make_stderr, print_info, print_scpt,
                                print_term, print_text)

try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess


class ApmCommand(Command):

    @property
    def mode(self):
        return 'apm'

    @property
    def name(self):
        return 'Atom Package Manager'

    @property
    def desc(self):
        return ('Atom plug-in', 'Atom plug-ins')

    def _check_exec(self):
        self._var__exec_path = (shutil.which('apm'), shutil.which('apm-beta'))
        flag = not (self._var__exec_path == (None, None))
        if not flag:
            print(f'macdaily-{self.cmd}: {red_bg}{flash}apm{reset}: command not found', file=sys.stderr)
            text = (f'macdaily-{self.cmd}: {red}apm{reset}: you may download Atom from '
                    f'{purple_bg}{under}https://atom.io{reset}')
            print_term(text, self._file, redirect=self._qflag)
        return flag

    def _pkg_args(self, namespace):
        flag = super()._pkg_args(namespace)

        # if ``beta`` not set, ``apm-beta`` is the only executable
        if not self._beta and self._var__exec_path[0] is None:
            return False
        return flag

    @abc.abstractmethod
    def _parse_args(self, namespace):
        super()._parse_args(namespace)
        self._beta = namespace.get('beta', False)

    def _loc_exec(self):
        if self._beta:
            self._exec = set(filter(None, self._var__exec_path))
        else:
            self._exec = {self._var__exec_path[0]}
        del self._var__exec_path

    def _check_pkgs(self, path):
        text = f'Listing installed {self.desc[1]}'
        print_info(text, self._file, redirect=self._vflag)

        argv = [path, 'list', '--bare', '--no-color']
        args = ' '.join(argv)
        print_scpt(args, self._file, redirect=self._vflag)
        with open(self._file, 'a') as file:
            file.write(f'Script started on {date()}\n')
            file.write(f'command: {args!r}\n')

        try:
            proc = subprocess.check_output(argv, stderr=make_stderr(self._vflag))
        except subprocess.CalledProcessError:
            print_text(traceback.format_exc(), self._file, redirect=self._vflag)
            _real_pkgs = set()
        else:
            context = proc.decode()
            print_text(context, self._file, redirect=self._vflag)

            _list_pkgs = list()
            for line in filter(None, context.strip().splitlines()):
                _list_pkgs.append(line.split('@')[0])
            _real_pkgs = set(_list_pkgs)
        finally:
            with open(self._file, 'a') as file:
                file.write(f'Script done on {date()}\n')

        text = 'Checking existence of specified packages'
        print_info(text, self._file, redirect=self._vflag)

        _temp_pkgs = list()
        _lost_pkgs = list()
        for package in self._packages:
            if package in _real_pkgs:
                _temp_pkgs.append(package)
            else:
                _lost_pkgs.append(package)

        self._var__real_pkgs = set(_real_pkgs)
        self._var__lost_pkgs = set(_lost_pkgs)
        self._var__temp_pkgs = set(_temp_pkgs)
