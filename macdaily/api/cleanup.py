# -*- coding: utf-8 -*-

import datetime
import os
import sys
import traceback
import uuid

from macdaily.cli.cleanup import parse_args
from macdaily.cls.cleanup.brew import BrewCleanup
from macdaily.cls.cleanup.cask import CaskCleanup
from macdaily.cls.cleanup.npm import NpmCleanup
from macdaily.cls.cleanup.pip import PipCleanup
from macdaily.cmd.archive import make_archive
from macdaily.cmd.config import parse_config
from macdaily.util.const import (__version__, bold, green, purple, reset,
                                 under, yellow)
from macdaily.util.misc import (beholder, get_pass, make_namespace, print_misc,
                                print_term, print_text, record, red)

if sys.version_info[:2] == (3, 4):
    import pathlib2 as pathlib
    import subprocess32 as subprocess
else:
    import pathlib
    import subprocess


@beholder
def cleanup(argv=None):
    # parse args & set context redirection flags
    args = parse_args(argv)
    quiet = args.quiet
    verbose = (args.quiet or not args.verbose)

    # parse config & change environ
    config = parse_config(quiet, verbose)
    os.environ['SUDO_ASKPASS'] = config['Miscellaneous']['askpass']

    # fetch current time
    today = datetime.datetime.today()
    logdate = datetime.date.strftime(today, r'%y%m%d')
    logtime = datetime.date.strftime(today, r'%H%M%S')

    # mkdir for logs
    logpath = pathlib.Path(os.path.join(config['Path']['logdir'], 'cleanup', logdate))
    logpath.mkdir(parents=True, exist_ok=True)

    # prepare command paras
    filename = os.path.join(logpath, '{}-{!s}.log'.format(logtime, uuid.uuid4()))
    confirm = config['Miscellaneous']['confirm']
    askpass = config['Miscellaneous']['askpass']
    timeout = config['Miscellaneous']['limit']
    disk_dir = config['Path']['arcdir']
    brew_renew = None

    # record program status
    text = '{}{}|🚨|{} {}Running MacDaily version {}{}'.format(bold, green, reset, bold, __version__, reset)
    print_term(text, filename, redirect=quiet)
    record(filename, args, today, config, redirect=verbose)

    # ask for password
    text = '{}{}|🔑|{} {}Your {}sudo{}{} password may be necessary{}'.format(bold, purple, reset, bold, under, reset, bold, reset)
    print_term(text, filename, redirect=quiet)
    password = get_pass(askpass)

    cmd_list = list()
    for mode in {'brew', 'cask', 'npm', 'pip'}:
        # skip disabled commands
        if (not config['Mode'].get(mode, False)) or getattr(args, 'no_{}'.format(mode), False):
            text = 'macdaily-cleanup: {}{}{}: command disabled'.format(yellow, mode, reset)
            print_term(text, filename, redirect=verbose)
            continue

        # update cleanup specifications
        namespace = getattr(args, mode, vars(args))

        # check master controlling flags
        if args.quiet:
            namespace['quiet'] = True
        if args.verbose:
            namespace['verbose'] = True

        # run command
        cmd_cls = globals()['{}Cleanup'.format(mode.capitalize())]
        command = cmd_cls(make_namespace(namespace), filename, timeout,
                          confirm, askpass, password, disk_dir, brew_renew)

        # record command
        cmd_list.append(command)
        brew_renew = command.time

    # archive ancient logs
    archive = make_archive(config, 'cleanup', today, quiet=quiet, verbose=verbose, logfile=filename)

    text = '{}{}|📖|{} {}MacDaily report of cleanup command{}'.format(bold, green, reset, bold, reset)
    print_term(text, filename, redirect=quiet)

    for command in cmd_list:
        text = 'Pruned caches of {}{}{}{}'.format(under, command.name, reset, bold)
        print_misc(text, os.devnull, redirect=quiet)

    if archive:
        formatted_list = '{}{}, {}'.format(reset, bold, under).join(archive)
        text = ('Archived following ancient logs: {}{}{}'.format(under, formatted_list, reset))
        print_misc(text, filename, redirect=quiet)

    if len(cmd_list) == 0:
        text = 'macdaily: {}cleanup{}: no caches cleanup'.format(purple, reset)
        print_term(text, os.devnull, redirect=quiet)

    if args.show_log:
        try:
            subprocess.check_call(['open', '-a', '/Applications/Utilities/Console.app', filename])
        except subprocess.CalledProcessError:
            print_text(traceback.format_exc(), filename, redirect=verbose)
            print('macdaily: {}cleanup{}: cannot show log file {!r}'.format(red, reset, filename), file=sys.stderr)

    mode_lst = [command.mode for command in cmd_list]
    mode_str = ', '.join(mode_lst) if mode_lst else 'none'
    text = ('{}{}|🍺|{} {}MacDaily successfully performed cleanup process '
            'for {} package managers{}'.format(bold, green, reset, bold, mode_str, reset))
    print_term(text, os.devnull, redirect=quiet)


if __name__ == '__main__':
    sys.exit(cleanup())
