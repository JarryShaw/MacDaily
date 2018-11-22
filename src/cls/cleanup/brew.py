# -*- coding: utf-8 -*-

from macdaily.cmd.cleanup import CleanupCommand
from macdaily.core.brew import BrewCommand


class BrewCleanup(BrewCommand, CleanupCommand):

    def _parse_args(self, namespace):
        self._quiet = namespace.get('quiet', False)
        self._verbose = namespace.get('verbose', False)
