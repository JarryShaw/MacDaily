# -*- coding: utf-8 -*-

import abc
import shutil
import sys

from macdaily.cls.command import Command
from macdaily.util.const.term import bold, flash, red, red_bg, reset
from macdaily.util.tools.print import print_info, print_term


class SystemCommand(Command):

    @property
    def mode(self):
        return 'system'

    @property
    def name(self):
        return 'macOS Software Update'

    @property
    def desc(self):
        return ('system software', 'system software')

    def _check_exec(self):
        self._var__exec_path = shutil.which('softwareupdate')
        flag = (self._var__exec_path is not None)
        if not flag:
            print(f'macdaily-{self.cmd}: {red_bg}{flash}system{reset}: command not found', file=sys.stderr)
            text = (f'macdaily-{self.cmd}: {red}system{reset}: '
                    "you may add `softwareupdate' to PATH through the following command -- "
                    f"""`{bold}echo 'export PATH="/usr/sbin:$PATH"' >> ~/.bash_profile{reset}'""")
            print_term(text, self._file, redirect=self._qflag)
        return flag

    def _loc_exec(self):
        self._exec = {self._var__exec_path}
        del self._var__exec_path

    @abc.abstractmethod
    def _check_list(self, path):
        self._var__rcmd_pkgs = set()  # pylint: disable=attribute-defined-outside-init
        self._var__norm_pkgs = set()  # pylint: disable=attribute-defined-outside-init

    def _check_pkgs(self, path):
        self._check_list(path)
        text = 'Checking existence of specified packages'
        print_info(text, self._file, redirect=self._vflag)

        _rcmd_pkgs = list()
        _norm_pkgs = list()
        _lost_pkgs = list()
        for package in self._packages:
            if package in self._var__rcmd_pkgs:
                _rcmd_pkgs.append(package)
            elif package in self._var__norm_pkgs:
                _norm_pkgs.append(package)
            else:
                _lost_pkgs.append(package)
        self._lost.extend(_lost_pkgs)

        self._var__real_pkgs = self._var__rcmd_pkgs | self._var__norm_pkgs  # pylint: disable=attribute-defined-outside-init
        self._var__lost_pkgs = set(_lost_pkgs)  # pylint: disable=attribute-defined-outside-init
        self._var__rcmd_pkgs = set(_rcmd_pkgs)  # pylint: disable=attribute-defined-outside-init
        self._var__norm_pkgs = set(_norm_pkgs)  # pylint: disable=attribute-defined-outside-init
        self._var__temp_pkgs = self._var__rcmd_pkgs | self._var__norm_pkgs  # pylint: disable=attribute-defined-outside-init
