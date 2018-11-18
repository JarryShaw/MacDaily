# -*- coding: utf-8 -*-

import os

from macdaily.cmd.logging import LoggingCommand
from macdaily.core.pip import PipCommand
from macdaily.util.misc import print_info, print_scpt, script


class PipLogging(PipCommand, LoggingCommand):

    @property
    def log(self):
        return 'requirements'

    @property
    def ext(self):
        return 'txt'

    def _parse_args(self, namespace):
        self._brew = namespace.get('brew', False)
        self._cpython = namespace.get('cpython', False)
        self._exclude_editable = namespace.get('exclude_editable', False)
        self._pypy = namespace.get('pypy', False)
        self._system = namespace.get('system', False)

        self._quiet = namespace.get('quiet', False)
        self._verbose = namespace.get('verbose', False)

    def _proc_logging(self, path):
        text = 'Listing installed {}'.format(self.desc[1])
        print_info(text, self._file, redirect=self._qflag)

        argv = [path, 'freeze']
        if self._exclude_editable:
            argv.append('--exclude-editable')
        logfile = os.path.join(self._logroot, '{}-{}.{}'.format(self.log, path, self.ext))

        print_scpt(argv, self._file, redirect=self._qflag)
        script(argv, self._file, suffix='> {}'.format(logfile),
               shell=True, timeout=self._timeout, redirect=self._vflag)
