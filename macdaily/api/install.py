# -*- coding: utf-8 -*-

import datetime
import os
import sys
import traceback
import uuid

from macdaily.cli.install import parse_args
from macdaily.cls.install.apm import ApmInstall
from macdaily.cls.install.brew import BrewInstall
from macdaily.cls.install.cask import CaskInstall
from macdaily.cls.install.gem import GemInstall
from macdaily.cls.install.mas import MasInstall
from macdaily.cls.install.npm import NpmInstall
from macdaily.cls.install.pip import PipInstall
from macdaily.cls.install.system import SystemInstall
from macdaily.cmd.archive import make_archive
from macdaily.cmd.config import parse_config
from macdaily.util.const import (__version__, bold, green, purple, red, reset,
                                 under, yellow)
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
def install(argv=None):
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
    logpath = pathlib.Path(os.path.join(config['Path']['logdir'], 'install', logdate))
    logpath.mkdir(parents=True, exist_ok=True)

    # prepare command paras
    filename = os.path.join(logpath, '{}-{!s}.log'.format(logtime, uuid.uuid4()))
    confirm = config['Miscellaneous']['confirm']
    askpass = config['Miscellaneous']['askpass']
    timeout = config['Miscellaneous']['limit']
    disk_dir = config['Path']['arcdir']
    brew_renew = None

    # record program status
    text = '{}{}|🚨|{} {}Running MacDaily version {}{}'.format(bold, green, reset, bold, __version__, reset)
    print_term(text, filename, redirect=quiet)
    record(filename, args, today, config, redirect=verbose)

    # ask for password
    text = '{}{}|🔑|{} {}Your {}sudo{}{} password may be necessary{}'.format(bold, purple, reset, bold, under, reset, bold, reset)
    print_term(text, filename, redirect=quiet)
    password = get_pass(askpass)

    cmd_list = list()
    for mode in {'apm', 'brew', 'cask', 'gem', 'mas', 'npm', 'pip', 'system'}:
        # skip disabled commands
        if (not config['Mode'].get(mode, False)):
            text = 'macdaily-install: {}{}{}: command disabled'.format(yellow, mode, reset)
            print_term(text, filename, redirect=verbose)
            continue

        # skip commands with no package spec
        packages = getattr(args, '{}_pkgs'.format(mode), list())
        namespace = getattr(args, mode, None)
        if not (packages or namespace):
            text = 'macdaily-install: {}{}{}: nothing to install'.format(yellow, mode, reset)
            print_term(text, filename, redirect=verbose)
            continue

        # update package specifications
        if namespace is None:
            namespace = dict(vars(args), packages=list())
        namespace['packages'].extend(packages)

        # check master controlling flags
        if args.yes:
            namespace['yes'] = True
        if args.quiet:
            namespace['quiet'] = True
        if args.verbose:
            namespace['verbose'] = True
        if args.no_cleanup:
            namespace['no_cleanup'] = True

        # run command
        cmd_cls = globals()['{}Install'.format(mode.capitalize())]
        command = cmd_cls(make_namespace(namespace), filename, timeout,
                          confirm, askpass, password, disk_dir, brew_renew)

        # record command
        cmd_list.append(command)
        brew_renew = command.time

    archive = None
    if not args.no_cleanup:
        archive = make_archive(config, 'install', today, quiet=quiet, verbose=verbose, logfile=filename)

    text = '{}{}|📖|{} {}MacDaily report of install command{}'.format(bold, green, reset, bold, reset)
    print_term(text, filename, redirect=quiet)

    for command in cmd_list:
        desc = make_description(command)
        pkgs = '{}{}, {}'.format(reset, bold, green).join(command.packages)
        fail = '{}{}, {}'.format(reset, bold, red).join(command.failed)

        if pkgs:
            flag = (len(pkgs) == 1)
            text = 'Installed following {}{}{}{}: {}{}{}'.format(under, desc(flag), reset, bold, green, pkgs, reset)
            print_misc(text, filename, redirect=quiet)
        else:
            text = 'No {}{}{}{} installed'.format(under, desc(False), reset, bold)
            print_misc(text, filename, redirect=quiet)

        if fail:
            flag = (len(fail) == 1)
            text = 'Installation of following {}{}{}{} failed: {}{}{}'.format(under, desc(flag), reset, bold, red, fail, reset)
            print_misc(text, filename, redirect=quiet)
        else:
            verb, noun = ('s', '') if len(fail) == 1 else ('', 's')
            text = 'All {}{}{}{} installation{} succeed{}'.format(under, desc(False), reset, bold, noun, verb)
            print_misc(text, filename, redirect=verbose)

    if archive:
        formatted_list = '{}{}, {}'.format(reset, bold, under).join(archive)
        text = ('Archived following ancient logs: {}{}{}'.format(under, formatted_list, reset))
        print_misc(text, filename, redirect=quiet)

    if len(cmd_list) == 0:
        text = 'macdaily: {}install{}: no packages installed'.format(purple, reset)
        print_term(text, filename, redirect=quiet)

    if args.show_log:
        try:
            subprocess.check_call(['open', '-a', '/Applications/Utilities/Console.app', filename])
        except subprocess.CalledProcessError:
            print_text(traceback.format_exc(), filename, redirect=verbose)
            print('macdaily: {}install{}: cannot show log file {!r}'.format(red, reset, filename), file=sys.stderr)

    mode_lst = [command.mode for command in cmd_list]
    mode_str = ', '.join(mode_lst) if mode_lst else 'none'
    text = ('{}{}|🍺|{} {}MacDaily successfully performed install process '
            'for {} package managers{}'.format(bold, green, reset, bold, mode_str, reset))
    print_term(text, filename, redirect=quiet)


if __name__ == '__main__':
    sys.exit(install())
