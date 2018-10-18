# -*- coding: utf-8 -*-

import glob
import os
import shutil
import sys
import time
import traceback

from macdaily.cmd.update.command import UpdateCommand
from macdaily.util.colours import (blush, bold, flash, purple, red, reset,
                                   under, yellow)
from macdaily.util.tools import script

try:
    import pathlib2 as pathlib
except ImportError:
    import pathlib

try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess


class BrewUpdate(UpdateCommand):

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
            print(f'macdaily-update: {blush}{flash}brew{reset}: command not found', file=sys.stderr)
            print(f'macdaily-update: {red}brew{reset}: you may find Homebrew on {purple}{under}https://brew.sh{reset}, '
                  f'or install Homebrew through following command -- `{bold}/usr/bin/ruby -e '
                  f'"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"{reset}`\n')
        return flag

    def _parse_args(self, namespace):
        self._all = namespace.pop('all', False)
        self._no_cleanup = namespace.pop('no_cleanup', False)
        self._force = namespace.pop('force', False)
        self._merge = namespace.pop('merge', False)
        self._quiet = namespace.pop('quiet', False)
        self._show_log = namespace.pop('show_log', False)
        self._verbose = namespace.pop('verbose', False)
        self._yes = namespace.pop('yes', False)

        self._logging_opts = namespace.pop('logging', str()).split()
        self._update_opts = namespace.pop('update', str()).split()

    def _loc_exec(self):
        self._exec = {self.__exec_path}
        del self.__exec_path

    def _check_pkgs(self, path):
        args = [path, 'list']
        try:
            proc = subprocess.check_output(args, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            _real_pkgs = set()
        else:
            _real_pkgs = set(proc.decode().split())

        _temp_pkgs = list()
        _lost_pkgs = list()
        for package in self._packages:
            if package in _real_pkgs:
                _temp_pkgs.append(package)
            else:
                _lost_pkgs.append(package)
        self._lost.extend(_lost_pkgs)

        self.__real_pkgs = set(_real_pkgs)
        self.__lost_pkgs = set(_lost_pkgs)
        self.__temp_pkgs = set(_temp_pkgs)

    def _check_list(self, path):
        if (self._brew_renew is None or
                time.time() - self._brew_renew >= 300):
            self._proc_renew(path)
            self._brew_renew = time.time()

        args = [path, 'outdated']
        if self._quiet:
            args.append('--quiet')
        if self._verbose:
            args.append('--verbose')
        args.extend(self._logging_opts)

        self._log.write(f'+ {" ".join(args)}\n')
        try:
            proc = subprocess.check_output(args, stderr=subprocess.DEVNULL)
        except subprocess.SubprocessError:
            self._log.write(traceback.format_exc())
            self.__temp_pkgs = set()
        else:
            context = proc.decode()
            self._log.write(context)

            _temp_pkgs = list()
            for line in context.strip().split('\n'):
                _temp_pkgs.append(line.split(maxsplit=1)[0])
            self.__temp_pkgs = set(_temp_pkgs)
        finally:
            self._log.write('\n')

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

    def _proc_update(self, path):
        args = [path, 'upgrade']
        if self._quiet:
            args.append('--quiet')
        if self._verbose:
            args.append('--verbose')
        args.extend(self._update_opts)

        args.append('')
        for package in self.__temp_pkgs:
            args[-1] = package
            argv = ' '.join(args)
            script(['echo', '-e', f'\n+ {bold}{argv}{reset}'], self._log.name)
            if script(args, self._log.name, timeout=self._timeout):
                self._fail.append(package)
            else:
                self._pkgs.append(package)
            self._log.write('\n')
        del self.__temp_pkgs

    def _proc_cleanup(self):
        if self._no_cleanup:
            return

        args = ['brew', 'cleanup']
        if self._verbose:
            args.append('--verbose')
        if self._quiet:
            args.append('--quiet')
        argv = ' '.join(args)
        script(['echo', '-e', f'\n+ {bold}{argv}{reset}'], self._log.name)

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
                script(['echo', '-e', f'++ {bold}{argv}{reset}'], self._log.name)

                args = ['rm', '-rf']
                if self._verbose:
                    args.append('-v')
                args.append(logs)
                argc = ' '.join(args)
                script(f'yes {self._password} | sudo --stdin --prompt="" {argc}', self._log.name, shell=True)

            if not flag:
                continue
            try:
                proc = subprocess.check_output([path, '--cache'], stderr=subprocess.DEVNULL)
            except subprocess.CalledProcessError:
                self._log.write(traceback.format_exc())
                continue

            cache = proc.decode().strip()
            if os.path.isdir(cache):
                args = [path, 'caches', 'archive']
                if self._verbose:
                    args.append('--verbose')
                if self._quiet:
                    args.append('--quiet')
                argv = ' '.join(args)
                script(['echo', '-e', f'++ {bold}{argv}{reset}'], self._log.name)

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
                    script(['echo', '-e', '\n'.join(sorted(file_list))], self._log.name)

        if not flag:
            script(['echo', '-e', f'macdaily-update: {yellow}brew{reset}: '
                    f'archive directory {bold}{self._disk_dir}{reset} not found'], self._log.name)
