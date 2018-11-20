# -*- coding: utf-8 -*-

import abc
import glob
import os
import shutil
import sys
import traceback

from macdaily.cls.command import Command
from macdaily.util.const import flash, purple_bg, red, red_bg, reset, under
from macdaily.util.misc import (date, make_stderr, print_info, print_scpt,
                                print_term, print_text)

try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess


class GemCommand(Command):

    @property
    def mode(self):
        return 'gem'

    @property
    def name(self):
        return 'RubyGems'

    @property
    def desc(self):
        return ('Ruby gem', 'Ruby gems')

    def _check_exec(self):
        self._var__exec_path = shutil.which('gem')
        flag = (self._var__exec_path is not None)
        if not flag:
            print(f'macdaily-{self.cmd}: {red_bg}{flash}gem{reset}: command not found', file=sys.stderr)
            text = (f'macdaily-{self.cmd}: {red}gem{reset}: you may download RubyGems from '
                    f'{purple_bg}{under}https://rubygems.org{reset}')
            print_term(text, self._file, redirect=self._qflag)
        return flag

    @abc.abstractmethod
    def _parse_args(self, namespace):
        super()._parse_args(namespace)
        self._brew = namespace.get('brew', False)
        self._system = namespace.get('system', False)

    def _loc_exec(self):
        if not (self._brew and self._system):
            self._exec = {self._var__exec_path}
        else:
            _exec_path = list()
            if self._brew:
                text = 'Looking for brewed Ruby'
                print_info(text, self._file, redirect=self._vflag)

                argv = ['brew', '--prefix']
                args = ' '.join(argv)
                print_scpt(args, self._file, redirect=self._vflag)
                with open(self._file, 'a') as file:
                    file.write(f'Script started on {date()}\n')
                    file.write(f'command: {args!r}\n')

                try:
                    proc = subprocess.check_output(argv, stderr=make_stderr(self._vflag))
                except subprocess.CalledProcessError:
                    print_text(traceback.format_exc(), self._file, redirect=self._vflag)
                else:
                    context = proc.decode()
                    print_text(context, self._file, redirect=self._vflag)

                    _glob_path = glob.glob(os.path.join(context.strip(), 'Cellar/ruby/*/bin/gem'))
                    _glob_path.sort(reverse=True)
                    _exec_path.append(_glob_path[0])
                finally:
                    with open(self._file, 'a') as file:
                        file.write(f'Script done on {date()}\n')
            if self._system:
                text = 'Looking for macOS-provided Ruby'
                print_info(text, self._file, redirect=self._vflag)
                if os.path.exists('/usr/bin/gem'):
                    _exec_path.append('/usr/bin/gem')
                else:
                    _exec_path.extend(glob.glob('/System/Library/Frameworks/Ruby.framework/Versions/Current/usr/bin/gem'))  # noqa
            self._exec = set(_exec_path)
        del self._var__exec_path

    def _check_pkgs(self, path):
        text = f'Listing installed {self.desc[1]}'
        print_info(text, self._file, redirect=self._vflag)

        argv = [path, 'list', '--no-versions']
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
            print_text(context, self._file, redirect=self._vflag)

            _temp_pkgs = list()
            for package in filter(None, context.strip().splitlines()):
                if package.startswith('***'):
                    continue
                _temp_pkgs.append(package)
            _real_pkgs = set(_temp_pkgs)
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
