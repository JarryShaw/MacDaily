# -*- coding: utf-8 -*-

import shutil
import sys

from macdaily.cls.command import Command
from macdaily.util.const import bold, flash, red, red_bg, reset
from macdaily.util.misc import print_text


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
        self._tmp_exec_path = shutil.which('softwareupdate')
        flag = (self._tmp_exec_path is None)
        if flag:
            print(f'macdaily-update: {red_bg}{flash}system{reset}: command not found', file=sys.stderr)
            text = (f'macdaily-update: {red}system{reset}: '
                    "you may add `softwareupdate' to PATH through the following command -- "
                    f"""`{bold}echo 'export PATH="/usr/sbin:$PATH"' >> ~/.bash_profile{reset}'""")
            print_text(text, self._file, redirect=self._qflag)
        return flag

    def _loc_exec(self):
        self._exec = {self._tmp_exec_path}
        del self._tmp_exec_path
