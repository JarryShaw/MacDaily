# -*- coding: utf-8 -*-

import abc
import glob
import os
import shutil
import sys
import traceback

from macdaily.cls.command import Command
from macdaily.util.colour import (blush, bold, flash, purple, red, reset,
                                  under, yellow)
from macdaily.util.tool import script

try:
    import pathlib2 as pathlib
except ImportError:
    import pathlib

try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess


class CaskCommand(Command):

    @property
    def mode(self):
        return 'cask'

    @property
    def name(self):
        return 'Homebrew Casks'

    @property
    def desc(self):
        return ('Caskroom binary', 'Caskroom binaries')

    def _check_exec(self):
        try:
            subprocess.check_call(['brew', 'command', 'cask'])
        except subprocess.CalledProcessError:
            print(f'update: {blush}{flash}cask{reset}: command not found', file=sys.stderr)
            print(f'update: {red}cask{reset}: you may find Caskroom on '
                  f'{purple}{under}https://caskroom.github.io{reset}, '
                  f'or install Caskroom through following command -- '
                  f"`{bold}brew tap homebrew/cask{reset}'\n")
            return True
        self.__exec_path = shutil.which('brew')
        return False

    @abc.abstractmethod
    def _parse_args(self, namespace):
        super()._parse_args(namespace)
        self._force = namespace.pop('force', False)
        self._merge = namespace.pop('merge', False)
        self._no_cleanup = namespace.pop('no_cleanup', False)
        self._verbose = namespace.pop('verbose', False)

    def _loc_exec(self):
        self._exec = {self.__exec_path}
        del self.__exec_path

    def _proc_renew(self, path):
        args = [path, 'update']
        if self._force:
            args.append('--force')
        if self._merge:
            args.append('--merge')
        if self._quiet:
            args.append('--quiet')
        if self._verbose:
            args.append('--verbose')
        script(['echo', '-e', f'\n+ {bold}{" ".join(args)}{reset}'], self._log.name)
        script(args, self._log.name)

    def _proc_cleanup(self):
        if self._no_cleanup:
            return

        if not os.path.isdir(self._disk_dir):
            return script(['echo', '-e', f'macdaily-update: {yellow}cask{reset}: '
                           f'archive directory {bold}{self._disk_dir}{reset} not found'], self._log.name)

        args = ['brew', 'cask', 'cleanup']
        if self._verbose:
            args.append('--verbose')
        if self._quiet:
            args.append('--quiet')
        argv = ' '.join(args)
        script(['echo', '-e', f'\n+ {bold}{argv}{reset}'], self._log.name)

        path_cask = os.path.join(self._disk_dir, 'Homebrew', 'Cask')
        path_down = os.path.join(self._disk_dir, 'Homebrew', 'download')

        pathlib.Path(path_cask).mkdir(parents=True, exist_ok=True)
        pathlib.Path(path_down).mkdir(parents=True, exist_ok=True)

        for path in self._exec:
            try:
                proc = subprocess.check_output([path, '--cache'], stderr=subprocess.DEVNULL)
            except subprocess.CalledProcessError:
                self._log.write(traceback.format_exc())
                continue

            cache = proc.decode().strip()
            if os.path.isdir(cache):
                args = [path, 'cask', 'caches', 'archive']
                if self._verbose:
                    args.append('--verbose')
                if self._quiet:
                    args.append('--quiet')
                argv = ' '.join(args)
                script(['echo', '-e', f'++ {bold}{argv}{reset}'], self._log.name)

                file_list = list()
                link_list = glob.glob(os.path.join(cache, 'Cask/*'))
                cask_list = [os.path.realpath(name) for name in link_list]
                for link in link_list:
                    file_list.append(link)
                    shutil.move(link, path_cask)
                for cask in filter(lambda p: os.path.splitext(cask)[1] != '.incomplete', cask_list):
                    file_list.append(cask)
                    shutil.move(cask, path_down)
                if self._verbose:
                    script(['echo', '-e', '\n'.join(sorted(file_list))], self._log.name)
