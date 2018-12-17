# -*- coding: utf-8 -*-

import datetime
import os
import re
import sys
import traceback
import uuid

from macdaily.cli.launch import get_launch_parser, parse_args
from macdaily.cmd.archive import make_archive
from macdaily.cmd.config import parse_config
from macdaily.cmd.launch import launch_askpass, launch_confirm, launch_daemons
from macdaily.util.const import (__version__, bold, green, purple, red, reset,
                                 under)
from macdaily.util.misc import (beholder, get_pass, print_misc, print_term,
                                print_text, record)

if sys.version_info[:2] == (3, 4):
    import pathlib2 as pathlib
    import subprocess32 as subprocess
else:
    import pathlib
    import subprocess


@beholder
def launch(argv=None):
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
    logpath = pathlib.Path(os.path.join(config['Path']['logdir'], 'launch', logdate))
    logpath.mkdir(parents=True, exist_ok=True)

    # prepare command paras
    filename = os.path.join(logpath, f'{logtime}-{uuid.uuid4()!s}.log')
    askpass = config['Miscellaneous']['askpass']

    # record program status
    text = f'{bold}{green}|🚨|{reset} {bold}Running MacDaily version {__version__}{reset}'
    print_term(text, filename, redirect=quiet)
    record(filename, args, today, config, redirect=verbose)

    # ask for password
    text = f'{bold}{purple}|🔑|{reset} {bold}Your {under}sudo{reset}{bold} password may be necessary{reset}'
    print_term(text, filename, redirect=quiet)
    password = get_pass(askpass)

    # update program list
    if args.all:
        args.program.extend(('askpass', 'confirm', 'daemons'))

    prog_dict = dict()
    for program in set(args.program):
        if re.match(r'^(askpass|confirm|daemons)$', program, re.IGNORECASE) is None:
            parser = get_launch_parser()
            parser.error(f"argument PROG: invalid choice: {program!r} (choose from 'askpass', 'confirm', 'daemons')")

        # launch program
        launch_func = globals()[f'launch_{program.lower()}']
        path = launch_func(quiet=quiet, verbose=verbose, config=config, password=password, logfile=filename)

        # record program
        prog_dict[program] = path

    archive = None
    if not args.no_cleanup:
        archive = make_archive(config, 'launch', today, quiet=quiet, verbose=verbose, logfile=filename)

    text = f'{bold}{green}|📖|{reset} {bold}MacDaily report of launch command{reset}'
    print_term(text, filename, redirect=quiet)

    for prog, path in prog_dict.items():
        text = f'Launched helper program {under}{prog}{reset}{bold} at {under}{path}{reset}'
        print_misc(text, filename, redirect=quiet)

    if archive:
        formatted_list = f'{reset}{bold}, {under}'.join(archive)
        text = (f'Archived following ancient logs: {under}{formatted_list}{reset}')
        print_misc(text, filename, redirect=quiet)

    if len(prog_dict) == 0:
        text = f'macdaily: {purple}launch{reset}: no program launched'
        print_term(text, filename, redirect=quiet)

    if args.show_log:
        try:
            subprocess.check_call(['open', '-a', '/Applications/Utilities/Console.app', filename])
        except subprocess.CalledProcessError:
            print_text(traceback.format_exc(), filename, redirect=verbose)
            print(f'macdaily: {red}launch{reset}: cannot show log file {filename!r}', file=sys.stderr)

    mode_str = ', '.join(prog_dict) if prog_dict else 'none'
    text = (f'{bold}{green}|🍺|{reset} {bold}MacDaily successfully performed launch process '
            f'for {mode_str} helper programs{reset}')
    print_term(text, filename, redirect=quiet)


if __name__ == '__main__':
    sys.exit(launch())
