# -*- coding: utf-8 -*-

import datetime
import os
import re
import sys

from macdaily.cli.launch import get_launch_parser, parse_args
from macdaily.cmd.launch import launch_askpass, launch_confirm
from macdaily.util.const import __version__, bold, green, purple, reset, under
from macdaily.util.misc import beholder, print_misc, print_term, record


@beholder
def launch(argv=None):
    # parse args & set context redirection flags
    args = parse_args(argv)
    quiet = args.quiet
    verbose = (args.quiet or not args.verbose)

    # fetch current time
    today = datetime.datetime.today()

    # record program status
    text = f'{bold}{green}|🚨|{reset} {bold}Running MacDaily version {__version__}{reset}'
    print_term(text, os.devnull, redirect=quiet)
    record(os.devnull, args, today, redirect=verbose)

    prog_dict = dict()
    for program in set(args.program):
        if re.match(r'^(askpass|confirm)$', program, re.IGNORECASE) is None:
            parser = get_launch_parser()
            parser.error(f"argument PROG: invalid choice: {program!r} (choose from 'askpass', 'confirm')")

        # launch program
        launch_func = globals()[f'launch_{program.lower()}']
        path = launch_func(quiet, verbose)

        # record program
        prog_dict[program] = path

    text = f'{bold}{green}|📖|{reset} {bold}MacDaily report of launch command{reset}'
    print_term(text, os.devnull, redirect=quiet)

    for prog, path in prog_dict.items():
        text = f'Launched helper program {under}{prog}{reset}{bold} at {under}{path}{reset}'
        print_misc(text, os.devnull, redirect=quiet)

    if len(prog_dict) == 0:
        text = f'macdaily: {purple}launch{reset}: no program launched'
        print_term(text, os.devnull, redirect=quiet)

    mode_str = ', '.join(prog_dict) if prog_dict else 'no'
    text = (f'{bold}{green}|🍺|{reset} {bold}MacDaily successfully performed launch process '
            f'for {mode_str} helper programs{reset}')
    print_term(text, os.devnull, redirect=quiet)


if __name__ == '__main__':
    sys.exit(launch())
