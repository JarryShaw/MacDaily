# -*- coding: utf-8 -*-

import abc
import os

from macdaily.util.colours import bold, reset, yellow
from macdaily.util.tools import script


class Command(metaclass=abc.ABCMeta):
    """Base command.

    1. keep namespace
    2. decide executable
    3. enumerate and start processors

    """
    @property
    @abc.abstractmethod
    def cmd(self):
        return NotImplemented

    @property
    @abc.abstractmethod
    def act(self):
        """noun, verb, verb pp."""
        return [NotImplemented, NotImplemented, NotImplemented]

    @property
    @abc.abstractmethod
    def mode(self):
        return NotImplemented

    @property
    @abc.abstractmethod
    def desc(self):
        return NotImplemented

    @property
    def packages(self):
        return set(self._pkgs)

    @property
    def failed(self):
        return set(self._fail)

    @property
    def notfound(self):
        return set(self._lost)

    def __init__(self, args, filename, timeout, password):
        if self._check_exec():
            return

        self._timeout = timeout
        self._password = password
        with open(filename, 'a', 1) as self._log:
            no_proc = False
            if self._pkg_args(args):
                self._loc_exec()
                self._run_proc()
            else:
                no_proc = True

        if no_proc or self._packages:
            script(['echo', '-e', f'macdaily-{self.cmd}: {yellow}{self.mode}{reset}: '
                    f'no {bold}{self.desc}{reset} to {self.act[1]}'], filename)

    @abc.abstractmethod
    def _check_exec(self):
        """Return if no executable found."""
        return True

    def _pkg_args(self, args):
        self._args = args
        namespace = vars(args)

        self._merge_packages(namespace)
        self._parse_args(namespace)

        return (self._packages or self._all)

    def _merge_packages(self, namespace):
        temp_pkg = list()
        args_pkg = namespace.pop(f'{self.mode}_pkgs', list())
        for pkgs in args_pkg:
            temp_pkg.extend(filter(None, pkgs.split(',')))
        self._packages = set(temp_pkg)

    @abc.abstractmethod
    def _parse_args(self, namespace):
        self._all = False

    @abc.abstractmethod
    def _loc_exec(self):
        self._exec = list()

    @abc.abstractmethod
    def _run_proc(self):
        self._pkgs = list()
        self._fail = list()
        self._lost = list()
