# -*- coding: utf-8 -*-

import re
import sys
import traceback

from macdaily.cmd.logging import LoggingCommand
from macdaily.core.brew import BrewCommand
from macdaily.util.misc import (date, make_stderr, print_info, print_scpt,
                                print_text)

try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess


class BrewLogging(BrewCommand, LoggingCommand):

    def _parse_args(self, namespace):
        self._describe = namespace.get('describe', False)

        self._quiet = namespace.get('quiet', False)
        self._verbose = namespace.get('verbose', False)

    def _proc_logging(self, path):
        text = f'Listing installed {self.desc[1]}'
        print_info(text, self._file, redirect=self._qflag)

        argv = [path, 'bundle', 'dump', '--force', f'--file=-']
        if self._describe:
            argv.append('--describe')

        args = ' '.join(argv)
        print_scpt(args, self._file, redirect=self._qflag)
        with open(self._file, 'a') as file:
            file.write(f'Script started on {date()}\n')
            file.write(f'command: {args!r}\n')

        stderr = make_stderr(self._vflag, sys.stderr)
        try:
            proc = subprocess.check_output(argv, stderr=stderr)
        except subprocess.SubprocessError:
            print_text(traceback.format_exc(), self._file, redirect=self._vflag)
        else:
            context = proc.decode()
            with open(self._logfile, 'w') as file:
                file.writelines(filter(lambda s: s.startswith('brew'), context.strip().splitlines()))
        finally:
            with open(self._file, 'a') as file:
                file.write(f'Script done on {date()}\n')
