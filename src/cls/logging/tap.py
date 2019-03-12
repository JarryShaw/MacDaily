# -*- coding: utf-8 -*-

import os
import shutil
import sys
import tempfile
import traceback

from macdaily.cmd.logging import LoggingCommand
from macdaily.util.compat import subprocess
from macdaily.util.const.term import bold, flash, purple_bg, red, red_bg, reset, under
from macdaily.util.tools.get import get_logfile
from macdaily.util.tools.make import make_stderr
from macdaily.util.tools.print import print_info, print_scpt, print_term, print_text
from macdaily.util.tools.script import script


class TapLogging(LoggingCommand):

    @property
    def log(self):
        return 'Brewfile'

    @property
    def ext(self):
        return ''

    @property
    def mode(self):
        return 'tap'

    @property
    def name(self):
        return 'Homebrew Taps'

    @property
    def desc(self):
        return ('third-party repository', 'third-party repositories')

    def _check_exec(self):
        try:
            subprocess.check_call(['brew', 'command', 'bundle'],
                                  stdout=subprocess.DEVNULL, stderr=make_stderr(self._vflag))
        except subprocess.CalledProcessError:
            print_text(traceback.format_exc(), self._file, redirect=self._vflag)
            print(f'macdaily-{self.cmd}: {red_bg}{flash}tap{reset}: command not found', file=sys.stderr)
            text = (f'macdaily-{self.cmd}: {red}tap{reset}: you may find Bundler on '
                    f'{purple_bg}{under}https://github.com/Homebrew/homebrew-bundle{reset}, '
                    f'or install Bundler through following command -- '
                    f"`{bold}brew tap homebrew/bundle{reset}'")
            print_term(text, self._file, redirect=self._qflag)
            return False
        self._var__exec_path = shutil.which('brew')
        return True

    def _parse_args(self, namespace):
        self._quiet = namespace.get('quiet', False)  # pylint: disable=attribute-defined-outside-init
        self._verbose = namespace.get('verbose', False)  # pylint: disable=attribute-defined-outside-init

    def _loc_exec(self):
        self._exec = {self._var__exec_path}
        del self._var__exec_path

    def _proc_logging(self, path):
        text = f'Listing installed {self.desc[1]}'
        print_info(text, self._file, redirect=self._qflag)

        suffix = path.replace('/', ':')
        with tempfile.NamedTemporaryFile() as _temp_file:
            logfile = os.path.join(self._logroot, f'{self.log}-{suffix}{self.ext}')
            argv = [path, 'bundle', 'dump', '--force', f'--file={_temp_file.name}']

            print_scpt(argv, self._file, redirect=self._qflag)
            script(argv, self._file, shell=True,
                   timeout=self._timeout, redirect=self._vflag)

            with open(_temp_file.name, 'r') as file:
                context = file.read()
            print_text(context, get_logfile(), redirect=self._vflag)

        with open(logfile, 'w') as file:
            file.writelines(filter(lambda s: s.startswith('tap'), context.strip().splitlines(True)))  # pylint: disable=filter-builtin-not-iterating
