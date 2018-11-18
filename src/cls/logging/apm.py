# -*- coding: utf-8 -*-

from macdaily.cmd.logging import LoggingCommand
from macdaily.core.apm import ApmCommand
from macdaily.util.misc import print_info, print_scpt, script


class ApmLogging(ApmCommand, LoggingCommand):

    def _parse_args(self, namespace):
        self._beta = namespace.get('beta', False)

        self._quiet = namespace.get('quiet', False)
        self._verbose = namespace.get('verbose', False)

        self._logging_opts = namespace.get('logging', str()).split()

    def _proc_logging(self, path):
        text = f'Listing installed {self.desc[1]}'
        print_info(text, self._file, redirect=self._qflag)

        argv = [path, 'list']
        argv.extend(self._logging_opts)
        argv.append('--installed')
        argv.append('--bare')

        print_scpt(argv, self._file, redirect=self._qflag)
        script(argv, self._file, suffix=f'> {self._logfile}',
               shell=True, timeout=self._timeout, redirect=self._vflag)
