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
from macdaily.cmd.archive import make_archive, make_storage
from macdaily.cmd.config import parse_config
from macdaily.util.const import (__version__, bold, green, purple, red, reset,
                                 under, yellow)
from macdaily.util.misc import (beholder, get_pass, make_namespace, print_misc,
                                print_term, print_text, record)

if sys.version_info[:2] == (3, 4):
    import pathlib2 as pathlib
    import subprocess32 as subprocess
else:
    import pathlib
    import subprocess


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
    text_record = f'{bold}{green}|🚨|{reset} {bold}Running MacDaily version {__version__}{reset}'
    print_term(text_record, os.devnull, redirect=quiet)
    record(os.devnull, args, today, config, redirect=verbose)

    # ask for password
    text_askpass = f'{bold}{purple}|🔑|{reset} {bold}Your {under}sudo{reset}{bold} password may be necessary{reset}'
    print_term(text_askpass, os.devnull, redirect=quiet)
    password = get_pass(askpass)

    cmd_list = list()
    log_list = list()
    file_list = list()
    for mode in {'apm', 'app', 'brew', 'cask', 'gem', 'mas', 'npm', 'pip', 'tap'}:
        # mkdir for logs
        logpath = pathlib.Path(os.path.join(config['Path']['logdir'], 'logging', mode, logdate))
        logpath.mkdir(parents=True, exist_ok=True)
        filename = os.path.join(logpath, f'{logtime}-{uuid.uuid4()!s}.log')

        # redo program status records
        print_term(text_record, filename, redirect=True)
        record(filename, args, today, config, redirect=True)
        print_term(text_askpass, filename, redirect=True)

        # skip disabled commands
        if (not config['Mode'].get(mode, False)) or getattr(args, f'no_{mode}', False):
            text = f'macdaily-logging: {yellow}{mode}{reset}: command disabled'
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
        cmd_cls = globals()[f'{mode.capitalize()}Logging']
        command = cmd_cls(make_namespace(namespace), filename, timeout,
                          confirm, askpass, password, disk_dir, brew_renew)

        # record command
        cmd_list.append(command)
        log_list.append(filename)
        brew_renew = command.time

        if not namespace['no_cleanup']:
            archive = make_archive(config, f'logging/{mode}', today, zipfile=False,
                                   quiet=quiet, verbose=verbose, logfile=filename)
            file_list.extend(archive)

        if namespace.get('show_log', False):
            try:
                subprocess.check_call(['open', '-a', '/Applications/Utilities/Console.app', filename])
            except subprocess.CalledProcessError:
                print_text(traceback.format_exc(), filename, redirect=verbose)
                print(f'macdaily: {red}logging{reset}: cannot show log file {filename!r}', file=sys.stderr)

    if not args.no_cleanup:
        storage = make_storage(config, today, quiet=quiet, verbose=verbose, logfile=filename)
        file_list.extend(storage)

    text = f'{bold}{green}|📖|{reset} {bold}MacDaily report of logging command{reset}'
    print_term(text, os.devnull, redirect=quiet)
    for file in log_list:
        print_term(text, file, redirect=True)

    for command in cmd_list:
        text = f'Recorded existing {under}{command.desc[1]}{reset}{bold} at {under}{command.sample}{reset}'
        print_misc(text, os.devnull, redirect=quiet)
        for file in log_list:
            print_misc(text, file, redirect=True)

    if file_list:
        formatted_list = f'{reset}{bold}, {under}'.join(file_list)
        text = (f'Archived following ancient logs: {under}{formatted_list}{reset}')
        print_misc(text, filename, redirect=quiet)

    if len(cmd_list) == 0:
        text = f'macdaily: {purple}logging{reset}: no packages recorded'
        print_term(text, os.devnull, redirect=quiet)
        for file in log_list:
            print_term(text, file, redirect=True)

    mode_lst = [command.mode for command in cmd_list]
    mode_str = ', '.join(mode_lst) if mode_lst else 'none'
    text = (f'{bold}{green}|🍺|{reset} {bold}MacDaily successfully performed logging process '
            f'for {mode_str} package managers{reset}')
    print_term(text, os.devnull, redirect=quiet)
    for file in log_list:
        print_term(text, file, redirect=True)


if __name__ == '__main__':
    sys.exit(logging())
