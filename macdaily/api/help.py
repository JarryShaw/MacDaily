# -*- coding: utf-8 -*-

import os
import re
import sys

from macdaily.cli.help import get_help_parser, parse_args
from macdaily.util.const.macro import (CMD_ARCHIVE, CMD_BUNDLE,  # pylint: disable=unused-import
                                       CMD_CLEANUP, CMD_CONFIG, CMD_DEPENDENCY, CMD_HELP,
                                       CMD_INSTALL, CMD_LAUNCH, CMD_LOGGING, CMD_POSTINSTALL,
                                       CMD_REINSTALL, CMD_UNINSTALL, CMD_UPDATE, COMMANDS, MAP_DICT,
                                       MAP_ALL, MAP_ARCHIVE, MAP_BUNDLE, MAP_CLEANUP, MAP_COMMANDS,
                                       MAP_CONFIG, MAP_DEPENDENCY, MAP_HELP, MAP_INSTALL,
                                       MAP_LAUNCH, MAP_LOGGING, MAP_POSTINSTALL, MAP_REINSTALL,
                                       MAP_UNINSTALL, MAP_UPDATE, ROOT)
from macdaily.util.error import CommandNotImplemented


def help_(argv=None):
    # parse args
    args = parse_args(argv)

    if args.command is None:
        pth = os.path.join(ROOT, 'man/macdaily.1')
        os.execlp('man', 'man', pth)

    command = args.command.strip().lower()
    if command in MAP_COMMANDS:
        print(COMMANDS, end='')
        return

    # split args, fetch cmd & sub
    temp = command.split('-', maxsplit=1)
    if len(temp) == 2:
        cmd, sub = temp
    else:
        cmd, sub = temp[0], None

    def _find_help(cmd, sub, man):
        pth = None
        if sub is None:
            pth = os.path.join(ROOT, 'man/macdaily-{}.1'.format(cmd))
        if sub in man:
            pth = os.path.join(ROOT, 'man/macdaily-{}-{}.1'.format(cmd, MAP_DICT[sub]))
        if pth is None:
            CMD = globals().get('CMD_{}'.format(cmd.upper()), set())
            parser = get_help_parser()
            pattern = r'.*{}.*'.format(command)
            matches = "', '".format().join(filter(lambda s: re.match(pattern, s, re.IGNORECASE),  # pylint: disable=cell-var-from-loop
                                          (r'%s-%s' % (cmd, sub) for sub in CMD)))
            if matches:
                parser.error("argument CMD: invalid choice: {!r} "
                             "(did you mean: '{}')".format(args.command, matches))
            else:
                parser.error("argument CMD: invalid choice: {!r} "
                             "(choose from {}-{})".format(args.command, cmd, (', %s-' % cmd).join(sorted(CMD))))
        os.execlp('man', 'man', pth)

    if cmd in MAP_ARCHIVE:
        _find_help('archive', sub, CMD_ARCHIVE)
    elif cmd in MAP_BUNDLE:
        # _find_help('bundle', sub, CMD_BUNDLE)
        raise CommandNotImplemented
    elif cmd in MAP_CLEANUP:
        _find_help('cleanup', sub, CMD_CLEANUP)
    elif cmd in MAP_CONFIG:
        _find_help('config', sub, CMD_CONFIG)
    elif cmd in MAP_DEPENDENCY:
        _find_help('dependency', sub, CMD_DEPENDENCY)
    elif cmd in MAP_HELP:
        _find_help('help', sub, CMD_HELP)
    elif cmd in MAP_INSTALL:
        _find_help('install', sub, CMD_INSTALL)
    elif cmd in MAP_LAUNCH:
        _find_help('launch', sub, CMD_LAUNCH)
    elif cmd in MAP_LOGGING:
        _find_help('logging', sub, CMD_LOGGING)
    elif cmd in MAP_POSTINSTALL:
        _find_help('postinstall', sub, CMD_POSTINSTALL)
    elif cmd in MAP_REINSTALL:
        _find_help('reinstall', sub, CMD_REINSTALL)
    elif cmd in MAP_UNINSTALL:
        _find_help('uninstall', sub, CMD_UNINSTALL)
    elif cmd in MAP_UPDATE:
        _find_help('update', sub, CMD_UPDATE)
    else:
        parser = get_help_parser()
        pattern = r'.*{}.*'.format(cmd)
        matches = "', '".join(filter(lambda s: re.match(pattern, s, re.IGNORECASE), MAP_ALL))  # pylint: disable=cell-var-from-loop
        if matches:
            parser.error('unrecognized arguments: {!r} '
                         "(did you mean: '{}')".format(args.command, matches))
        else:
            parser.error("argument CMD: invalid choice: {!r} "
                         "(choose from {})".format(args.command, ', '.join(sorted(MAP_ALL))))


if __name__ == '__main__':
    sys.exit(help_())
