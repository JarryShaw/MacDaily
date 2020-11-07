# -*- coding: utf-8 -*-

import abc

from macdaily.cls.command import Command
from macdaily.util.tools.print import print_info


class ReinstallCommand(Command):

    @property
    def cmd(self):
        return 'reinstall'

    @property
    def act(self):
        return ('reinstall', 'reinstalled', 'reinstalled')

    @property
    def job(self):
        return ('reinstallation', 'reinstallation')

    def _run_proc(self):
        self._pkgs = list()
        self._fail = list()
        self._lost = list()
        for path in self._exec:
            text = f'Using {self.name} executable {path!r}'
            print_info(text, self._file, redirect=self._qflag)
            if self._proc_logging(path):
                self._proc_reinstall(path)
            else:
                text = f'No {self.desc[1]} to reinstall for executable {path!r}'
                print_info(text, self._file, redirect=self._qflag)
            self._proc_fixmissing(path)
        self._proc_cleanup()

    def _proc_logging(self, path):
        if self._packages:
            self._check_pkgs(path)
            self._did_you_mean()
        else:
            self._check_list(path)
        return self._check_confirm(path)

    @abc.abstractmethod
    def _check_pkgs(self, path):
        self._var__temp_pkgs = self._packages  # pylint: disable=attribute-defined-outside-init

    @abc.abstractmethod
    def _check_list(self, path):
        self._var__temp_pkgs = set()  # pylint: disable=attribute-defined-outside-init

    @abc.abstractmethod
    def _proc_reinstall(self, path):
        pass
