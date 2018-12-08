# -*- coding: utf-8 -*-

import abc
import copy

from macdaily.cls.command import Command
from macdaily.util.misc import print_info


class InstallCommand(Command):

    @property
    def cmd(self):
        return 'install'

    @property
    def act(self):
        return ('install', 'installed', 'installed')

    @property
    def job(self):
        return ('installation', 'installation')

    @property
    def ignored(self):
        return NotImplemented

    @property
    def notfound(self):
        return NotImplemented

    def _pkg_args(self, namespace):
        """Return if there's packages for main process."""
        self._merge_packages(namespace)
        self._parse_args(namespace)

        self._pkgs = list()
        self._fail = list()

        return bool(self._packages)

    def _run_proc(self):
        self._pkgs = list()
        self._fail = list()
        for path in self._exec:
            text = 'Using {} executable {!r}'.format(self.name, path)
            print_info(text, self._file, redirect=self._qflag)

            self._var__temp_pkgs = self._packages
            if self._check_confirm():
                self._proc_install(path)
            else:
                text = 'No {} to install for executable {!r}'.format(self.desc[1], path)
                print_info(text, self._file, redirect=self._qflag)
            self._proc_fixmissing(path)
        self._proc_cleanup()

    @abc.abstractmethod
    def _proc_install(self, path):
        pass
