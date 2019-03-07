# -*- coding: utf-8 -*-

import traceback

from macdaily.cmd.reinstall import ReinstallCommand
from macdaily.core.cask import CaskCommand
from macdaily.util.compat import subprocess
from macdaily.util.const.string import MAX, MIN
from macdaily.util.tools.make import make_stderr
from macdaily.util.tools.misc import date
from macdaily.util.tools.print import print_info, print_scpt, print_text
from macdaily.util.tools.script import run


class CaskReinstall(CaskCommand, ReinstallCommand):

    def _parse_args(self, namespace):
        self._endswith = namespace.get('endswith', MAX)  # pylint: disable=attribute-defined-outside-init
        self._force = namespace.get('force', False)  # pylint: disable=attribute-defined-outside-init
        self._no_cleanup = namespace.get('no_cleanup', False)  # pylint: disable=attribute-defined-outside-init
        self._no_quarantine = namespace.get('no_quarantine', False)  # pylint: disable=attribute-defined-outside-init
        self._startswith = namespace.get('startswith', MIN)  # pylint: disable=attribute-defined-outside-init

        self._all = namespace.get('all', False)  # pylint: disable=attribute-defined-outside-init
        self._quiet = namespace.get('quiet', False)  # pylint: disable=attribute-defined-outside-init
        self._verbose = namespace.get('verbose', False)  # pylint: disable=attribute-defined-outside-init
        self._yes = namespace.get('yes', False)  # pylint: disable=attribute-defined-outside-init

        self._logging_opts = namespace.get('logging', str()).split()  # pylint: disable=attribute-defined-outside-init
        self._reinstall_opts = namespace.get('reinstall', str()).split()  # pylint: disable=attribute-defined-outside-init

    def _check_pkgs(self, path):
        if self._force:
            self._var__temp_pkgs = self._packages  # pylint: disable=attribute-defined-outside-init
            self._var__lost_pkgs = set()  # pylint: disable=attribute-defined-outside-init
        else:
            super()._check_pkgs(path)

    def _check_list(self, path):
        text = 'Checking installed {}'.format(self.desc[1])
        print_info(text, self._file, redirect=self._vflag)

        argv = [path, 'cask', 'list']
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
            self._var__temp_pkgs = set(context.strip().split())  # pylint: disable=attribute-defined-outside-init
            print_text(context, self._file, redirect=self._vflag)
        finally:
            with open(self._file, 'a') as file:
                file.write('Script done on {}\n'.format(date()))

    def _proc_reinstall(self, path):
        text = 'Reinstalling specified {}'.format(self.desc[1])
        print_info(text, self._file, redirect=self._qflag)

        argv = [path, 'cask', 'reinstall']
        if self._force:
            argv.append('--force')
        if self._quiet:
            argv.append('--quiet')
        if self._verbose:
            argv.append('--verbose')
        argv.extend(self._reinstall_opts)

        argv.append('')
        askpass = 'SUDO_ASKPASS={!r}'.format(self._askpass)
        for package in self._var__temp_pkgs:
            argv[-1] = package
            print_scpt(' '.join(argv), self._file, redirect=self._qflag)
            if run(argv, self._file, shell=True, timeout=self._timeout,
                   redirect=self._qflag, verbose=self._vflag, prefix=askpass):
                self._fail.append(package)
            else:
                self._pkgs.append(package)
        del self._var__temp_pkgs
