# -*- coding: utf-8 -*-

import os
import shutil
import sys
import tempfile
import traceback

from macdaily.cmd.logging import LoggingCommand
from macdaily.util.compat import subprocess
from macdaily.util.const.term import (bold, flash, purple_bg, red, red_bg,
                                      reset, under)
from macdaily.util.tools.make import make_stderr
from macdaily.util.tools.print import (print_info, print_scpt, print_term,
                                       print_text)
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
            print('macdaily-{}: {}{}tap{}: command not found'.format(self.cmd, red_bg, flash, reset), file=sys.stderr)
            text = ('macdaily-{}: {}tap{}: you may find Bundler on '
                    '{}{}https://github.com/Homebrew/homebrew-bundle{}, '
                    'or install Bundler through following command -- '
                    "`{}brew tap homebrew/bundle{}'".format(self.cmd, red, reset, purple_bg, under, reset, bold, reset))
            print_term(text, self._file, redirect=self._qflag)
            return False
        self._var__exec_path = shutil.which('brew')
        return True

    def _parse_args(self, namespace):
        self._quiet = namespace.get('quiet', False)
        self._verbose = namespace.get('verbose', False)

    def _loc_exec(self):
        self._exec = {self._var__exec_path}
        del self._var__exec_path

    def _proc_logging(self, path):
        text = 'Listing installed {}'.format(self.desc[1])
        print_info(text, self._file, redirect=self._qflag)

        suffix = path.replace('/', ':')
        with tempfile.NamedTemporaryFile() as _temp_file:
            logfile = os.path.join(self._logroot, '{}-{}{}'.format(self.log, suffix, self.ext))
            argv = [path, 'bundle', 'dump', '--force', '--file={}'.format(_temp_file.name)]

            print_scpt(argv, self._file, redirect=self._qflag)
            script(argv, self._file, shell=True,
                   timeout=self._timeout, redirect=self._vflag)

            with open(_temp_file.name, 'r') as file:
                context = file.read()
            print_text(context, os.devnull, redirect=self._vflag)

        with open(logfile, 'w') as file:
            file.writelines(filter(lambda s: s.startswith('tap'), context.strip().splitlines(True)))
