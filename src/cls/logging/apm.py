# -*- coding: utf-8 -*-

import os
import traceback

from macdaily.cmd.logging import LoggingCommand
from macdaily.core.apm import ApmCommand
from macdaily.util.compat import subprocess
from macdaily.util.tools.make import make_stderr
from macdaily.util.tools.misc import date
from macdaily.util.tools.print import print_info, print_scpt, print_text


class ApmLogging(ApmCommand, LoggingCommand):

    @property
    def log(self):
        return 'packages'

    @property
    def ext(self):
        return '.txt'

    def _parse_args(self, namespace):
        self._beta = namespace.get('beta', False)  # pylint: disable=attribute-defined-outside-init

        self._quiet = namespace.get('quiet', False)  # pylint: disable=attribute-defined-outside-init
        self._verbose = namespace.get('verbose', False)  # pylint: disable=attribute-defined-outside-init

    def _proc_logging(self, path):
        text = f'Listing installed {self.desc[1]}'
        print_info(text, self._file, redirect=self._qflag)

        suffix = path.replace('/', ':')
        logfile = os.path.join(self._logroot, f'{self.log}-{suffix}{self.ext}')

        argv = [path, 'list', '--installed', '--bare']
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
                file.writelines(filter(None, context.strip().splitlines(True)))  # pylint: disable=filter-builtin-not-iterating
        finally:
            with open(self._file, 'a') as file:
                file.write(f'Script done on {date()}\n')
