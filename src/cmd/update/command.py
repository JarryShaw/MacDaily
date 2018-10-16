# -*- coding: utf-8 -*-

import abc

from macdaily.cmd.command import Command


class UpdateCommand(Command):

    @property
    def cmd(self):
        return 'update'

    @property
    def act(self):
        return ('upgrade', 'upgraded', 'up-to-date')

    def _run_proc(self):
        self._pkgs = list()
        self._fail = list()
        self._lost = list()
        for path in self._exec:
            self._proc_logging(path)
            self._proc_update(path)

    def _proc_logging(self, path):
        if self._packages:
            self._check_pkgs(path)
            self._did_you_mean()
        else:
            self._check_list(path)

    @abc.abstractmethod
    def _check_pkgs(self, path):
        self.__temp_pkgs = self._packages

    @abc.abstractmethod
    def _check_list(self, path):
        self.__temp_pkgs = set()

    @abc.abstractmethod
    def _proc_update(self, path):
        pass
