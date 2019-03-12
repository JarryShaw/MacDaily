# -*- coding: utf-8 -*-

import datetime
import os
import sys
import traceback
import uuid

from macdaily.cli.logging import parse_args
from macdaily.cls.logging.apm import ApmLogging  # pylint: disable=unused-import
from macdaily.cls.logging.app import AppLogging  # pylint: disable=unused-import
from macdaily.cls.logging.brew import BrewLogging  # pylint: disable=unused-import
from macdaily.cls.logging.cask import CaskLogging  # pylint: disable=unused-import
from macdaily.cls.logging.gem import GemLogging  # pylint: disable=unused-import
from macdaily.cls.logging.mas import MasLogging  # pylint: disable=unused-import
from macdaily.cls.logging.npm import NpmLogging  # pylint: disable=unused-import
from macdaily.cls.logging.pip import PipLogging  # pylint: disable=unused-import
from macdaily.cls.logging.tap import TapLogging  # pylint: disable=unused-import
from macdaily.cmd.archive import make_archive, make_storage
from macdaily.cmd.config import parse_config
from macdaily.util.compat import pathlib, subprocess
from macdaily.util.const.macro import VERSION as __version__
from macdaily.util.const.term import bold, green, purple, red, reset, under, yellow
from macdaily.util.tools.deco import beholder
from macdaily.util.tools.get import get_pass, get_logfile
from macdaily.util.tools.make import make_namespace
from macdaily.util.tools.misc import record
from macdaily.util.tools.print import print_misc, print_term, print_text


@beholder
def logging(argv=None):
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

    # prepare command paras
    confirm = config['Miscellaneous']['confirm']
    askpass = config['Miscellaneous']['askpass']
    timeout = config['Miscellaneous']['limit']
    disk_dir = config['Path']['arcdir']
    brew_renew = None

    # record program status
    text_record = '{}{}|🚨|{} {}Running MacDaily version {}{}'.format(bold, green, reset, bold, __version__, reset)
    print_term(text_record, get_logfile(), redirect=quiet)
    record(get_logfile(), args, today, config, redirect=verbose)

    # ask for password
    text_askpass = '{}{}|🔑|{} {}Your {}sudo{}{} password may be necessary{}'.format(bold, purple, reset, bold, under, reset, bold, reset)
    print_term(text_askpass, get_logfile(), redirect=quiet)
    password = get_pass(askpass)

    cmd_list = list()
    log_list = list()
    file_list = list()
    for mode in {'apm', 'app', 'brew', 'cask', 'gem', 'mas', 'npm', 'pip', 'tap'}:
        # mkdir for logs
        logpath = pathlib.Path(os.path.join(config['Path']['logdir'], 'logging', mode, logdate))
        logpath.mkdir(parents=True, exist_ok=True)
        filename = os.path.join(logpath, '{}-{!s}.log'.format(logtime, uuid.uuid4()))
        os.environ['MACDAILY_LOGFILE'] = filename

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
        namespace = getattr(args, mode, vars(args))

        # check master controlling flags
        if args.quiet:
            namespace['quiet'] = True
        if args.verbose:
            namespace['verbose'] = True
        if args.show_log:
            namespace['show_log'] = True
        if args.no_cleanup:
            namespace['no_cleanup'] = True

        # run command
        cmd_cls = globals()['{}Logging'.format(mode.capitalize())]
        command = cmd_cls(make_namespace(namespace), filename, timeout,
                          confirm, askpass, password, disk_dir, brew_renew)

        # record command
        cmd_list.append(command)
        log_list.append(filename)
        brew_renew = command.time

        if not namespace['no_cleanup']:
            archive = make_archive(config, 'logging/{}'.format(mode), today, zipfile=False,
                                   quiet=quiet, verbose=verbose, logfile=filename)
            file_list.extend(archive)

        if namespace.get('show_log', False):
            try:
                subprocess.check_call(['open', '-a', '/Applications/Utilities/Console.app', filename])
            except subprocess.CalledProcessError:
                print_text(traceback.format_exc(), filename, redirect=verbose)
                print('macdaily: {}logging{}: cannot show log file {!r}'.format(red, reset, filename), file=sys.stderr)

    if not args.no_cleanup:
        storage = make_storage(config, today, quiet=quiet, verbose=verbose, logfile=filename)
        file_list.extend(storage)

    text = '{}{}|📖|{} {}MacDaily report of logging command{}'.format(bold, green, reset, bold, reset)
    print_term(text, get_logfile(), redirect=quiet)
    for file in log_list:
        print_term(text, file, redirect=True)

    for command in cmd_list:
        text = 'Recorded existing {}{}{}{} at {}{}{}'.format(under, command.desc[1], reset, bold, under, command.sample, reset)
        print_misc(text, get_logfile(), redirect=quiet)
        for file in log_list:
            print_misc(text, file, redirect=True)

    if file_list:
        formatted_list = '{}{}, {}'.format(reset, bold, under).join(file_list)
        text = ('Archived following ancient logs: {}{}{}'.format(under, formatted_list, reset))
        print_misc(text, filename, redirect=quiet)

    if len(cmd_list) == 0:  # pylint: disable=len-as-condition
        text = 'macdaily: {}logging{}: no packages recorded'.format(purple, reset)
        print_term(text, get_logfile(), redirect=quiet)
        for file in log_list:
            print_term(text, file, redirect=True)

    mode_lst = [command.mode for command in cmd_list]
    mode_str = ', '.join(mode_lst) if mode_lst else 'none'
    text = ('{}{}|🍺|{} {}MacDaily successfully performed logging process '
            'for {} package managers{}'.format(bold, green, reset, bold, mode_str, reset))
    print_term(text, get_logfile(), redirect=quiet)
    for file in log_list:
        print_term(text, file, redirect=True)


if __name__ == '__main__':
    sys.exit(logging())
