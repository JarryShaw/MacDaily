# -*- coding: utf-8 -*-

import os
import sys
import traceback

from macdaily.cmd.logging import LoggingCommand
from macdaily.core.pip import PipCommand
from macdaily.util.misc import (date, make_stderr, print_info, print_scpt,
                                print_text)

try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess


class PipLogging(PipCommand, LoggingCommand):

    @property
    def log(self):
        return 'requirements'

    @property
    def ext(self):
        return '.txt'

    def _parse_args(self, namespace):
        self._brew = namespace.get('brew', False)
        self._cpython = namespace.get('cpython', False)
        self._exclude_editable = namespace.get('exclude_editable', False)
        self._pypy = namespace.get('pypy', False)
        self._system = namespace.get('system', False)

        self._quiet = namespace.get('quiet', False)
        self._verbose = namespace.get('verbose', False)

    def _proc_logging(self, path):
        text = f'Listing installed {self.desc[1]}'
        print_info(text, self._file, redirect=self._qflag)

        suffix = path.replace('/', ':')
        logfile = os.path.join(self._logroot, f'{self.log}-{suffix}{self.ext}')

        argv = [path, '-m', 'pip', 'freeze']
        if self._exclude_editable:
            argv.append('--exclude-editable')

        args = ' '.join(argv)
        print_scpt(args, self._file, redirect=self._qflag)
        with open(self._file, 'a') as file:
            file.write(f'Script started on {date()}\n')
            file.write(f'command: {args!r}\n')

        try:
            proc = subprocess.check_output(argv, stderr=make_stderr(self._vflag))
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
                file.write(f'Script done on {date()}\n')
