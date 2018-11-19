# -*- coding: utf-8 -*-

import datetime
import os
import sys
import traceback
import uuid

from macdaily.cli.logging import parse_args
from macdaily.cls.logging.apm import ApmLogging
from macdaily.cls.logging.app import AppLogging
from macdaily.cls.logging.brew import BrewLogging
from macdaily.cls.logging.cask import CaskLogging
from macdaily.cls.logging.gem import GemLogging
from macdaily.cls.logging.mas import MasLogging
from macdaily.cls.logging.npm import NpmLogging
from macdaily.cls.logging.pip import PipLogging
from macdaily.cls.logging.tap import TapLogging
from macdaily.cmd.config import parse_config
from macdaily.util.const import (__version__, bold, green, purple, red, reset,
                                 under, yellow)
from macdaily.util.misc import (beholder, get_pass, make_namespace, print_misc,
                                print_term, print_text, record)

try:
    import pathlib2 as pathlib
except ImportError:
    import pathlib

try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess


@beholder
def logging(argv=None):
    # parse args & set context redirection flags
    args = parse_args(argv)
    quiet = args.quiet
    verbose = (args.quiet or not args.verbose)

    # parse config & change environ
    config = parse_config(quiet, verbose)
    os.environ['SUDO_ASKPASS'] = config['Miscellanea']['askpass']

    # fetch current time
    today = datetime.datetime.today()
    logdate = datetime.date.strftime(today, r'%y%m%d')
    logtime = datetime.date.strftime(today, r'%H%M%S')

    # prepare command paras
    timeout = config['Miscellanea']['timeout']
    confirm = config['Miscellanea']['confirm']
    askpass = config['Miscellanea']['askpass']
    disk_dir = config['Path']['arcdir']
    brew_renew = None

    # record program status
    text_record = '{}{}|🚨|{} {}Running MacDaily version {}{}'.format(bold, green, reset, bold, __version__, reset)
    print_term(text_record, os.devnull, redirect=quiet)
    record(os.devnull, args, today, config, redirect=verbose)

    # ask for password
    text_askpass = '{}{}|🔑|{} {}Your {}sudo{}{} password may be necessary{}'.format(bold, purple, reset, bold, under, reset, bold, reset)
    print_term(text_askpass, os.devnull, redirect=quiet)
    password = get_pass(askpass)

    cmd_list = list()
    log_list = list()
    for mode in {'apm', 'app', 'brew', 'cask', 'gem', 'mas', 'npm', 'pip', 'tap'}:
        # mkdir for logs
        logpath = pathlib.Path(os.path.join(config['Path']['logdir'], 'logging', mode, logdate))
        logpath.mkdir(parents=True, exist_ok=True)
        filename = os.path.join(logpath, '{}-{!s}.log'.format(logtime, uuid.uuid4()))

        # redo program status records
        print_term(text_record, filename, redirect=True)
        record(filename, args, today, config, redirect=True)
        print_term(text_askpass, filename, redirect=True)

        # skip disabled commands
        if (not config['Mode'].get(mode, False)) or getattr(args, 'no_{}'.format(mode), False):
            text = 'macdaily-logging: {}{}{}: command disabled'.format(yellow, mode, reset)
            print_term(text, filename, redirect=verbose)
            continue

        # update logging specifications
        namespace = getattr(args, mode, None)
        if namespace is None:
            if not args.all:
                continue
            namespace = vars(args)

        # check master controlling flags
        if args.quiet:
            namespace['quiet'] = True
        if args.verbose:
            namespace['verbose'] = True
        if args.show_log:
            namespace['show_log'] = True

        # run command
        cmd_cls = globals()['{}Logging'.format(mode.capitalize())]
        command = cmd_cls(make_namespace(namespace), filename, timeout,
                          confirm, askpass, password, disk_dir, brew_renew)

        # record command
        cmd_list.append(command)
        log_list.append(filename)
        brew_renew = command.time

        if namespace.get('show_log', False):
            try:
                subprocess.check_call(['open', '-a', '/Applications/Utilities/Console.app', filename])
            except subprocess.CalledProcessError:
                print_text(traceback.format_exc(), filename, redirect=verbose)
                print('macdaily: {}logging{}: cannot show log file {!r}'.format(red, reset, filename), file=sys.stderr)

    text = '{}{}|📖|{} {}MacDaily report of logging command{}'.format(bold, green, reset, bold, reset)
    print_term(text, os.devnull, redirect=quiet)
    for file in log_list:
        print_term(text, file, redirect=True)

    for command in cmd_list:
        text = 'Recorded existing {}{}{}{} at {}{}{}'.format(under, command.desc[1], reset, bold, under, command.sample, reset)
        print_misc(text, os.devnull, redirect=quiet)
        for file in log_list:
            print_term(text, file, redirect=True)

    if len(cmd_list) == 0:
        text = 'macdaily: {}logging{}: no packages recorded'.format(purple, reset)
        print_term(text, os.devnull, redirect=quiet)
        for file in log_list:
            print_term(text, file, redirect=True)

    mode_lst = [command.mode for command in cmd_list]
    mode_str = ', '.join(mode_lst) if mode_lst else 'none'
    text = ('{}{}|🍺|{} {}MacDaily successfully performed logging process '
            'for {} package managers{}'.format(bold, green, reset, bold, mode_str, reset))
    print_term(text, os.devnull, redirect=quiet)
    for file in log_list:
        print_term(text, file, redirect=True)


if __name__ == '__main__':
    sys.exit(logging())
