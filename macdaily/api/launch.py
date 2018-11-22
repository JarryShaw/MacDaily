# -*- coding: utf-8 -*-

import datetime
import os
import re
import sys

from macdaily.cli.launch import get_launch_parser, parse_args
from macdaily.cmd.config import parse_config
from macdaily.cmd.launch import launch_askpass, launch_confirm, launch_daemons
from macdaily.util.const import __version__, bold, green, purple, reset, under
from macdaily.util.misc import (beholder, get_pass, print_misc, print_term,
                                record)


@beholder
def launch(argv=None):
    # parse args & set context redirection flags
    args = parse_args(argv)
    quiet = args.quiet
    verbose = (args.quiet or not args.verbose)

    # parse config & change environ
    config = parse_config(quiet, verbose)
    os.environ['SUDO_ASKPASS'] = config['Miscellanea']['askpass']

    # fetch current time & prepare command paras
    today = datetime.datetime.today()
    askpass = config['Miscellanea']['askpass']

    # record program status
    text = '{}{}|🚨|{} {}Running MacDaily version {}{}'.format(bold, green, reset, bold, __version__, reset)
    print_term(text, os.devnull, redirect=quiet)
    record(os.devnull, args, today, config, redirect=verbose)

    # ask for password
    text = '{}{}|🔑|{} {}Your {}sudo{}{} password may be necessary{}'.format(bold, purple, reset, bold, under, reset, bold, reset)
    print_term(text, os.devnull, redirect=quiet)
    password = get_pass(askpass)

    # update program list
    if args.all:
        args.program.extend('askpass', 'confirm', 'daemons')

    prog_dict = dict()
    for program in set(args.program):
        if re.match(r'^(askpass|confirm|daemons)$', program, re.IGNORECASE) is None:
            parser = get_launch_parser()
            parser.error("argument PROG: invalid choice: {!r} (choose from 'askpass', 'confirm', 'daemons')".format(program))

        # launch program
        launch_func = globals()['launch_{}'.format(program.lower())]
        path = launch_func(quiet=quiet, verbose=verbose, config=config, password=password)

        # record program
        prog_dict[program] = path

    text = '{}{}|📖|{} {}MacDaily report of launch command{}'.format(bold, green, reset, bold, reset)
    print_term(text, os.devnull, redirect=quiet)

    for prog, path in prog_dict.items():
        text = 'Launched helper program {}{}{}{} at {}{}{}'.format(under, prog, reset, bold, under, path, reset)
        print_misc(text, os.devnull, redirect=quiet)

    if len(prog_dict) == 0:
        text = 'macdaily: {}launch{}: no program launched'.format(purple, reset)
        print_term(text, os.devnull, redirect=quiet)

    mode_str = ', '.join(prog_dict) if prog_dict else 'none'
    text = ('{}{}|🍺|{} {}MacDaily successfully performed launch process '
            'for {} helper programs{}'.format(bold, green, reset, bold, mode_str, reset))
    print_term(text, os.devnull, redirect=quiet)


if __name__ == '__main__':
    sys.exit(launch())
