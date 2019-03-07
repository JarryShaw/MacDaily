# -*- coding: utf-8 -*-

from macdaily.cmd.install import InstallCommand
from macdaily.core.gem import GemCommand
from macdaily.util.tools.print import print_info, print_scpt
from macdaily.util.tools.script import sudo


class GemInstall(GemCommand, InstallCommand):

    def _parse_args(self, namespace):
        self._brew = namespace.get('brew', False)  # pylint: disable=attribute-defined-outside-init
        self._system = namespace.get('system', False)  # pylint: disable=attribute-defined-outside-init

        self._quiet = namespace.get('quiet', False)  # pylint: disable=attribute-defined-outside-init
        self._verbose = namespace.get('verbose', False)  # pylint: disable=attribute-defined-outside-init
        self._yes = namespace.get('yes', False)  # pylint: disable=attribute-defined-outside-init

        self._install_opts = namespace.get('install', str()).split()  # pylint: disable=attribute-defined-outside-init

    def _proc_install(self, path):
        text = 'Installing specified {}'.format(self.desc[1])
        print_info(text, self._file, redirect=self._qflag)

        argv = [path, 'install']
        if self._quiet:
            argv.append('--quiet')
        if self._verbose:
            argv.append('--verbose')
        argv.extend(self._install_opts)

        argc = ' '.join(argv)
        for package in self._var__temp_pkgs:
            args = '{} {}'.format(argc, package)
            print_scpt(args, self._file, redirect=self._qflag)
            yes = 'y' if self._yes else None
            if sudo(argv, self._file, self._password, timeout=self._timeout,
                    redirect=self._qflag, verbose=self._vflag, yes=yes):
                self._fail.append(package)
            else:
                self._pkgs.append(package)
        del self._var__temp_pkgs
