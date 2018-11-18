# -*- coding: utf-8 -*-

import os

from macdaily.cmd.logging import LoggingCommand
from macdaily.core.apm import ApmCommand
from macdaily.util.misc import print_info, print_scpt, script


class ApmLogging(ApmCommand, LoggingCommand):

    @property
    def log(self):
        return 'packages'

    @property
    def ext(self):
        return 'txt'

    def _parse_args(self, namespace):
        self._beta = namespace.get('beta', False)

        self._quiet = namespace.get('quiet', False)
        self._verbose = namespace.get('verbose', False)

    def _proc_logging(self, path):
        text = f'Listing installed {self.desc[1]}'
        print_info(text, self._file, redirect=self._qflag)

        argv = [path, 'list', '--installed', '--bare']
        logfile = os.path.join(self._logroot, f'{self.log}-{path}.{self.ext}')

        print_scpt(argv, self._file, redirect=self._qflag)
        script(argv, self._file, suffix=f'> {logfile}',
               shell=True, timeout=self._timeout, redirect=self._vflag)
