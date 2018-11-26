# -*- coding: utf-8 -*-

import abc

from macdaily.cls.command import Command
from macdaily.util.misc import print_info


class DependencyCommand(Command):

    @property
    def cmd(self):
        return 'dependency'

    @property
    def act(self):
        return ('query', 'queried', 'displayed')

    @property
    def job(self):
        return ('dependency', 'dependencies')

    def _run_proc(self):
        self._pkgs = list()
        self._fail = list()
        self._lost = list()
        for path in self._exec:
            text = f'Using {self.name} executable {path!r}'
            print_info(text, self._file, redirect=self._qflag)
            if self._proc_logging(path):
                self._proc_dependency(path)
            else:
                text = f'No {self.desc[1]} to query for executable {path!r}'
                print_info(text, self._file, redirect=self._qflag)

    def _proc_logging(self, path):
        if self._packages:
            self._check_pkgs(path)
            self._did_you_mean()
        else:
            self._check_list(path)
        return bool(self._var__temp_pkgs)

    @abc.abstractmethod
    def _check_pkgs(self, path):
        self._var__temp_pkgs = self._packages

    @abc.abstractmethod
    def _check_list(self, path):
        self._var__temp_pkgs = set()

    @abc.abstractmethod
    def _proc_dependency(self, path):
        pass
