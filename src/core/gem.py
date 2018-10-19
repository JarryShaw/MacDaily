# -*- coding: utf-8 -*-

import abc
import glob
import os
import shutil
import sys

from macdaily.cls.command import Command
from macdaily.util.colour import blush, flash, purple, red, reset, under

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
        self.__exec_path = shutil.which('gem')
        flag = (self.__exec_path is None)
        if flag:
            print(f'update: {blush}{flash}gem{reset}: command not found\n', file=sys.stderr)
            print(f'update: {red}gem{reset}: you may download RubyGems from '
                  f'{purple}{under}https://rubygems.org{reset}\n')
        return flag

    @abc.abstractmethod
    def _parse_args(self, namespace):
        super()._parse_args(namespace)
        self._brew = namespace.pop('brew', False)
        self._system = namespace.pop('system', False)

    def _loc_exec(self):
        if not (self._brew and self._system):
            self._exec = {self.__exec_path}
        else:
            _exec_path = list()
            if self._brew:
                try:
                    proc = subprocess.check_output(['brew', '--prefix'], stderr=subprocess.DEVNULL)
                except subprocess.CalledProcessError:
                    prefix = '/usr/local'
                else:
                    prefix = proc.decode().strip()

                _glob_path = glob.glob(os.path.join(prefix, 'Cellar/ruby/*/bin/gem'))
                _glob_path.sort(reverse=True)
                _exec_path.append(_glob_path[0])
            if self._system and os.path.exists('/usr/bin/gem'):
                _exec_path.append('/usr/bin/gem')
            self._exec = set(_exec_path)
        del self.__exec_path
