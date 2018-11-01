# -*- coding: utf-8 -*-

import shutil
import sys

from macdaily.cls.command import Command
from macdaily.util.const import bold, flash, red, red_bg, reset
from macdaily.util.misc import print_term


class SystemCommand(Command):

    @property
    def mode(self):
        return 'system'

    @property
    def name(self):
        return 'macOS Software Update'

    @property
    def desc(self):
        return ('system software', 'system software')

    def _check_exec(self):
        self._var__exec_path = shutil.which('softwareupdate')
        flag = (self._var__exec_path is None)
        if flag:
            print('macdaily-update: {}{}system{}: command not found'.format(red_bg, flash, reset), file=sys.stderr)
            text = ('macdaily-update: {}system{}: '
                    "you may add `softwareupdate' to PATH through the following command -- "
                    """`{}echo 'export PATH="/usr/sbin:$PATH"' >> ~/.bash_profile{}'""".format(red, reset, bold, reset))
            print_term(text, self._file, redirect=self._qflag)
        return flag

    def _loc_exec(self):
        self._exec = {self._var__exec_path}
        del self._var__exec_path
