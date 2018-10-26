# -*- coding: utf-8 -*-

import abc
import shutil
import sys

from macdaily.cls.command import Command
from macdaily.util.const import (bold, flash, purple_bg, red, red_bg, reset,
                                 under)
from macdaily.util.misc import print_info, print_scpt, print_text, run, sudo


class NpmCommand(Command):

    @property
    def mode(self):
        return 'npm'

    @property
    def name(self):
        return 'Node.js Package Manager'

    @property
    def desc(self):
        return ('node module', 'node modules')

    def _check_exec(self):
        self.__exec_path = shutil.which('npm')
        flag = (self.__exec_path is None)
        if flag:
            print(f'macdaily-update: {red_bg}{flash}npm{reset}: command not found', file=sys.stderr)
            text = (f'macdaily-update: {red}npm{reset}: you may download Node.js from '
                    f'{purple_bg}{under}https://nodejs.org/{reset}')
            print_text(text, self._file, redirect=self._qflag)
        return flag

    @abc.abstractmethod
    def _parse_args(self, namespace):
        super()._parse_args(namespace)
        self._no_cleanup = namespace.pop('no_cleanup', False)
        self._quiet = namespace.pop('quiet', False)
        self._verbose = namespace.pop('verbose', False)

    def _loc_exec(self):
        self._exec = {self.__exec_path}
        del self.__exec_path

    def _proc_cleanup(self):
        if self._no_cleanup:
            return

        text = 'Pruning caches and archives'
        print_info(text, self._file, redirect=self._qflag)

        argv = ['npm', 'cleanup']
        if self._verbose:
            argv.append('--verbose')
        if self._quiet:
            argv.append('--quiet')
        print_scpt(' '.join(argv), self._file, redirect=self._qflag)

        def _cleanup(argv):
            if self._verbose:
                argv.append('--verbose')
            if self._quiet:
                argv.append('--quiet')
            args = ' '.join(argv)
            print_scpt(args, self._file, redirect=self._qflag)
            sudo(args, self._file, redirect=self._qflag, askpass=self._askpass)

        for path in self._exec:
            _cleanup([path, 'dedupe', '--global'])
            _cleanup([path, 'cache', 'clean', '--force'])
