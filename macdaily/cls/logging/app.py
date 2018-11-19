# -*- coding: utf-8 -*-

import os
import shutil
import sys
import traceback

from macdaily.cmd.logging import LoggingCommand
from macdaily.util.const import ROOT
from macdaily.util.misc import (date, make_pipe, make_stderr, print_info,
                                print_scpt, print_text)

try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess


class AppLogging(LoggingCommand):

    @property
    def log(self):
        return 'macOS'

    @property
    def ext(self):
        return '.log'

    @property
    def mode(self):
        return 'app'

    @property
    def name(self):
        return 'macOS Application Logging'

    @property
    def desc(self):
        return ('Mac Application', 'Mac Applications')

    def _check_exec(self):
        return True

    def _parse_args(self, namespace):
        self._quiet = namespace.get('quiet', False)
        self._verbose = namespace.get('verbose', False)

    def _loc_exec(self):
        self._exec = {sys.executable}

    def _proc_logging(self, path):
        text = 'Listing installed {}'.format(self.desc[1])
        print_info(text, self._file, redirect=self._qflag)

        suffix = path.replace('/', ':')
        logfile = os.path.join(self._logroot, '{}-{}{}'.format(self.log, suffix, self.ext))

        find = os.path.join(ROOT, 'res', 'find.py')
        argv = ['sudo', '--stdin', "--prompt=''", path, find, '/']
        args = ' '.join(argv)
        print_scpt(args, self._file, redirect=self._qflag)
        with open(self._file, 'a') as file:
            file.write('Script started on {}\n'.format(date()))
            file.write('command: {!r}\n'.format(args))

        try:
            with make_pipe(self._password, self._vflag) as pipe:
                proc = subprocess.check_output(argv, stdin=pipe.stdout, stderr=make_stderr(self._vflag))
        except subprocess.CalledProcessError:
            print_text(traceback.format_exc(), self._file, redirect=self._vflag)
            _real_pkgs = dict()
        else:
            context = proc.decode()
            print_text(context, self._file, redirect=self._vflag)

            with open(logfile, 'w') as file:
                file.writelines(filter(None, context.strip().splitlines(True)))
        finally:
            with open(self._file, 'a') as file:
                file.write('Script done on {}\n'.format(date()))
