# -*- coding: utf-8 -*-

from macdaily.cmd.cleanup import CleanupCommand
from macdaily.core.brew import BrewCommand


class BrewCleanup(BrewCommand, CleanupCommand):

    def _parse_args(self, namespace):
        self._quiet = namespace.get('quiet', False)  # pylint: disable=attribute-defined-outside-init
        self._verbose = namespace.get('verbose', False)  # pylint: disable=attribute-defined-outside-init
