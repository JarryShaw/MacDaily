# -*- coding: utf-8 -*-

import abc
import glob
import os
import shutil
import sys
import traceback

from macdaily.cls.command import Command
from macdaily.util.const import (bold, flash, purple_bg, red, red_bg, reset,
                                 under, yellow)
from macdaily.util.misc import (date, print_info, print_scpt, print_text, run,
                                sudo)

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
        self._tmp_exec_path = shutil.which('brew')
        flag = (self._tmp_exec_path is None)
        if flag:
            print(f'macdaily-update: {red_bg}{flash}brew{reset}: command not found', file=sys.stderr)
            text = (f'macdaily-update: {red}brew{reset}: you may find Homebrew on '
                    f'{purple_bg}{under}https://brew.sh{reset}, or install Homebrew through following command -- '
                    f'`{bold}/usr/bin/ruby -e "$(curl -fsSL '
                    f"""https://raw.githubusercontent.com/Homebrew/install/master/install)"{reset}'""")
            print_text(text, self._file, redirect=self._qflag)
        return flag

    @abc.abstractmethod
    def _parse_args(self, namespace):
        super()._parse_args(namespace)
        self._force = namespace.pop('force', False)
        self._merge = namespace.pop('merge', False)
        self._no_cleanup = namespace.pop('no_cleanup', False)
        self._verbose = namespace.pop('verbose', False)

    def _loc_exec(self):
        self._exec = {self._tmp_exec_path}
        del self._tmp_exec_path

    def _proc_renew(self, path):
        text = 'Updating Homebrew database'
        print_info(text, self._file, redirect=self._qflag)

        argv = [path, 'update']
        if self._force:
            argv.append('--force')
        if self._merge:
            argv.append('--merge')
        if self._quiet:
            argv.append('--quiet')
        if self._verbose:
            argv.append('--verbose')
        print_scpt(' '.join(argv), self._file, redirect=self._qflag)
        run(argv, self._file, redirect=self._qflag)

    def _proc_cleanup(self):
        if self._no_cleanup:
            return

        text = 'Pruning caches and archives'
        print_info(text, self._file, redirect=self._qflag)

        argv = ['brew', 'cleanup']
        if self._verbose:
            argv.append('--verbose')
        if self._quiet:
            argv.append('--quiet')
        args = ' '.join(argv)
        print_scpt(args, self._file, redirect=self._qflag)

        flag = (not os.path.isdir(self._disk_dir))
        for path in self._exec:
            logs = os.path.expanduser('~/Library/Logs/Homebrew/')
            if os.path.isdir(logs):
                argv = [path, 'logs', 'cleanup']
                if self._verbose:
                    argv.append('--verbose')
                if self._quiet:
                    argv.append('--quiet')
                args = ' '.join(argv)
                print_scpt(args, self._file, redirect=self._vflag)

                argv = ['rm', '-rf']
                if self._verbose:
                    argv.append('-v')
                argv.append(logs)
                sudo(argv, self._file, askpass=self._askpass, redirect=self._qflag)

            # if external disk not attached
            if flag:
                continue

            argv = [path, '--cache']
            args = ' '.join(argv)
            print_scpt(args, self._file, redirect=self._vflag)
            with open(self._file, 'a') as file:
                file.write(f'Script started on {date()}\n')
                file.write(f'command: {args!r}\n')

            fail = False
            try:
                proc = subprocess.check_output(argv, stderr=subprocess.DEVNULL)
            except subprocess.CalledProcessError:
                print_text(traceback.format_exc(), self._file, redirect=self._vflag)
                fail = True
            else:
                context = proc.decode()
                print_text(context, self._file, redirect=self._vflag)
            finally:
                with open(self._file, 'a') as file:
                    file.write(f'Script done on {date()}\n')
            if fail:
                continue

            cache = context.strip()
            if os.path.isdir(cache):
                argv = [path, 'caches', 'archive']
                if self._verbose:
                    argv.append('--verbose')
                if self._quiet:
                    argv.append('--quiet')
                args = ' '.join(argv)
                print_scpt(args, self._file, redirect=self._qflag)

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
                print_text(os.linesep.join(sorted(file_list)), self._file, redirect=self._vflag)

        if flag:
            text = (f'macdaily-update: {yellow}brew{reset}: '
                    f'archive directory {bold}{self._disk_dir}{reset} not found')
            print_text(text, self._file, redirect=self._vflag)
