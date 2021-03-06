# -*- coding: utf-8 -*-

import json
import os
import traceback

from macdaily.cmd.logging import LoggingCommand
from macdaily.core.npm import NpmCommand
from macdaily.util.compat import subprocess
from macdaily.util.tools.make import make_stderr
from macdaily.util.tools.misc import date
from macdaily.util.tools.print import print_info, print_scpt, print_text


class NpmLogging(NpmCommand, LoggingCommand):

    @property
    def log(self):
        return 'package'

    @property
    def ext(self):
        return '.json'

    def _parse_args(self, namespace):
        self._long = namespace.get('long', False)  # pylint: disable=attribute-defined-outside-init

        self._quiet = namespace.get('quiet', False)  # pylint: disable=attribute-defined-outside-init
        self._verbose = namespace.get('verbose', False)  # pylint: disable=attribute-defined-outside-init

    def _proc_logging(self, path):
        text = f'Listing installed {self.desc[1]}'
        print_info(text, self._file, redirect=self._qflag)

        suffix = path.replace('/', ':')
        logfile = os.path.join(self._logroot, f'{self.log}-{suffix}{self.ext}')

        argv = [path, 'list', '--global', '--json']
        if self._long:
            argv.append('--long')

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

            content = json.loads(context.strip())
            with open(logfile, 'w') as file:
                json.dump(content, file, indent=2)
        finally:
            with open(self._file, 'a') as file:
                file.write(f'Script done on {date()}\n')
