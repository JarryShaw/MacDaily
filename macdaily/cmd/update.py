# -*- coding: utf-8 -*-

import abc

from macdaily.cls.command import Command
from macdaily.util.tools.print import print_info


class UpdateCommand(Command):

    @property
    def cmd(self):
        return 'update'

    @property
    def act(self):
        return ('upgrade', 'upgraded', 'up-to-date')

    @property
    def job(self):
        return ('update', 'updates')

    def _run_proc(self):
        self._pkgs = list()
        self._fail = list()
        self._lost = list()
        for path in self._exec:
            text = 'Using {} executable {!r}'.format(self.name, path)
            print_info(text, self._file, redirect=self._qflag)
            if self._proc_logging(path):
                self._proc_update(path)
            else:
                text = 'No {} to upgrade for executable {!r}'.format(self.desc[1], path)
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
    def _proc_update(self, path):
        pass
