# -*- coding: utf-8 -*-

import abc
import contextlib
import glob
import os
import re
import shutil
import sys
import traceback

from macdaily.cls.command import Command
from macdaily.util.const import (bold, flash, green, purple_bg, red, red_bg,
                                 reset, under, yellow)
from macdaily.util.misc import (date, get_input, make_stderr, print_info,
                                print_scpt, print_term, print_text, run, sudo)

if sys.version_info[:2] == (3, 4):
    import pathlib2 as pathlib
    import subprocess32 as subprocess
else:
    import pathlib
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
        self._var__exec_path = shutil.which('brew')
        flag = (self._var__exec_path is not None)
        if not flag:
            print(f'macdaily-{self.cmd}: {red_bg}{flash}brew{reset}: command not found', file=sys.stderr)
            text = (f'macdaily-{self.cmd}: {red}brew{reset}: you may find Homebrew on '
                    f'{purple_bg}{under}https://brew.sh{reset}, or install Homebrew through following command -- '
                    f'`{bold}/usr/bin/ruby -e "$(curl -fsSL '
                    f"""https://raw.githubusercontent.com/Homebrew/install/master/install)"{reset}'""")
            print_term(text, self._file, redirect=self._qflag)
        return flag

    @abc.abstractmethod
    def _parse_args(self, namespace):
        super()._parse_args(namespace)
        self._force = namespace.get('force', False)
        self._merge = namespace.get('merge', False)
        self._no_cleanup = namespace.get('no_cleanup', False)
        self._verbose = namespace.get('verbose', False)

    def _loc_exec(self):
        self._exec = {self._var__exec_path}
        del self._var__exec_path

    def _check_pkgs(self, path):
        text = f'Listing installed {self.desc[1]}'
        print_info(text, self._file, redirect=self._vflag)

        argv = [path, 'list']
        args = ' '.join(argv)
        print_scpt(args, self._file, redirect=self._vflag)
        with open(self._file, 'a') as file:
            file.write(f'Script started on {date()}\n')
            file.write(f'command: {args!r}\n')

        try:
            proc = subprocess.check_output(argv, stderr=make_stderr(self._vflag))
        except subprocess.CalledProcessError:
            print_text(traceback.format_exc(), self._file, redirect=self._vflag)
            _real_pkgs = set()
        else:
            context = proc.decode()
            _real_pkgs = set(context.split())
            print_text(context, self._file, redirect=self._vflag)
        finally:
            with open(self._file, 'a') as file:
                file.write(f'Script done on {date()}\n')

        text = 'Checking existence of specified packages'
        print_info(text, self._file, redirect=self._vflag)

        _temp_pkgs = list()
        _lost_pkgs = list()
        for package in self._packages:
            if package in _real_pkgs:
                _temp_pkgs.append(package)
            else:
                _lost_pkgs.append(package)
        self._lost.extend(_lost_pkgs)

        self._var__real_pkgs = set(_real_pkgs)
        self._var__lost_pkgs = set(_lost_pkgs)
        self._var__temp_pkgs = set(_temp_pkgs)

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

    def _proc_fixmissing(self, path):
        text = f'Checking broken {self.desc[0]} dependencies'
        print_info(text, self._file, redirect=self._qflag)

        def _proc_check():
            argv = [path, 'missing', f'--hide={",".join(self._ignore)!r}']
            args = ' '.join(argv)
            print_scpt(args, self._file, redirect=self._vflag)
            with open(self._file, 'a') as file:
                file.write(f'Script started on {date()}\n')
                file.write(f'command: {args!r}\n')

            _deps_pkgs = list()
            try:  # brew missing exits with a non-zero status if any formulae are missing dependencies
                proc = subprocess.run(argv, stdout=subprocess.PIPE, stderr=make_stderr(self._vflag))
            except subprocess.SubprocessError:
                print_text(traceback.format_exc(), self._file, redirect=self._vflag)
            else:
                context = proc.stdout.decode()
                print_text(context, self._file, redirect=self._vflag)

                for line in filter(None, context.strip().splitlines()):
                    _deps_pkgs.extend(line.split()[1:])
            finally:
                with open(self._file, 'a') as file:
                    file.write(f'Script done on {date()}\n')
            return set(_deps_pkgs)

        def _proc_confirm():
            pkgs = f'{reset}, {bold}'.join(_deps_pkgs)
            text = f'macdaily-{self.cmd}: {yellow}brew{reset}: found broken dependencies: {bold}{pkgs}{reset}'
            print_term(text, self._file, redirect=self._qflag)
            if self._yes or self._quiet:
                return True
            while True:
                ans = get_input(self._confirm, 'Would you like to reinstall?',
                                prefix=f'Found broken dependencies: {", ".join(_deps_pkgs)}.\n\n',
                                suffix=f' ({green}y{reset}/{red}N{reset}) ')
                if re.match(r'[yY]', ans):
                    return True
                elif re.match(r'[nN]', ans):
                    return False
                else:
                    print('Invalid input.', file=sys.stderr)

        _deps_pkgs = _proc_check() - self._ignore
        if not _deps_pkgs:
            text = f'macdaily-{self.cmd}: {green}brew{reset}: no broken dependencies'
            print_term(text, self._file, redirect=self._qflag)
            return

        text = f'Fixing broken {self.desc[0]} dependencies'
        print_info(text, self._file, redirect=self._qflag)

        if _proc_confirm():
            argv = [path, 'reinstall']
            if self._quiet:
                argv.append('--quiet')
            if self._verbose:
                argv.append('--verbose')
            argv.append('')

            _done_pkgs = set()
            while _deps_pkgs:
                for package in _deps_pkgs:
                    argv[-1] = package
                    print_scpt(' '.join(argv), self._file, redirect=self._qflag)
                    if not run(argv, self._file, redirect=self._qflag,
                               timeout=self._timeout, verbose=self._vflag):
                        with contextlib.suppress(ValueError):
                            self._pkgs.remove(package)
                _done_pkgs |= _deps_pkgs
                _deps_pkgs = _proc_check() - _done_pkgs - self._ignore

            text = f'macdaily-{self.cmd}: {green}brew{reset}: all broken dependencies fixed'
        else:
            text = f'macdaily-{self.cmd}: {red}brew{reset}: all broken dependencies remain'
        print_term(text, self._file, redirect=self._qflag)

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
                sudo(argv, self._file, self._password,
                     redirect=self._qflag, verbose=self._vflag)

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
                proc = subprocess.check_output(argv, stderr=make_stderr(self._vflag))
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
                        if os.path.isdir(path):
                            if name != 'Cask':
                                file_list.extend(_move(path, os.path.join(stem, name)))
                        elif os.path.splitext(name)[1] != '.incomplete' and path not in cask_list:
                            try:
                                shutil.move(path, os.path.join(arch, name))
                            except (shutil.Error, FileExistsError):
                                os.remove(path)
                            # with contextlib.suppress(shutil.Error, FileExistsError):
                            #     shutil.move(path, os.path.join(arch, name))
                            file_list.append(path)
                    return file_list

                cask_list = [os.path.realpath(name) for name in glob.glob(os.path.join(cache, 'Cask/*'))]
                file_list = _move(cache, 'Homebrew')
                print_text(os.linesep.join(sorted(file_list)), self._file, redirect=self._vflag)

        if flag:
            text = (f'macdaily-{self.cmd}: {yellow}brew{reset}: '
                    f'archive directory {bold}{self._disk_dir}{reset} not found')
            print_term(text, self._file, redirect=self._vflag)
