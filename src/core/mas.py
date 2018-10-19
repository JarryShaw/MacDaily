# -*- coding: utf-8 -*-

import shutil
import sys

from macdaily.cls.command import Command
from macdaily.util.colour import blush, bold, flash, red, reset


class MasCommand(Command):

    @property
    def mode(self):
        return 'mas'

    @property
    def name(self):
        return 'Mac App Store CLI'

    @property
    def desc(self):
        return ('macOS application', 'macOS applications')

    def _check_exec(self):
        self.__exec_path = shutil.which('mas')
        flag = (self.__exec_path is None)
        if flag:
            print(f'macdaily-update: {blush}{flash}mas{reset}: command not found', file=sys.stderr)
            print(f'macdaily-update: {red}mas{reset}: you may download MAS through following command -- '
                  f"`{bold}brew install mas{reset}'\n")
        return flag

    def _loc_exec(self):
        self._exec = {self.__exec_path}
        del self.__exec_path
