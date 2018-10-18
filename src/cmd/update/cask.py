# -*- coding: utf-8 -*-

import glob
import os
import shutil
import sys
import textwrap
import time
import traceback

from macdaily.cmd.update.command import UpdateCommand
from macdaily.util.colours import (blush, bold, flash, length, purple, red,
                                   reset, under, yellow)
from macdaily.util.tools import script

try:
    import pathlib2 as pathlib
except ImportError:
    import pathlib

try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess


class CaskUpdate(UpdateCommand):

    @property
    def mode(self):
        return 'cask'

    @property
    def name(self):
        return 'Caskroom'

    @property
    def desc(self):
        return ('Homebrew Cask', 'Homebrew Casks')

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

    def _parse_args(self, namespace):
        self._all = namespace.pop('all', False)
        self._cleanup = namespace.pop('cleanup', True)
        self._exhaust = namespace.pop('exhaust', False)
        self._force = namespace.pop('force', False)
        self._greedy = namespace.pop('greedy', False)
        self._merge = namespace.pop('merge', False)
        self._quiet = namespace.pop('quiet', False)
        self._show_log = namespace.pop('show_log', False)
        self._verbose = namespace.pop('verbose', False)

        self._logging_opts = namespace.pop('logging', str()).split()
        self._update_opts = namespace.pop('update', str()).split()

    def _loc_exec(self):
        self._exec = {self.__exec_path}
        del self.__exec_path

    def _check_pkgs(self, path):
        args = [path, 'cask', 'list']
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

        if self._exhaust:
            return self._exhaust_check(path)

        args = [path, 'cask', 'outdated']
        if self._quiet:
            args.append('--quiet')
        if self._verbose:
            args.append('--verbose')
        if self._greedy:
            args.append('--greedy')
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
            self.__temp_pkgs = set(context.split())
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

    def _exhaust_check(self, path):
        args = ['brew', 'cask', 'outdated', '--exhaust']
        if self._quiet:
            args.append('--quiet')
        if self._verbose:
            args.append('--verbose')
        args.extend(self._logging_opts)
        self._log.write(f'+ {" ".join(args)}\n')

        args = [path, 'cask', 'list']
        if self._verbose:
            self._log.write(f'++ {" ".join(args)}')
        try:
            proc = subprocess.check_output(args, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            self._log.write(traceback.format_exc())
            _list_pkgs = set()
        else:
            context = proc.decode()
            if self._verbose:
                self._log.write(context)
            _list_pkgs = set(context.split())

        args = [path, '--prefix']
        if self._verbose:
            self._log.write(f'++ {" ".join(args)}')
        try:
            proc = subprocess.check_output(args, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            self._log.write(traceback.format_exc())
            self.__temp_pkgs = set()
            return
        else:
            context = proc.decode()
            if self._verbose:
                self._log.write(context)
            prefix = context.strip()

        _temp_pkgs = list()
        for cask in _list_pkgs:
            args = [path, 'cask', 'info', cask]
            if self._verbose:
                self._log.write(f'++ {" ".join(args)}')
            try:
                proc = subprocess.check_output(args, stderr=subprocess.DEVNULL)
            except subprocess.CalledProcessError:
                self._log.write(traceback.format_exc())
                continue

            context = proc.decode()
            if self._verbose:
                self._log.write(context)
            version = context.split(maxsplit=2)[1]

            installed = os.path.join(prefix, 'Caskroom', cask, version)
            if os.path.isdir(installed):
                _temp_pkgs.append(cask)

        self.__temp_pkgs = set(_temp_pkgs)
        if self._verbose:
            self._log.write(f'++ {path} cask outdated list\n')
        max_len = len(max(_temp_pkgs, key=lambda s: len(s)))
        context = '\n'.join(textwrap.wrap('    '.join(map(lambda s: s.ljust(max_len), self.__temp_pkgs)), length))
        self._log.write(f'{context}\n')

    def _proc_update(self, path):
        args = [path, 'cask', 'upgrade']
        if self._quiet:
            args.append('--quiet')
        if self._verbose:
            args.append('--verbose')
        if self._greedy:
            args.append('--greedy')
        if self._exhaust:
            args.append('--exhaust')
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
        if self._cleanup():
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
                    shutil.move(link, os.path.join(self._disk_dir, 'Homebrew', 'Cask'))
                for cask in filter(lambda p: os.path.splitext(cask)[1] != '.incomplete', cask_list):
                    file_list.append(cask)
                    shutil.move(cask, os.path.join(self._disk_dir, 'Homebrew', 'download'))
                if self._verbose:
                    script(['echo', '-e', '\n'.join(sorted(file_list))], self._log.name)
