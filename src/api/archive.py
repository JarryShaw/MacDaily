# -*- coding: utf-8 -*-

import copy
import datetime
import os
import sys

from macdaily.cli.archive import get_archive_parser, parse_args
from macdaily.cmd.archive import make_archive, make_storage
from macdaily.cmd.config import parse_config
from macdaily.util.const import __version__, bold, green, purple, reset, under
from macdaily.util.misc import beholder, print_misc, print_term, record


@beholder
def archive(argv=None):
    # parse args & set context redirection flags
    args = parse_args(argv)
    quiet = args.quiet
    verbose = (args.quiet or not args.verbose)

    # parse config & change environ
    config = parse_config(quiet, verbose)
    os.environ['SUDO_ASKPASS'] = config['Miscellanea']['askpass']

    # fetch current time
    today = datetime.datetime.today()

    # record program status
    text = f'{bold}{green}|🚨|{reset} {bold}Running MacDaily version {__version__}{reset}'
    print_term(text, os.devnull, redirect=quiet)
    record(os.devnull, args, today, config, redirect=verbose)

    log_pth = {'logging/apm', 'logging/app', 'logging/brew', 'logging/cask',
               'logging/gem', 'logging/mas', 'logging/npm', 'logging/pip', 'logging/tap'}
    all_pth = log_pth | {'cleanup', 'dependency', 'postinstall', 'reinstall', 'tarfile', 'uninstall', 'update'}

    # update path list
    if args.all:
        args.path.extend(all_pth)
    if 'logging' in args.path:
        args.path.remove('logging')
        args.path.extend(log_pth)

    file_dict = dict()
    for mode in set(args.path):
        if mode not in all_pth:
            tmp_pth = all_pth.add('logging')
            parser = get_archive_parser()
            parser.error(f"argument CMD: invalid choice: {mode!r} (choose from {', '.join(sorted(tmp_pth))})")

        # make archives
        file_list = make_archive(config, mode, today, zipfile=False, quiet=quiet, verbose=verbose)

        # record file list
        file_dict[mode] = copy.copy(file_list)

    if not args.no_storage:
        file_list = make_storage(config, today, quiet=quiet, verbose=verbose)
        file_dict['archive'] = copy.copy(file_list)

    text = f'{bold}{green}|📖|{reset} {bold}MacDaily report of archive command{reset}'
    print_term(text, os.devnull, redirect=quiet)

    for mode, file_list in file_dict.items():
        if len(file_list):
            formatted_list = f'{reset}{bold}, {under}'.join(file_list)
            text = f'Archived following ancient logs of {under}{mode}{reset}{bold}: {under}{formatted_list}{reset}'
        else:
            text = f'No ancient logs of {under}{mode}{reset}{bold} archived'
        print_misc(text, os.devnull, redirect=quiet)

    if len(file_list) == 0:
        text = f'macdaily: {purple}archive{reset}: no logs archived'
        print_term(text, os.devnull, redirect=quiet)

    mode_str = ', '.join(file_dict) if file_dict else 'none'
    text = (f'{bold}{green}|🍺|{reset} {bold}MacDaily successfully performed archive process '
            f'for {mode_str} helper programs{reset}')
    print_term(text, os.devnull, redirect=quiet)


if __name__ == '__main__':
    sys.exit(archive())
