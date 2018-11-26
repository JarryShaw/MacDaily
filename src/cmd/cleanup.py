# -*- coding: utf-8 -*-

import abc

from macdaily.cls.command import Command
from macdaily.util.misc import print_info


class CleanupCommand(Command):

    @property
    def cmd(self):
        return 'cleanup'

    @property
    def act(self):
        return ('prune', 'pruned', 'cleanup')

    @property
    def job(self):
        return ('cleanup', 'cleanup')

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
        self._no_cleanup = False

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
        self._proc_cleanup()

    @abc.abstractmethod
    def _proc_cleanup(self):
        pass
