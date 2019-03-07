# -*- coding: utf-8 -*-

from macdaily.cmd.install import InstallCommand
from macdaily.core.apm import ApmCommand
from macdaily.util.tools.print import print_info, print_scpt
from macdaily.util.tools.script import run


class ApmInstall(ApmCommand, InstallCommand):

    def _parse_args(self, namespace):
        self._beta = namespace.get('beta', False)  # pylint: disable=attribute-defined-outside-init

        self._quiet = namespace.get('quiet', False)  # pylint: disable=attribute-defined-outside-init
        self._verbose = namespace.get('verbose', False)  # pylint: disable=attribute-defined-outside-init
        self._yes = namespace.get('yes', False)  # pylint: disable=attribute-defined-outside-init

        self._install_opts = namespace.get('install', str()).split()  # pylint: disable=attribute-defined-outside-init

    def _proc_install(self, path):
        text = f'Installing specified {self.desc[1]}'
        print_info(text, self._file, redirect=self._qflag)

        argv = [path, 'install']
        if self._quiet:
            argv.append('--quiet')
        if self._verbose:
            argv.append('--verbose')
        argv.extend(self._install_opts)
        argv.append('')

        for package in self._var__temp_pkgs:
            argv[-1] = package
            print_scpt(argv, self._file, redirect=self._qflag)
            if run(argv, self._file, timeout=self._timeout,
                   redirect=self._qflag, verbose=self._vflag):
                self._fail.append(package)
            else:
                self._pkgs.append(package)
        del self._var__temp_pkgs
