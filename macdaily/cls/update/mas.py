# -*- coding: utf-8 -*-

import re
import traceback

from macdaily.cmd.update import UpdateCommand
from macdaily.core.mas import MasCommand
from macdaily.util.compat import subprocess
from macdaily.util.tools.make import make_stderr
from macdaily.util.tools.misc import date
from macdaily.util.tools.print import print_info, print_scpt, print_text
from macdaily.util.tools.script import sudo


class MasUpdate(MasCommand, UpdateCommand):

    def _parse_args(self, namespace):
        self._all = namespace.get('all', False)  # pylint: disable=attribute-defined-outside-init
        self._quiet = namespace.get('quiet', False)  # pylint: disable=attribute-defined-outside-init
        self._yes = namespace.get('yes', False)  # pylint: disable=attribute-defined-outside-init

        self._logging_opts = namespace.get('logging', str()).split()  # pylint: disable=attribute-defined-outside-init
        self._update_opts = namespace.get('update', str()).split()  # pylint: disable=attribute-defined-outside-init

    def _check_list(self, path):
        text = 'Checking outdated {}'.format(self.desc[1])
        print_info(text, self._file, redirect=self._vflag)

        argv = [path, 'outdated']
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
            self._var__temp_pkgs = set()  # pylint: disable=attribute-defined-outside-init
        else:
            context = proc.decode()
            print_text(context, self._file, redirect=self._vflag)

            _temp_pkgs = dict()
            for line in filter(None, context.strip().splitlines()):
                match = re.match(r'(?P<code>\d{10}) (?P<name>.*?) \(.+?\)', line)
                if match is None:
                    continue
                _temp_pkgs[match.group('name')] = match.group('code')
            self._var__temp_pkgs = set(_temp_pkgs.keys())  # pylint: disable=attribute-defined-outside-init
            self._ver__dict_pkgs = _temp_pkgs  # pylint: disable=attribute-defined-outside-init
        finally:
            with open(self._file, 'a') as file:
                file.write('Script done on {}\n'.format(date()))

    def _proc_update(self, path):
        text = 'Upgrading outdated {}'.format(self.desc[1])
        print_info(text, self._file, redirect=self._qflag)

        argv = [path, 'upgrade']
        argv.extend(self._update_opts)

        argc = ' '.join(argv)
        for package in self._var__temp_pkgs:
            code = self._var__dict_pkgs[package]
            print_scpt('{} {} [{}]'.format(argc, package, code), self._file, redirect=self._qflag)
            if sudo('{} {}'.format(argc, code), self._file, self._password, timeout=self._timeout,
                    redirect=self._qflag, verbose=self._vflag):
                self._fail.append(package)
            else:
                self._pkgs.append(package)
        del self._var__temp_pkgs
