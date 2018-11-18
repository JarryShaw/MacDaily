# -*- coding: utf-8 -*-

import os
import shutil
import sys
import traceback

from macdaily.cmd.logging import LoggingCommand
from macdaily.core.cask import CaskCommand
from macdaily.util.const import (bold, flash, purple_bg, red, red_bg, reset,
                                 under)
from macdaily.util.misc import (date, make_stderr, print_info, print_scpt,
                                print_term, print_text)

try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess


class CaskLogging(CaskCommand, LoggingCommand):

    @property
    def log(self):
        return 'Brewfile'

    @property
    def ext(self):
        return ''

    def _check_exec(self):
        stderr = make_stderr(self._vflag, sys.stderr)
        try:
            subprocess.check_call(['brew', 'command', 'bundle'], stdout=subprocess.DEVNULL, stderr=stderr)
        except subprocess.CalledProcessError:
            print_text(traceback.format_exc(), self._file, redirect=self._vflag)
            print('macdaily-{}: {}{}bundle{}: command not found'.format(self.cmd, red_bg, flash, reset), file=sys.stderr)
            text = ('macdaily-{}: {}bundle{}: you may find Bundler on '
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

    def _proc_logging(self, path):
        text = 'Listing installed {}'.format(self.desc[1])
        print_info(text, self._file, redirect=self._qflag)

        logfile = os.path.join(self._logroot, '{}-{}.{}'.format(self.log, path, self.ext))
        argv = [path, 'bundle', 'dump', '--force', '--file=-'.format()]
        args = ' '.join(argv)
        print_scpt(args, self._file, redirect=self._qflag)
        with open(self._file, 'a') as file:
            file.write('Script started on {}\n'.format(date()))
            file.write('command: {!r}\n'.format(args))

        stderr = make_stderr(self._vflag, sys.stderr)
        try:
            proc = subprocess.check_output(argv, stderr=stderr)
        except subprocess.SubprocessError:
            print_text(traceback.format_exc(), self._file, redirect=self._vflag)
        else:
            context = proc.decode()
            with open(logfile, 'w') as file:
                file.writelines(filter(lambda s: s.startswith('cask'), context.strip().splitlines(True)))
        finally:
            with open(self._file, 'a') as file:
                file.write('Script done on {}\n'.format(date()))
