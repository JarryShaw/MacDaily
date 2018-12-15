# -*- coding: utf-8 -*-

import contextlib
import copy
import json
import os
import re
import sys
import tempfile
import traceback

from macdaily.cmd.dependency import DependencyCommand
from macdaily.core.pip import PipCommand
from macdaily.util.misc import (bold, date, make_stderr, print_info,
                                print_scpt, print_term, print_text, red, reset,
                                under, yellow)

if sys.version_info[:2] == (3, 4):
    import subprocess32 as subprocess
else:
    import subprocess


class PipDependency(PipCommand, DependencyCommand):

    def _parse_args(self, namespace):
        self._brew = namespace.get('brew', False)
        self._cpython = namespace.get('cpython', False)
        self._depth = namespace.get('depth', -1)
        self._pypy = namespace.get('pypy', False)
        self._system = namespace.get('system', False)
        self._topological = namespace.get('topological', False)
        self._tree = namespace.get('tree', False)
        self._user = namespace.get('user', False)

        self._all = namespace.get('all', False)
        self._quiet = namespace.get('quiet', False)
        self._verbose = namespace.get('verbose', False)

    def _check_list(self, path):
        text = f'Checking installed {self.desc[1]}'
        print_info(text, self._file, redirect=self._vflag)

        argv = [path, '-m', 'pip', 'list', '--not-required', '--format=columns']
        args = ' '.join(argv)
        print_scpt(args, self._file, redirect=self._vflag)
        with open(self._file, 'a') as file:
            file.write(f'Script started on {date()}\n')
            file.write(f'command: {args!r}\n')

        argv[-1] = '--format=json'
        try:
            proc = subprocess.check_output(argv, stderr=make_stderr(self._vflag))
        except subprocess.SubprocessError:
            print_text(traceback.format_exc(), self._file, redirect=self._vflag)
            self._var__temp_pkgs = set()
        else:
            # self._var__temp_pkgs = set(map(lambda pkg: pkg.split('==')[0], proc.decode().split()))
            text = proc.decode()
            start = text.rfind('[')
            stop = text.rfind(']') + 1
            context = json.loads(text[start:stop])
            self._var__temp_pkgs = set(map(lambda item: item['name'], context))

            prefix = text[:start]
            if prefix:
                print_text(prefix, self._file, redirect=self._vflag)
            if context:
                name_len = max(7, max(map(lambda item: len(item['name']), context), default=7))
                version_len = max(7, max(map(lambda item: len(item['version']), context), default=7))

                def _pprint(package, version):
                    text = [package.ljust(name_len), version.ljust(version_len)]
                    return ' '.join(text)

                print_text(_pprint('Package', 'Version'), self._file, redirect=self._vflag)
                print_text(' '.join(map(lambda length: '-' * length,
                                        [name_len, version_len])), self._file, redirect=self._vflag)
                for item in context:
                    print_text(_pprint(item['name'], item['version']), self._file, redirect=self._vflag)
        finally:
            with open(self._file, 'a') as file:
                file.write(f'Script done on {date()}\n')

    def _proc_dependency(self, path):
        text = f'Querying dependencies of {self.desc[1]}'
        print_info(text, self._file, redirect=self._qflag)

        def _fetch_dependency(package, depth):
            if depth == 0:
                return dict()
            depth -= 1

            dependencies = _data_pkgs.get(package)
            if dependencies is not None:
                return dependencies

            text = f'Searching dependencies of {self.desc[0]} {under}{package}{reset}'
            print_info(text, self._file, redirect=self._vflag)

            argv = [path, '-m', 'pip', 'show', package]
            args = ' '.join(argv)
            print_scpt(args, self._file, redirect=self._vflag)
            with open(self._file, 'a') as file:
                file.write(f'Script started on {date()}\n')
                file.write(f'command: {args!r}\n')

            _deps_pkgs = dict()
            try:
                proc = subprocess.check_output(argv, stderr=make_stderr(self._vflag))
            except subprocess.CalledProcessError:
                self._fail.append(package)
                with contextlib.suppress(KeyError):
                    self._var__temp_pkgs.remove(package)
                print_text(traceback.format_exc(), self._file, redirect=self._vflag)
            else:
                context = proc.decode()
                print_text(context, self._file, redirect=self._vflag)

                requirements = set()
                for line in context.strip().splitlines():
                    match = re.match(r'Requires: (.*)', line)
                    if match is not None:
                        requirements = set(match.groups()[0].split(', '))
                        break

                _list_pkgs.append(package)
                for item in filter(None, requirements):
                    if item in self._var__temp_pkgs:
                        self._var__temp_pkgs.remove(item)
                    _deps_pkgs[item] = _fetch_dependency(item, depth)
                _data_pkgs.update(_deps_pkgs)
            finally:
                with open(self._file, 'a') as file:
                    file.write(f'Script done on {date()}\n')
            return _deps_pkgs

        _list_pkgs = list()
        _deps_pkgs = dict()
        _data_pkgs = dict()
        _temp_pkgs = copy.copy(self._var__temp_pkgs)
        for package in _temp_pkgs:
            _deps_pkgs[package] = _fetch_dependency(package, self._depth)
        self._pkgs.extend(_list_pkgs)

        def _print_dependency_tree(package, dependencies):
            with tempfile.NamedTemporaryFile() as dumpfile:
                dumper = dictdumper.Tree(dumpfile.name, quiet=True)
                dumper(dependencies, name=package)

                with open(dumpfile.name) as file:
                    for line in filter(None, file):
                        print_text(line.strip(), self._file)

        def _print_dependency_text(package, dependencies):
            def _list_dependency(dependencies):
                _list_pkgs = list()
                for package, deps_pkgs in dependencies.items():
                    _list_pkgs.append(package)
                    _list_pkgs.extend(_list_dependency(deps_pkgs))
                return _list_pkgs

            _list_pkgs = list()
            for item in reversed(_list_dependency(dependencies)):
                if item in _list_pkgs:
                    continue
                _list_pkgs.append(item)

            if not self._topological:
                _list_pkgs.sort()
            if self._qflag:
                if _list_pkgs:
                    print_term(f"{package}: {' '.join(_list_pkgs)}", self._file)
                else:
                    print_term(f"{package} (independent)", self._file)
            else:
                print_text(os.linesep.join(_list_pkgs), self._file)

        text = f'Listing dependencies of {self.desc[1]}'
        print_info(text, self._file, redirect=self._vflag)

        argv = [path, 'dependency']
        if self._tree:
            argv.append('--tree')
        if self._quiet:
            argv.append('--quiet')
        if self._verbose:
            argv.append('--verbose')
        if self._topological:
            argv.append('--topological')
        if self._depth != -1:
            argv.append(f'--depth={self._depth}')
        argv.append('')

        if self._qflag:
            print_scpt(path, os.devnull)

        for package in sorted(self._var__temp_pkgs):
            argv[-1] = package
            print_scpt(' '.join(argv), self._file, redirect=self._qflag)
            if self._tree:
                try:
                    import dictdumper
                except ImportError:
                    print_term(f'macdaily-dependency: {yellow}pip{reset}: {bold}DictDumper{reset} not installed, '
                               f"which is mandatory for using `{bold}--tree{reset}' option",
                               self._file, redirect=self._vflag)
                    print(f'macdaily-dependency: {red}pip{reset}: broken dependency', file=sys.stderr)
                    raise
                _print_dependency_tree(package, _deps_pkgs[package])
            else:
                _print_dependency_text(package, _deps_pkgs[package])
        del self._var__temp_pkgs
