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
from macdaily.cmd.launch import launch_askpass, launch_confirm, launch_daemons  # pylint: disable=unused-import
from macdaily.util.compat import pathlib, subprocess
from macdaily.util.const.macro import VERSION as __version__
from macdaily.util.const.term import bold, green, purple, red, reset, under
from macdaily.util.tools.deco import beholder
from macdaily.util.tools.get import get_pass
from macdaily.util.tools.misc import record
from macdaily.util.tools.print import print_misc, print_term, print_text


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
    filename = os.path.join(logpath, '{}-{!s}.log'.format(logtime, uuid.uuid4()))
    os.environ['MACDAILY_LOGFILE'] = filename

    askpass = config['Miscellaneous']['askpass']

    # record program status
    text = '{}{}|🚨|{} {}Running MacDaily version {}{}'.format(bold, green, reset, bold, __version__, reset)
    print_term(text, filename, redirect=quiet)
    record(filename, args, today, config, redirect=verbose)

    # ask for password
    text = '{}{}|🔑|{} {}Your {}sudo{}{} password may be necessary{}'.format(bold, purple, reset, bold, under, reset, bold, reset)
    print_term(text, filename, redirect=quiet)
    password = get_pass(askpass)

    # update program list
    if args.all:
        args.program.extend(('askpass', 'confirm', 'daemons'))

    prog_dict = dict()
    for program in set(args.program):
        if re.match(r'^(askpass|confirm|daemons)$', program, re.IGNORECASE) is None:
            parser = get_launch_parser()
            parser.error("argument PROG: invalid choice: {!r} (choose from 'askpass', 'confirm', 'daemons')".format(program))

        # launch program
        launch_func = globals()['launch_{}'.format(program.lower())]
        path = launch_func(quiet=quiet, verbose=verbose, config=config, password=password, logfile=filename)

        # record program
        prog_dict[program] = path

    archive = None
    if not args.no_cleanup:
        archive = make_archive(config, 'launch', today, quiet=quiet, verbose=verbose, logfile=filename)

    text = '{}{}|📖|{} {}MacDaily report of launch command{}'.format(bold, green, reset, bold, reset)
    print_term(text, filename, redirect=quiet)

    for prog, path in prog_dict.items():
        text = 'Launched helper program {}{}{}{} at {}{}{}'.format(under, prog, reset, bold, under, path, reset)
        print_misc(text, filename, redirect=quiet)

    if archive:
        formatted_list = '{}{}, {}'.format(reset, bold, under).join(archive)
        text = ('Archived following ancient logs: {}{}{}'.format(under, formatted_list, reset))
        print_misc(text, filename, redirect=quiet)

    if len(prog_dict) == 0:
        text = 'macdaily: {}launch{}: no program launched'.format(purple, reset)
        print_term(text, filename, redirect=quiet)

    if args.show_log:
        try:
            subprocess.check_call(['open', '-a', '/Applications/Utilities/Console.app', filename])
        except subprocess.CalledProcessError:
            print_text(traceback.format_exc(), filename, redirect=verbose)
            print('macdaily: {}launch{}: cannot show log file {!r}'.format(red, reset, filename), file=sys.stderr)

    mode_str = ', '.join(prog_dict) if prog_dict else 'none'
    text = ('{}{}|🍺|{} {}MacDaily successfully performed launch process '
            'for {} helper programs{}'.format(bold, green, reset, bold, mode_str, reset))
    print_term(text, filename, redirect=quiet)


if __name__ == '__main__':
    sys.exit(launch())
