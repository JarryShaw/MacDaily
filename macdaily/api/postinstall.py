# -*- coding: utf-8 -*-

import datetime
import os
import sys
import traceback
import uuid

from macdaily.cli.postinstall import parse_args
from macdaily.cmd.archive import make_archive
from macdaily.cmd.config import parse_config
from macdaily.cmd.postinstall import PostinstallCommand
from macdaily.util.const import (__version__, bold, green, pink, purple, red,
                                 reset, under, yellow)
from macdaily.util.misc import (beholder, get_pass, make_description,
                                make_namespace, print_misc, print_term,
                                print_text, record)

if sys.version_info[:2] == (3, 4):
    import pathlib2 as pathlib
    import subprocess32 as subprocess
else:
    import pathlib
    import subprocess


@beholder
def postinstall(argv=None):
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
    logpath = pathlib.Path(os.path.join(config['Path']['logdir'], 'postinstall', logdate))
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

    # check if disabled
    enabled = (not config['Mode'].get('brew', False))

    # run command
    if enabled:
        command = PostinstallCommand(make_namespace(args), filename, timeout,
                                     confirm, askpass, password, disk_dir, brew_renew)
    else:
        text = 'macdaily-postinstall: {}brew{}: command disabled'.format(yellow, reset)
        print_term(text, filename, redirect=verbose)

    archive = None
    if not args.no_cleanup:
        archive = make_archive(config, 'postinstall', today, quiet=quiet, verbose=verbose, logfile=filename)

    text = '{}{}|📖|{} {}MacDaily report of postinstall command{}'.format(bold, green, reset, bold, reset)
    print_term(text, filename, redirect=quiet)

    if enabled:
        desc = make_description(command)
        pkgs = '{}{}, {}'.format(reset, bold, green).join(command.packages)
        miss = '{}{}, {}'.format(reset, bold, yellow).join(command.notfound)
        ilst = '{}{}, {}'.format(reset, bold, pink).join(command.ignored)
        fail = '{}{}, {}'.format(reset, bold, red).join(command.failed)

        if pkgs:
            flag = (len(pkgs) == 1)
            text = 'Postinstalled following {}{}{}{}: {}{}{}'.format(under, desc(flag), reset, bold, green, pkgs, reset)
            print_misc(text, filename, redirect=quiet)
        else:
            text = 'No {}{}{}{} postinstalled'.format(under, desc(False), reset, bold)
            print_misc(text, filename, redirect=quiet)

        if fail:
            flag = (len(fail) == 1)
            text = 'Postinstallation of following {}{}{}{} failed: {}{}{}'.format(under, desc(flag), reset, bold, red, fail, reset)
            print_misc(text, filename, redirect=quiet)
        else:
            verb, noun = ('s', '') if len(fail) == 1 else ('', 's')
            text = 'All {}{}{}{} postinstallation{} succeed{}'.format(under, desc(False), reset, bold, noun, verb)
            print_misc(text, filename, redirect=verbose)

        if ilst:
            flag = (len(ilst) == 1)
            text = 'Ignored postinstallation of following {}{}{}{}: {}{}{}'.format(under, desc(flag), reset, bold, pink, ilst, reset)
            print_misc(text, filename, redirect=quiet)
        else:
            text = 'No {}{}{}{} ignored'.format(under, desc(False), reset, bold)
            print_misc(text, filename, redirect=verbose)

        if miss:
            flag = (len(miss) == 1)
            text = 'Following {}{}{}{} not found: {}{}{}'.format(under, desc(flag), reset, bold, yellow, miss, reset)
            print_misc(text, filename, redirect=quiet)
        else:
            text = 'Hit all {}{}{}{} specifications'.format(under, desc(False), reset, bold)
            print_misc(text, filename, redirect=verbose)

    if archive:
        formatted_list = '{}{}, {}'.format(reset, bold, under).join(archive)
        text = ('Archived following ancient logs: {}{}{}'.format(under, formatted_list, reset))
        print_misc(text, filename, redirect=quiet)

    if not enabled:
        text = 'macdaily: {}postinstall{}: no Homebrew formulae postinstalled'.format(purple, reset)
        print_term(text, filename, redirect=quiet)

    if args.show_log:
        try:
            subprocess.check_call(['open', '-a', '/Applications/Utilities/Console.app', filename])
        except subprocess.CalledProcessError:
            print_text(traceback.format_exc(), filename, redirect=verbose)
            print('macdaily: {}postinstall{}: cannot show log file {!r}'.format(red, reset, filename), file=sys.stderr)

    text = ('{}{}|🍺|{} {}MacDaily successfully performed postinstall process{}'.format(bold, green, reset, bold, reset))
    print_term(text, filename, redirect=quiet)


if __name__ == '__main__':
    sys.exit(postinstall())
