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
from macdaily.util.misc import (date, print_info, print_scpt, print_term,
                                print_text, run)

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
            print_text(traceback.format_exc(), self._file, redirect=self._vflag)
            print('macdaily-update: {}{}cask{}: command not found'.format(red_bg, flash, reset), file=sys.stderr)
            text = ('macdaily-update: {}cask{}: you may find Caskroom on '
                    '{}{}https://caskroom.github.io{}, '
                    'or install Caskroom through following command -- '
                    "`{}brew tap homebrew/cask{}'".format(red, reset, purple_bg, under, reset, bold, reset))
            print_term(text, self._file, redirect=self._qflag)
            return True
        self._var__exec_path = shutil.which('brew')
        return False

    @abc.abstractmethod
    def _parse_args(self, namespace):
        super()._parse_args(namespace)
        self._force = namespace.pop('force', False)
        self._merge = namespace.pop('merge', False)
        self._no_cleanup = namespace.pop('no_cleanup', False)
        self._verbose = namespace.pop('verbose', False)

    def _loc_exec(self):
        self._exec = {self._var__exec_path}
        del self._var__exec_path

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

        if not os.path.isdir(self._disk_dir):
            text = ('macdaily-update: {}cask{}: '
                    'archive directory {}{}{} not found'.format(yellow, reset, bold, self._disk_dir, reset))
            return print_term(text, self._file, redirect=self._vflag)

        argv = ['brew', 'cask', 'cleanup']
        if self._verbose:
            argv.append('--verbose')
        if self._quiet:
            argv.append('--quiet')
        print_scpt(' '.join(argv), self._file, redirect=self._qflag)

        path_cask = os.path.join(self._disk_dir, 'Homebrew', 'Cask')
        path_down = os.path.join(self._disk_dir, 'Homebrew', 'download')

        pathlib.Path(path_cask).mkdir(parents=True, exist_ok=True)
        pathlib.Path(path_down).mkdir(parents=True, exist_ok=True)

        for path in self._exec:
            argv = [path, '--cache']
            args = ' '.join(argv)
            print_scpt(args, self._file, redirect=self._vflag)
            with open(self._file, 'a') as file:
                file.write('Script started on {}\n'.format(date()))
                file.write('command: {!r}\n'.format(args))

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
                    file.write('Script done on {}\n'.format(date()))
            if fail:
                continue

            cache = context.strip()
            if os.path.isdir(cache):
                argv = [path, 'cask', 'caches', 'archive']
                if self._verbose:
                    argv.append('--verbose')
                if self._quiet:
                    argv.append('--quiet')
                print_scpt(' '.join(argv), self._file, redirect=self._qflag)

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
                    print_text(os.linesep.join(sorted(file_list)), self._file, redirect=self._vflag)
