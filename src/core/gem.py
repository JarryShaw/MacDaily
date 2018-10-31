# -*- coding: utf-8 -*-

import abc
import glob
import os
import shutil
import sys
import traceback

from macdaily.cls.command import Command
from macdaily.util.const import flash, purple_bg, red, red_bg, reset, under
from macdaily.util.misc import (date, print_info, print_scpt, print_term,
                                print_text)

try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess


class GemCommand(Command):

    @property
    def mode(self):
        return 'gem'

    @property
    def name(self):
        return 'RubyGems'

    @property
    def desc(self):
        return ('Ruby gem', 'Ruby gems')

    def _check_exec(self):
        self._var__exec_path = shutil.which('gem')
        flag = (self._var__exec_path is None)
        if flag:
            print(f'macdaily-update: {red_bg}{flash}gem{reset}: command not found', file=sys.stderr)
            text = (f'macdaily-update: {red}gem{reset}: you may download RubyGems from '
                    f'{purple_bg}{under}https://rubygems.org{reset}')
            print_term(text, self._file, redirect=self._qflag)
        return flag

    @abc.abstractmethod
    def _parse_args(self, namespace):
        super()._parse_args(namespace)
        self._brew = namespace.pop('brew', False)
        self._system = namespace.pop('system', False)

    def _loc_exec(self):
        if not (self._brew and self._system):
            self._exec = {self._var__exec_path}
        else:
            _exec_path = list()
            if self._brew:
                text = 'Looking for brewed Ruby'
                print_info(text, self._file, redirect=self._vflag)

                argv = ['brew', '--prefix']
                args = ' '.join(argv)
                print_scpt(args, self._file, redirect=self._vflag)
                with open(self._file, 'a') as file:
                    file.write(f'Script started on {date()}\n')
                    file.write(f'command: {args!r}\n')

                try:
                    proc = subprocess.check_output(argv, stderr=subprocess.DEVNULL)
                except subprocess.CalledProcessError:
                    print_text(traceback.format_exc(), self._file, redirect=self._vflag)
                else:
                    context = proc.decode()
                    print_text(context, self._file, redirect=self._vflag)

                    _glob_path = glob.glob(os.path.join(context.strip(), 'Cellar/ruby/*/bin/gem'))
                    _glob_path.sort(reverse=True)
                    _exec_path.append(_glob_path[0])
                finally:
                    with open(self._file, 'a') as file:
                        file.write(f'Script done on {date()}\n')
            if self._system and os.path.exists('/usr/bin/gem'):
                _exec_path.append('/usr/bin/gem')
            self._exec = set(_exec_path)
        del self._var__exec_path
