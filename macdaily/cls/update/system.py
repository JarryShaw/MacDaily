# -*- coding: utf-8 -*-

import re
import traceback

from macdaily.cmd.update import UpdateCommand
from macdaily.core.system import SystemCommand
from macdaily.util.compat import subprocess
from macdaily.util.tools.make import make_stderr
from macdaily.util.tools.misc import date
from macdaily.util.tools.print import print_info, print_scpt, print_text
from macdaily.util.tools.script import sudo


class SystemUpdate(SystemCommand, UpdateCommand):

    def _parse_args(self, namespace):
        self._recommend = namespace.get('recommended', False)  # pylint: disable=attribute-defined-outside-init
        self._restart = namespace.get('restart', False)  # pylint: disable=attribute-defined-outside-init

        self._all = namespace.get('all', False)  # pylint: disable=attribute-defined-outside-init
        self._quiet = namespace.get('quiet', False)  # pylint: disable=attribute-defined-outside-init
        self._verbose = namespace.get('verbose', False)  # pylint: disable=attribute-defined-outside-init
        self._yes = namespace.get('yes', False)  # pylint: disable=attribute-defined-outside-init

        self._logging_opts = namespace.get('logging', str()).split()  # pylint: disable=attribute-defined-outside-init
        self._update_opts = namespace.get('update', str()).split()  # pylint: disable=attribute-defined-outside-init

    def _check_list(self, path):
        text = 'Checking outdated {}'.format(self.desc[1])
        print_info(text, self._file, redirect=self._vflag)

        argv = [path, '--list']
        argv.extend(self._logging_opts)
        args = ' '.join(argv)
        print_scpt(args, self._file, redirect=self._vflag)
        with open(self._file, 'a') as file:
            file.write('Script started on {}\n'.format(date()))
            file.write('command: {!r}\n'.format(args))

        try:
            proc = subprocess.check_output(argv, stderr=make_stderr(self._vflag))
        except subprocess.SubprocessError:
            print_text(traceback.format_exc(), self._file, redirect=self._vflag)
            self._var__rcmd_pkgs = set()  # pylint: disable=attribute-defined-outside-init
            self._var__norm_pkgs = set()  # pylint: disable=attribute-defined-outside-init
        else:
            context = proc.decode()
            print_text(context, self._file, redirect=self._vflag)

            _rcmd_pkgs = list()
            _norm_pkgs = list()
            for package in filter(lambda s: re.match(r'^\W*[-*]', s), context.strip().splitlines()):
                flag, name = package.split(maxsplit=1)
                if flag == '*':
                    _rcmd_pkgs.append(name)
                if flag == '-':
                    _norm_pkgs.append(name)

            self._var__rcmd_pkgs = set(_rcmd_pkgs)  # pylint: disable=attribute-defined-outside-init
            self._var__norm_pkgs = set(_norm_pkgs)  # pylint: disable=attribute-defined-outside-init
        finally:
            with open(self._file, 'a') as file:
                file.write('Script done on {}\n'.format(date()))
        self._var__temp_pkgs = self._var__rcmd_pkgs | self._var__norm_pkgs  # pylint: disable=attribute-defined-outside-init

    def _proc_update(self, path):
        text = 'Upgrading outdated {}'.format(self.desc[1])
        print_info(text, self._file, redirect=self._qflag)

        if self._recommend:
            _temp_pkgs = self._var__rcmd_pkgs
        else:
            _temp_pkgs = self._var__rcmd_pkgs | self._var__norm_pkgs

        argv = [path, '--install', '--no-scan']
        if self._restart:
            argv.append('--restart')
        if self._quiet:
            argv.append('--quiet')
        argv.extend(self._update_opts)

        argc = ' '.join(argv)
        for package in _temp_pkgs:
            args = '{} {!r}'.format(argc, package)
            print_scpt(args, self._file, redirect=self._qflag)
            if sudo(args, self._file, self._password, timeout=self._timeout,
                    redirect=self._qflag, verbose=self._vflag):
                self._fail.append(package)
            else:
                self._pkgs.append(package)
        del self._var__rcmd_pkgs
        del self._var__norm_pkgs
        del self._var__temp_pkgs
