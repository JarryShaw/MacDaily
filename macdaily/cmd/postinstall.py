# -*- coding: utf-8 -*-

import traceback

from macdaily.core.brew import BrewCommand
from macdaily.util.compat import subprocess
from macdaily.util.const.string import MAX, MIN
from macdaily.util.tools.misc import date
from macdaily.util.tools.print import print_info, print_scpt, print_text
from macdaily.util.tools.script import run


class PostinstallCommand(BrewCommand):

    @property
    def cmd(self):
        return 'postinstall'

    @property
    def act(self):
        return ('postinstall', 'postinstalled', 'postinstalled')

    @property
    def job(self):
        return ('postinstallation', 'postinstallation')

    def _parse_args(self, namespace):
        self._endswith = namespace.get('endswith', MAX)  # pylint: disable=attribute-defined-outside-init
        self._no_cleanup = namespace.get('no_cleanup', False)  # pylint: disable=attribute-defined-outside-init
        self._startswith = namespace.get('startswith', MIN)  # pylint: disable=attribute-defined-outside-init

        self._all = namespace.get('all', False)  # pylint: disable=attribute-defined-outside-init
        self._quiet = namespace.get('quiet', False)  # pylint: disable=attribute-defined-outside-init
        self._verbose = namespace.get('verbose', False)  # pylint: disable=attribute-defined-outside-init
        self._yes = namespace.get('yes', False)  # pylint: disable=attribute-defined-outside-init

        self._logging_opts = namespace.get('logging', str()).split()  # pylint: disable=attribute-defined-outside-init
        self._postinstall_opts = namespace.get('postinstall', str()).split()  # pylint: disable=attribute-defined-outside-init

    def _run_proc(self):
        self._pkgs = list()
        self._fail = list()
        self._lost = list()
        for path in self._exec:
            text = 'Using {} executable {!r}'.format(self.name, path)
            print_info(text, self._file, redirect=self._qflag)
            if self._proc_logging(path):
                self._proc_postinstall(path)
            else:
                text = 'No {} to postinstall for executable {!r}'.format(self.desc[1], path)
                print_info(text, self._file, redirect=self._qflag)
            self._proc_fixmissing(path)
        self._proc_cleanup()

    def _proc_logging(self, path):
        if self._packages:
            self._check_pkgs(path)
            self._did_you_mean()
        else:
            self._check_list(path)
        return self._check_confirm(path)

    def _check_list(self, path):
        text = 'Checking installed {}'.format(self.desc[1])
        print_info(text, self._file, redirect=self._vflag)

        argv = [path, 'list']
        argv.extend(self._logging_opts)

        args = ' '.join(argv)
        print_scpt(args, self._file, redirect=self._vflag)
        with open(self._file, 'a') as file:
            file.write('Script started on {}\n'.format(date()))
            file.write('command: {!r}\n'.format(args))

        try:
            proc = subprocess.check_output(argv, stderr=subprocess.DEVNULL)
        except subprocess.SubprocessError:
            print_text(traceback.format_exc(), self._file, redirect=self._vflag)
            self._var__temp_pkgs = set()  # pylint: disable=attribute-defined-outside-init
        else:
            context = proc.decode()
            print_text(context, self._file, redirect=self._vflag)

            _temp_pkgs = list()
            for package in context.strip().split():
                if self._startswith <= package <= self._endswith:
                    _temp_pkgs.append(package)
            self._var__temp_pkgs = set(_temp_pkgs)  # pylint: disable=attribute-defined-outside-init
        finally:
            with open(self._file, 'a') as file:
                file.write('Script done on {}\n'.format(date()))

    def _proc_postinstall(self, path):
        text = 'Postinstalling specified {}'.format(self.desc[1])
        print_info(text, self._file, redirect=self._qflag)

        argv = [path, 'postinstall']
        if self._quiet:
            argv.append('--quiet')
        if self._verbose:
            argv.append('--verbose')
        argv.extend(self._postinstall_opts)

        argv.append('')
        for package in self._var__temp_pkgs:
            argv[-1] = package
            print_scpt(' '.join(argv), self._file, redirect=self._qflag)
            if run(argv, self._file, timeout=self._timeout,
                   redirect=self._qflag, verbose=self._vflag):
                self._fail.append(package)
            else:
                self._pkgs.append(package)
        del self._var__temp_pkgs
