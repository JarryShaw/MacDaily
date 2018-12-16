# -*- coding: utf-8 -*-

import abc
import os
import sys

from macdaily.cls.command import Command
from macdaily.util.misc import print_info

if sys.version_info[:2] == (3, 4):
    import pathlib2 as pathlib
else:
    import pathlib


class LoggingCommand(Command):

    @property
    @abc.abstractmethod
    def log(self):
        return NotImplemented

    @property
    @abc.abstractmethod
    def ext(self):
        return NotImplemented

    @property
    def cmd(self):
        return 'logging'

    @property
    def act(self):
        return ('log', 'logged', 'recorded')

    @property
    def job(self):
        return ('logging', 'logging')

    @property
    def sample(self):
        return os.path.join(self._logroot, f'{self.log}{self.ext}')

    @property
    def packages(self):
        return NotImplemented

    @property
    def ignored(self):
        return NotImplemented

    @property
    def failed(self):
        return NotImplemented

    @property
    def notfound(self):
        return NotImplemented

    def __init__(self, namespace, filename, timeout, confirm,
                 askpass, password, disk_dir, brew_renew=None):
        self._qflag = namespace.get('quiet', False)
        self._vflag = self._qflag or (not namespace.get('verbose', False))

        text = f'Running {self.cmd} command for {self.mode}'
        print_info(text, filename, redirect=self._qflag)

        # assign members
        self._file = filename
        self._timeout = timeout
        self._confirm = confirm
        self._askpass = askpass
        self._password = password
        self._disk_dir = disk_dir
        self._brew_renew = brew_renew
        self._logroot = str(pathlib.Path(filename).resolve().parents[1])

        # exit if no executable found
        if self._check_exec():
            # mainloop process
            self._pkg_args(namespace)
            self._loc_exec()
            self._run_proc()

        # remove temp vars
        [delattr(self, attr) for attr in filter(lambda s: s.startswith('_var_'), dir(self))]

    def _pkg_args(self, namespace):
        return self._parse_args(namespace)

    def _run_proc(self):
        for path in self._exec:
            text = f'Using {self.name} executable {path!r}'
            print_info(text, self._file, redirect=self._qflag)
            self._proc_logging(path)

    @abc.abstractmethod
    def _proc_logging(self, path):
        pass
