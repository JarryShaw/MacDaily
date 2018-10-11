# -*- coding: utf-8 -*-

import abc


class Command(metaclass=abc.ABCMeta):
    """Base command.

    1. keep namespace
    2. decide executable
    3. enumerate and start processors

    """
    @property
    @abc.abstractmethod
    def mode(self):
        return NotImplemented

    @property
    def packages(self):
        return set(self._pkgs)

    def __init__(self, args):
        self._pkg_args(args)
        self._loc_exec()
        self._run_proc()

    def _pkg_args(self, args):
        self._args = args
        namespace = vars(args)

        self._merge_packages(namespace)
        self._parse_args(namespace)

    def _merge_packages(self, namespace):
        temp_pkg = list()
        args_pkg = namespace.pop(f'{self.mode}_pkgs', list())
        for pkgs in args_pkg:
            temp_pkg.extend(filter(None, pkgs.split(',')))
        self._packages = set(temp_pkg)

    @abc.abstractmethod
    def _parse_args(self, namespace):
        pass

    @abc.abstractmethod
    def _loc_exec(self):
        self._exec = list()

    @abc.abstractmethod
    def _run_proc(self):
        self._pkgs = list()
