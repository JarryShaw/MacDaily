# -*- coding: utf-8 -*-

import copy
import datetime
import os
import sys
import traceback
import uuid

from macdaily.cli.archive import get_archive_parser, parse_args
from macdaily.cmd.archive import make_archive, make_storage
from macdaily.cmd.config import parse_config
from macdaily.util.const import (__version__, bold, green, pink, purple, red,
                                 reset, under)
from macdaily.util.misc import (beholder, print_misc, print_term, print_text,
                                record)

if sys.version_info[:2] == (3, 4):
    import pathlib2 as pathlib
    import subprocess32 as subprocess
else:
    import pathlib
    import subprocess


@beholder
def archive(argv=None):
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
    logpath = pathlib.Path(os.path.join(config['Path']['logdir'], 'archive', logdate))
    logpath.mkdir(parents=True, exist_ok=True)

    # prepare command paras
    filename = os.path.join(logpath, '{}-{!s}.log'.format(logtime, uuid.uuid4()))
    disk_dir = config['Path']['arcdir']

    # record program status
    text = '{}{}|🚨|{} {}Running MacDaily version {}{}'.format(bold, green, reset, bold, __version__, reset)
    print_term(text, filename, redirect=quiet)
    record(filename, args, today, config, redirect=verbose)

    log_pth = {'logging/apm', 'logging/app', 'logging/brew', 'logging/cask',
               'logging/gem', 'logging/mas', 'logging/npm', 'logging/pip', 'logging/tap'}
    all_pth = log_pth | {'archive', 'cleanup', 'dependency', 'postinstall',
                         'reinstall', 'tarfile', 'uninstall', 'update'}

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
            with open(filename, 'a') as file:
                file.write('macdaily: archive: invalid option: {!r}'.format(mode))
            parser = get_archive_parser()
            parser.error("argument CMD: invalid choice: {!r} (choose from {})".format(mode, ', '.join(sorted(tmp_pth))))

        # make archives
        file_list = make_archive(config, mode, today, zipfile=False, quiet=quiet, verbose=verbose)

        # record file list
        file_dict[mode] = copy.copy(file_list)

    storage = None
    if not args.no_storage:
        storage = make_storage(config, today, quiet=quiet, verbose=verbose)

    text = '{}{}|📖|{} {}MacDaily report of archive command{}'.format(bold, green, reset, bold, reset)
    print_term(text, filename, redirect=quiet)

    for mode, file_list in file_dict.items():
        if len(file_list):
            formatted_list = '{}{}, {}'.format(reset, bold, under).join(file_list)
            text = 'Archived following ancient logs of {}{}{}{}: {}{}{}'.format(pink, mode, reset, bold, under, formatted_list, reset)
        else:
            text = 'No ancient logs of {}{}{}{} archived'.format(under, mode, reset, bold)
        print_misc(text, filename, redirect=quiet)

    if len(file_dict) == 0:
        text = 'macdaily: {}archive{}: no logs archived'.format(purple, reset)
        print_term(text, filename, redirect=quiet)

    if storage:
        formatted_list = '{}{}, {}'.format(reset, bold, under).join(storage)
        text = ('Stored following ancient archived into {}external hard disk{} '
                '{} at {}{}{}{}: {}{}{}'.format(pink, reset, bold, under, disk_dir, reset, bold, under, formatted_list, reset))
        print_misc(text, filename, redirect=quiet)

    if args.show_log:
        try:
            subprocess.check_call(['open', '-a', '/Applications/Utilities/Console.app', filename])
        except subprocess.CalledProcessError:
            print_text(traceback.format_exc(), filename, redirect=verbose)
            print('macdaily: {}archive{}: cannot show log file {!r}'.format(red, reset, filename), file=sys.stderr)

    mode_str = ', '.join(file_dict) if file_dict else 'none'
    text = ('{}{}|🍺|{} {}MacDaily successfully performed archive process '
            'for {} helper programs{}'.format(bold, green, reset, bold, mode_str, reset))
    print_term(text, filename, redirect=quiet)


if __name__ == '__main__':
    sys.exit(archive())
