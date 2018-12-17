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
    filename = os.path.join(logpath, f'{logtime}-{uuid.uuid4()!s}.log')
    confirm = config['Miscellaneous']['confirm']
    askpass = config['Miscellaneous']['askpass']
    timeout = config['Miscellaneous']['limit']
    disk_dir = config['Path']['arcdir']
    brew_renew = None

    # record program status
    text = f'{bold}{green}|🚨|{reset} {bold}Running MacDaily version {__version__}{reset}'
    print_term(text, filename, redirect=quiet)
    record(filename, args, today, config, redirect=verbose)

    # ask for password
    text = f'{bold}{purple}|🔑|{reset} {bold}Your {under}sudo{reset}{bold} password may be necessary{reset}'
    print_term(text, filename, redirect=quiet)
    password = get_pass(askpass)

    # check if disabled
    enabled = (not config['Mode'].get('brew', False))

    # run command
    if enabled:
        command = PostinstallCommand(make_namespace(args), filename, timeout,
                                     confirm, askpass, password, disk_dir, brew_renew)
    else:
        text = f'macdaily-postinstall: {yellow}brew{reset}: command disabled'
        print_term(text, filename, redirect=verbose)

    archive = None
    if not args.no_cleanup:
        archive = make_archive(config, 'postinstall', today, quiet=quiet, verbose=verbose, logfile=filename)

    text = f'{bold}{green}|📖|{reset} {bold}MacDaily report of postinstall command{reset}'
    print_term(text, filename, redirect=quiet)

    if enabled:
        desc = make_description(command)
        pkgs = f'{reset}{bold}, {green}'.join(command.packages)
        miss = f'{reset}{bold}, {yellow}'.join(command.notfound)
        ilst = f'{reset}{bold}, {pink}'.join(command.ignored)
        fail = f'{reset}{bold}, {red}'.join(command.failed)

        if pkgs:
            flag = (len(pkgs) == 1)
            text = f'Postinstalled following {under}{desc(flag)}{reset}{bold}: {green}{pkgs}{reset}'
            print_misc(text, filename, redirect=quiet)
        else:
            text = f'No {under}{desc(False)}{reset}{bold} postinstalled'
            print_misc(text, filename, redirect=quiet)

        if fail:
            flag = (len(fail) == 1)
            text = f'Postinstallation of following {under}{desc(flag)}{reset}{bold} failed: {red}{fail}{reset}'
            print_misc(text, filename, redirect=quiet)
        else:
            verb, noun = ('s', '') if len(fail) == 1 else ('', 's')
            text = f'All {under}{desc(False)}{reset}{bold} postinstallation{noun} succeed{verb}'
            print_misc(text, filename, redirect=verbose)

        if ilst:
            flag = (len(ilst) == 1)
            text = f'Ignored postinstallation of following {under}{desc(flag)}{reset}{bold}: {pink}{ilst}{reset}'
            print_misc(text, filename, redirect=quiet)
        else:
            text = f'No {under}{desc(False)}{reset}{bold} ignored'
            print_misc(text, filename, redirect=verbose)

        if miss:
            flag = (len(miss) == 1)
            text = f'Following {under}{desc(flag)}{reset}{bold} not found: {yellow}{miss}{reset}'
            print_misc(text, filename, redirect=quiet)
        else:
            text = f'Hit all {under}{desc(False)}{reset}{bold} specifications'
            print_misc(text, filename, redirect=verbose)

    if archive:
        formatted_list = f'{reset}{bold}, {under}'.join(archive)
        text = (f'Archived following ancient logs: {under}{formatted_list}{reset}')
        print_misc(text, filename, redirect=quiet)

    if not enabled:
        text = f'macdaily: {purple}postinstall{reset}: no Homebrew formulae postinstalled'
        print_term(text, filename, redirect=quiet)

    if args.show_log:
        try:
            subprocess.check_call(['open', '-a', '/Applications/Utilities/Console.app', filename])
        except subprocess.CalledProcessError:
            print_text(traceback.format_exc(), filename, redirect=verbose)
            print(f'macdaily: {red}postinstall{reset}: cannot show log file {filename!r}', file=sys.stderr)

    text = (f'{bold}{green}|🍺|{reset} {bold}MacDaily successfully performed postinstall process{reset}')
    print_term(text, filename, redirect=quiet)


if __name__ == '__main__':
    sys.exit(postinstall())
