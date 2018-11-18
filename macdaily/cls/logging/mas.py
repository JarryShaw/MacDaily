# -*- coding: utf-8 -*-

import os

from macdaily.cmd.logging import LoggingCommand
from macdaily.core.mas import MasCommand
from macdaily.util.misc import print_info, print_scpt, script


class MasLogging(MasCommand, LoggingCommand):

    @property
    def log(self):
        return 'applications'

    @property
    def ext(self):
        return 'log'

    def _parse_args(self, namespace):
        self._quiet = namespace.get('quiet', False)
        self._verbose = namespace.get('verbose', False)

    def _proc_logging(self, path):
        text = 'Listing installed {}'.format(self.desc[1])
        print_info(text, self._file, redirect=self._qflag)

        logfile = os.path.join(self._logroot, '{}-{}.{}'.format(self.log, path, self.ext))
        argv = [path, 'list']

        print_scpt(argv, self._file, redirect=self._qflag)
        script(argv, self._file, suffix='> {}'.format(logfile),
               shell=True, timeout=self._timeout, redirect=self._vflag)
