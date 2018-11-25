# -*- coding: utf-8 -*-

import os
import sys

from macdaily.cli.help import get_help_parser, parse_args
from macdaily.util.const import (COMMANDS, MAN_ARCHIVE, MAN_BUNDLE,
                                 MAN_CLEANUP, MAN_COMMANDS, MAN_CONFIG,
                                 MAN_DEPENDENCY, MAN_HELP, MAN_INSTALL,
                                 MAN_LAUNCH, MAN_LOGGING, MAN_POSTINSTALL,
                                 MAN_REINSTALL, MAN_UNINSTALL, MAN_UPDATE,
                                 MAP_ALL, MAP_ARCHIVE, MAP_BUNDLE, MAP_CLEANUP,
                                 MAP_COMMANDS, MAP_CONFIG, MAP_DEPENDENCY,
                                 MAP_HELP, MAP_INSTALL, MAP_LAUNCH,
                                 MAP_LOGGING, MAP_POSTINSTALL, MAP_REINSTALL,
                                 MAP_UNINSTALL, MAP_UPDATE, ROOT)
from macdaily.util.error import CommandNotImplemented


def help_(argv=None):
    # parse args
    args = parse_args(argv)

    if args.command is None:
        pth = os.path.join(ROOT, 'man/macdaily.1')
        os.execlp('man', 'man', pth)

    if args.command in MAP_COMMANDS:
        print(COMMANDS, end='')
        return

    # split args, fetch cmd & sub
    temp = args.command.split('-', maxsplit=1)
    if len(temp) == 2:
        cmd, sub = temp
    else:
        cmd, sub = temp[0], None

    def _find_help(cmd, sub, man):
        pth = None
        if sub is None:
            pth = os.path.join(ROOT, f'man/macdaily-{cmd}.1')
        if sub in man:
            pth = os.path.join(ROOT, f'man/macdaily-{cmd}-{sub}.1')
        if pth is None:
            parser = get_help_parser()
            parser.error(f"argument CMD: invalid choice: {args.command!r} "
                         f"(choose from {', '.join(sorted(MAP_ALL))})")
        os.execlp('man', 'man', pth)

    if cmd in MAP_ARCHIVE:
        _find_help('archive', sub, MAN_ARCHIVE)
    elif cmd in MAP_BUNDLE:
        # _find_help('bundle', sub, MAN_BUNDLE)
        raise CommandNotImplemented
    elif cmd in MAP_CLEANUP:
        _find_help('cleanup', sub, MAN_CLEANUP)
    elif cmd in MAP_CONFIG:
        _find_help('config', sub, MAN_CONFIG)
    elif cmd in MAP_DEPENDENCY:
        _find_help('dependency', sub, MAN_DEPENDENCY)
    elif cmd in MAP_HELP:
        _find_help('help', sub, MAN_HELP)
    elif cmd in MAP_INSTALL:
        _find_help('install', sub, MAN_INSTALL)
    elif cmd in MAP_LAUNCH:
        _find_help('launch', sub, MAN_LAUNCH)
    elif cmd in MAP_LOGGING:
        _find_help('logging', sub, MAN_LOGGING)
    elif cmd in MAP_POSTINSTALL:
        _find_help('postinstall', sub, MAN_POSTINSTALL)
    elif cmd in MAP_REINSTALL:
        _find_help('reinstall', sub, MAN_REINSTALL)
    elif cmd in MAP_UNINSTALL:
        _find_help('uninstall', sub, MAN_UNINSTALL)
    elif cmd in MAP_UPDATE:
        _find_help('update', sub, MAN_UPDATE)
    else:
        parser = get_help_parser()
        parser.error(f"argument CMD: invalid choice: {args.command!r} "
                     f"(choose from {', '.join(sorted(MAP_ALL))})")


if __name__ == '__main__':
    sys.exit(help_())
