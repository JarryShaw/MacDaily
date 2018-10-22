# -*- coding: utf-8 -*-

import abc
import glob
import os
import shutil
import sys
import traceback

from macdaily.cls.command import Command
from macdaily.util.colour import (bold, flash, purple_bg, red, red_bg, reset,
                                  under, yellow)
from macdaily.util.misc import write
from macdaily.util.tool import script

try:
    import pathlib2 as pathlib
except ImportError:
    import pathlib

try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess


class BrewCommand(Command):

    @property
    def mode(self):
        return 'brew'

    @property
    def name(self):
        return 'Homebrew'

    @property
    def desc(self):
        return ('Homebrew formula', 'Homebrew formulae')

    def _check_exec(self):
        self.__exec_path = shutil.which('brew')
        flag = (self.__exec_path is None)
        if flag:
            print(f'macdaily-update: {red_bg}{flash}brew{reset}: command not found', file=sys.stderr)
            print(f'macdaily-update: {red}brew{reset}: you may find Homebrew on '
                  f'{purple_bg}{under}https://brew.sh{reset}, or install Homebrew through following command -- '
                  f'`{bold}/usr/bin/ruby -e "$(curl -fsSL '
                  f"""https://raw.githubusercontent.com/Homebrew/install/master/install)"{reset}'""")
        return flag

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
        script(['echo', f'|📝| {bold}{" ".join(args)}{reset}'], self._file)
        script(args, self._file)

    def _proc_cleanup(self):
        if self._no_cleanup:
            return

        args = ['brew', 'cleanup']
        if self._verbose:
            args.append('--verbose')
        if self._quiet:
            args.append('--quiet')
        argv = ' '.join(args)
        script(['echo', f'|📝| {bold}{argv}{reset}'], self._file)

        flag = os.path.isdir(self._disk_dir)
        for path in self._exec:
            logs = os.path.expanduser('~/Library/Logs/Homebrew/')
            if os.path.isdir(logs):
                args = [path, 'logs', 'cleanup']
                if self._verbose:
                    args.append('--verbose')
                if self._quiet:
                    args.append('--quiet')
                argv = ' '.join(args)
                script(['echo', f'|📝| {bold}{argv}{reset}'], self._file)

                args = ['rm', '-rf']
                if self._verbose:
                    args.append('-v')
                args.append(logs)
                argc = ' '.join(args)
                script(f'SUDO_ASKPASS={self._askpass} sudo --askpass --stdin --prompt="" {argc}',
                       self._file, shell=True)

            if not flag:
                continue
            try:
                proc = subprocess.check_output([path, '--cache'], stderr=subprocess.DEVNULL)
            except subprocess.CalledProcessError:
                write(self._file, traceback.format_exc())
                continue

            cache = proc.decode().strip()
            if os.path.isdir(cache):
                args = [path, 'caches', 'archive']
                if self._verbose:
                    args.append('--verbose')
                if self._quiet:
                    args.append('--quiet')
                argv = ' '.join(args)
                script(['echo', f'|📝| {bold}{argv}{reset}'], self._file)

                def _move(root, stem):
                    arch = os.path.join(self._disk_dir, stem)
                    pathlib.Path(arch).mkdir(parents=True, exist_ok=True)

                    file_list = list()
                    for name in os.listdir(root):
                        path = os.path.join(root, name)
                        if os.path.isdir(path) and name != 'Cask':
                            file_list.extend(_move(path, os.path.join(stem, name)))
                        elif os.path.splitext(name)[1] != '.incomplete' and path not in cask_list:
                            shutil.move(path, os.path.join(arch, name))
                            file_list.append(path)
                    return file_list

                cask_list = [os.path.realpath(name) for name in glob.glob(os.path.join(cache, 'Cask/*'))]
                file_list = _move(cache, 'Homebrew')
                if self._verbose:
                    script(['echo', '\n'.join(sorted(file_list))], self._file)

        if not flag:
            script(['echo', f'macdaily-update: {yellow}brew{reset}: '
                    f'archive directory {bold}{self._disk_dir}{reset} not found'], self._file)
