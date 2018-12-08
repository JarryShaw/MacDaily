# -*- coding: utf-8 -*-

from macdaily.cmd.cleanup import CleanupCommand
from macdaily.core.cask import CaskCommand


class CaskCleanup(CaskCommand, CleanupCommand):

    def _parse_args(self, namespace):
        self._quiet = namespace.get('quiet', False)
        self._verbose = namespace.get('verbose', False)
