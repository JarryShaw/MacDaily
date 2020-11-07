# -*- coding: utf-8 -*-

from macdaily.cmd.cleanup import CleanupCommand
from macdaily.core.pip import PipCommand


class PipCleanup(PipCommand, CleanupCommand):

    def _parse_args(self, namespace):
        self._brew = namespace.get('brew', False)  # pylint: disable=attribute-defined-outside-init
        self._cpython = namespace.get('cpython', False)  # pylint: disable=attribute-defined-outside-init
        self._pypy = namespace.get('pypy', False)  # pylint: disable=attribute-defined-outside-init
        self._system = namespace.get('system', False)  # pylint: disable=attribute-defined-outside-init

        self._quiet = namespace.get('quiet', False)  # pylint: disable=attribute-defined-outside-init
        self._verbose = namespace.get('verbose', False)  # pylint: disable=attribute-defined-outside-init
