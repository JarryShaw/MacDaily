# -*- coding: utf-8 -*-

import abc

from macdaily.cls.command import Command
from macdaily.util.misc import print_info

try:
    import pathlib2 as pathlib
except ImportError:
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
    def jon(self):
        return ('logging', 'logging')

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

    def __init__(self, namespace, filename, timeout, *args, **kwargs):
        self._qflag = namespace.get('quiet', False)
        self._vflag = self._qflag or (not namespace.get('verbose', False))

        text = 'Running {} command for {}'.format(self.cmd, self.mode)
        print_info(text, filename, redirect=self._qflag)

        # exit if no executable found
        if self._check_exec():
            # assign members
            self._file = filename
            self._timeout = timeout
            self._logroot = str(pathlib.Path(filename).resolve().parents[1])

            # mainloop process
            self._parse_args(namespace)
            self._loc_exec()
            self._run_proc()

        # remove temp vars
        [delattr(self, attr) for attr in filter(lambda s: s.startswith('_var_'), dir(self))]

    def _run_proc(self):
        self._pkgs = list()
        self._fail = list()
        self._lost = list()
        for path in self._exec:
            text = 'Using {} executable {!r}'.format(self.name, path)
            print_info(text, self._file, redirect=self._qflag)
            self._proc_logging(path)

    @abc.abstractmethod
    def _proc_logging(self, path):
        pass
