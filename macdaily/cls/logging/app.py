# -*- coding: utf-8 -*-

import os
import shutil
import sys

from macdaily.cmd.logging import LoggingCommand
from macdaily.util.const import ROOT
from macdaily.util.misc import print_info, print_scpt, sudo


class AppLogging(LoggingCommand):

    @property
    def log(self):
        return 'macOS'

    @property
    def ext(self):
        return 'log'

    @property
    def mode(self):
        return 'app'

    @property
    def name(self):
        return 'macOS Application Logging'

    @property
    def desc(self):
        return ('macOS Application', 'macOS Applications')

    def _check_exec(self):
        return True

    def _parse_args(self, namespace):
        self._quiet = namespace.get('quiet', False)
        self._verbose = namespace.get('verbose', False)

    def _loc_exec(self):
        return {sys.executable}

    def _proc_logging(self, path):
        text = 'Listing installed {}'.format(self.desc[1])
        print_info(text, self._file, redirect=self._qflag)

        logfile = os.path.join(self._logroot, '{}-{}.{}'.format(self.log, path, self.ext))
        find = os.path.join(ROOT, 'res', 'find.py')
        argv = [path, find, '/']

        print_scpt(argv, self._file, redirect=self._qflag)
        sudo(argv, self._file, self._password, suffix='> {}'.format(logfile),
             askpass=self._askpass, verbose=self._vflag, timeout=self._timeout)
