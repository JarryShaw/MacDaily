# -*- coding: utf-8 -*-

import shutil
import sys
import traceback

from macdaily.cls.command import Command
from macdaily.util.compat import subprocess
from macdaily.util.const.term import bold, flash, red, red_bg, reset
from macdaily.util.tools.make import make_stderr
from macdaily.util.tools.misc import date
from macdaily.util.tools.print import print_info, print_scpt, print_term, print_text


class MasCommand(Command):  # pylint: disable=abstract-method

    @property
    def mode(self):
        return 'mas'

    @property
    def name(self):
        return 'Mac App Store CLI'

    @property
    def desc(self):
        return ('macOS application', 'macOS applications')

    def _check_exec(self):
        self._var__exec_path = shutil.which('mas')
        flag = (self._var__exec_path is not None)
        if not flag:
            print(f'macdaily-{self.cmd}: {red_bg}{flash}mas{reset}: command not found', file=sys.stderr)
            text = (f'macdaily-{self.cmd}: {red}mas{reset}: you may download MAS through following command -- '
                    f"`{bold}brew install mas{reset}'")
            print_term(text, self._file, redirect=self._qflag)
        return flag

    def _loc_exec(self):
        self._exec = {self._var__exec_path}
        del self._var__exec_path

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
            proc = subprocess.check_output(argv, stderr=make_stderr(self._vflag))
        except subprocess.CalledProcessError:
            print_text(traceback.format_exc(), self._file, redirect=self._vflag)
            _real_pkgs = set()
        else:
            context = proc.decode()
            print_text(context, self._file, redirect=self._vflag)

            _list_pkgs = dict()
            for line in context.strip().splitlines():
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

        self._var__real_pkgs = set(_real_pkgs)  # pylint: disable=attribute-defined-outside-init
        self._var__lost_pkgs = set(_lost_pkgs)  # pylint: disable=attribute-defined-outside-init
        self._var__temp_pkgs = set(_temp_pkgs)  # pylint: disable=attribute-defined-outside-init
