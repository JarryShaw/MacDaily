# -*- coding: utf-8 -*-

import collections
import os
import re
import sys
import traceback

from macdaily.cmd.logging import LoggingCommand
from macdaily.core.gem import GemCommand
from macdaily.util.misc import (date, make_stderr, print_info, print_scpt,
                                print_text)

if sys.version_info[:2] == (3, 4):
    import subprocess32 as subprocess
else:
    import subprocess


class GemLogging(GemCommand, LoggingCommand):

    @property
    def log(self):
        return 'lockdown'

    @property
    def ext(self):
        return '.rb'

    def _parse_args(self, namespace):
        self._brew = namespace.get('brew', False)
        self._system = namespace.get('system', False)

        self._quiet = namespace.get('quiet', False)
        self._verbose = namespace.get('verbose', False)

    def _proc_logging(self, path):
        text = f'Listing installed {self.desc[1]}'
        print_info(text, self._file, redirect=self._qflag)

        argv = [path, 'list']
        args = ' '.join(argv)
        print_scpt(args, self._file, redirect=self._qflag)
        with open(self._file, 'a') as file:
            file.write(f'Script started on {date()}\n')
            file.write(f'command: {args!r}\n')

        try:
            proc = subprocess.check_output(argv, stderr=make_stderr(self._vflag))
        except subprocess.CalledProcessError:
            print_text(traceback.format_exc(), self._file, redirect=self._vflag)
            _real_pkgs = dict()
        else:
            context = proc.decode()
            print_text(context, self._file, redirect=self._vflag)
            _real_pkgs = collections.defaultdict(list)
            for line in filter(None, context.strip().splitlines()):
                if line.startswith('***'):
                    continue
                package, versions = line.split(maxsplit=1)
                _real_pkgs[package].extend(re.findall(r'\d+\.\d+\.\d+', versions))
        finally:
            with open(self._file, 'a') as file:
                file.write(f'Script done on {date()}\n')

        _temp_pkgs = list()
        argv = [path, 'lock', '']
        for package, versions in _real_pkgs.items():
            for version in versions:
                argv[-1] = f'{package}-{version}'
                args = ' '.join(argv)
                print_scpt(args, self._file, redirect=self._vflag)
                with open(self._file, 'a') as file:
                    file.write(f'Script started on {date()}\n')
                    file.write(f'command: {args!r}\n')

                try:
                    proc = subprocess.check_output(argv, stderr=make_stderr(self._vflag))
                except subprocess.CalledProcessError:
                    print_text(traceback.format_exc(), self._file, redirect=self._vflag)
                    _real_pkgs = dict()
                else:
                    context = proc.decode()
                    print_text(context, self._file, redirect=self._vflag)
                    _temp_pkgs.extend(filter(lambda s: s.startswith('gem'), context.splitlines(True)))
                finally:
                    with open(self._file, 'a') as file:
                        file.write(f'Script done on {date()}\n')

        suffix = path.replace('/', ':')
        logfile = os.path.join(self._logroot, f'{self.log}-{suffix}{self.ext}')
        with open(logfile, 'w') as file:
            file.write(f"require 'rubygems'{os.linesep}")
            file.writelines(sorted(set(_temp_pkgs)))
