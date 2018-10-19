# -*- coding: utf-8 -*-

import shutil
import sys

from macdaily.cls.command import Command
from macdaily.util.colour import blush, bold, flash, red, reset


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
        self.__exec_path = shutil.which('softwareupdate')
        flag = (self.__exec_path is None)
        if flag:
            print(f'macdaily-update: {blush}{flash}system{reset}: command not found', file=sys.stderr)
            print(f'macdaily-update: {red}system{reset}: '
                  "you may add `softwareupdate' to PATH through the following command -- "
                  f'''`{bold}echo 'export PATH="/usr/sbin:$PATH"' >> ~/.bash_profile{reset}'\n''')
        return flag

    def _loc_exec(self):
        self._exec = {self.__exec_path}
        del self.__exec_path
