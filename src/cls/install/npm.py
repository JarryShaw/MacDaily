# -*- coding: utf-8 -*-

from macdaily.cmd.install import InstallCommand
from macdaily.core.npm import NpmCommand
from macdaily.util.misc import print_info, print_scpt, sudo


class NpmInstall(NpmCommand, InstallCommand):

    def _parse_args(self, namespace):
        self._no_cleanup = namespace.get('no_cleanup', False)

        self._quiet = namespace.get('quiet', False)
        self._verbose = namespace.get('verbose', False)
        self._yes = namespace.get('yes', False)

        self._install_opts = namespace.get('install', str()).split()

    def _proc_install(self, path):
        text = 'Installing specified {}'.format(self.desc[1])
        print_info(text, self._file, redirect=self._qflag)

        argv = [path, 'install', '--global']
        if self._quiet:
            argv.append('--quiet')
        if self._verbose:
            argv.append('--verbose')
        argv.extend(self._install_opts)
        argv.append('')

        for package in self._var__temp_pkgs:
            argv[-1] = package
            print_scpt(argv, self._file, redirect=self._qflag)
            if sudo(argv, self._file, self._password, timeout=self._timeout,
                    redirect=self._qflag, verbose=self._vflag):
                self._fail.append(package)
            else:
                self._pkgs.append(package)
        del self._var__temp_pkgs
