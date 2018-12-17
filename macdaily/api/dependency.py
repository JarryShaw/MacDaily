# -*- coding: utf-8 -*-

import datetime
import importlib
import os
import sys
import traceback
import uuid

from macdaily.cli.dependency import parse_args
from macdaily.cls.dependency.brew import BrewDependency
from macdaily.cls.dependency.pip import PipDependency
from macdaily.cmd.archive import make_archive
from macdaily.cmd.config import parse_config
from macdaily.util.const import (__version__, bold, green, pink, purple, red,
                                 reset, under, yellow)
from macdaily.util.misc import (beholder, make_description, make_namespace,
                                print_misc, print_term, print_text, record)

if sys.version_info[:2] == (3, 4):
    import pathlib2 as pathlib
    import subprocess32 as subprocess
else:
    import pathlib
    import subprocess


@beholder
def dependency(argv=None):
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
    logpath = pathlib.Path(os.path.join(config['Path']['logdir'], 'dependency', logdate))
    logpath.mkdir(parents=True, exist_ok=True)

    # prepare command paras
    filename = os.path.join(logpath, '{}-{!s}.log'.format(logtime, uuid.uuid4()))
    confirm = config['Miscellaneous']['confirm']
    askpass = config['Miscellaneous']['askpass']
    timeout = config['Miscellaneous']['limit']
    disk_dir = config['Path']['arcdir']
    brew_renew = None
    password = None

    # record program status
    text = '{}{}|🚨|{} {}Running MacDaily version {}{}'.format(bold, green, reset, bold, __version__, reset)
    print_term(text, filename, redirect=quiet)
    record(filename, args, today, config, redirect=verbose)

    cmd_list = list()
    for mode in {'brew', 'pip'}:
        # skip disabled commands
        if (not config['Mode'].get(mode, False)) or getattr(args, 'no_{}'.format(mode), False):
            text = 'macdaily-dependency: {}{}{}: command disabled'.format(yellow, mode, reset)
            print_term(text, filename, redirect=verbose)
            continue

        # skip commands with no package spec
        packages = getattr(args, '{}_pkgs'.format(mode), list())
        namespace = getattr(args, mode, None)
        if not (packages or namespace or args.all):
            text = 'macdaily-dependency: {}{}{}: nothing to upgrade'.format(yellow, mode, reset)
            print_term(text, filename, redirect=verbose)
            continue

        # update package specifications
        if namespace is None:
            namespace = dict(vars(args), packages=list())
        namespace['packages'].extend(packages)

        # check master controlling flags
        if args.depth:
            namespace['depth'] = args.depth
        if args.quiet:
            namespace['quiet'] = True
        if args.verbose:
            namespace['verbose'] = True
        if args.topological:
            namespace['topological'] = True

        # validate depth option
        depth = namespace.get('depth')
        if depth is not None and depth < 0:
            module = importlib.import_module('macdaily.cli.dependency')
            parser = getattr(module, 'get_{}_parser'.format(mode))()
            parser.error("argument LEVEL: invalid int value: {!r}".format(depth))

        # run command
        cmd_cls = globals()['{}Dependency'.format(mode.capitalize())]
        command = cmd_cls(make_namespace(namespace), filename, timeout,
                          confirm, askpass, password, disk_dir, brew_renew)

        # record command
        cmd_list.append(command)
        brew_renew = command.time

    archive = None
    if not args.no_cleanup:
        archive = make_archive(config, 'update', today, quiet=quiet, verbose=verbose, logfile=filename)

    text = '{}{}|📖|{} {}MacDaily report of dependency command{}'.format(bold, green, reset, bold, reset)
    print_term(text, filename, redirect=quiet)

    for command in cmd_list:
        desc = make_description(command)
        pkgs = '{}{}, {}'.format(reset, bold, green).join(command.packages)
        miss = '{}{}, {}'.format(reset, bold, yellow).join(command.notfound)
        ilst = '{}{}, {}'.format(reset, bold, pink).join(command.ignored)
        fail = '{}{}, {}'.format(reset, bold, red).join(command.failed)

        if pkgs:
            flag = (len(pkgs) == 1)
            text = 'Queried following {}{}{}{}: {}{}{}'.format(under, desc(flag), reset, bold, green, pkgs, reset)
            print_misc(text, filename, redirect=quiet)
        else:
            text = 'No {}{}{}{} queried'.format(under, desc(False), reset, bold)
            print_misc(text, filename, redirect=quiet)

        if fail:
            flag = (len(fail) == 1)
            text = 'Query of following {}{}{}{} failed: {}{}{}'.format(under, desc(flag), reset, bold, red, fail, reset)
            print_misc(text, filename, redirect=quiet)
        else:
            verb, noun = ('s', '') if len(fail) == 1 else ('', 's')
            text = 'All {}{}{}{} query{} succeed{}'.format(under, desc(False), reset, bold, noun, verb)
            print_misc(text, filename, redirect=verbose)

        if ilst:
            flag = (len(ilst) == 1)
            text = 'Ignored query of following {}{}{}{}: {}{}{}'.format(under, desc(flag), reset, bold, pink, ilst, reset)
            print_misc(text, filename, redirect=quiet)
        else:
            text = 'No {}{}{}{} ignored'.format(under, desc(False), reset, bold)
            print_misc(text, filename, redirect=verbose)

        if miss:
            flag = (len(miss) == 1)
            text = 'Following {}{}{}{} not found: {}{}{}'.format(under, desc(flag), reset, bold, yellow, miss, reset)
            print_misc(text, filename, redirect=quiet)
        else:
            text = 'Hit all {}{}{}{} specifications'.format(under, desc(False), reset, bold)
            print_misc(text, filename, redirect=verbose)

    if archive:
        formatted_list = '{}{}, {}'.format(reset, bold, under).join(archive)
        text = ('Archived following ancient logs: {}{}{}'.format(under, formatted_list, reset))
        print_misc(text, filename, redirect=quiet)

    if len(cmd_list) == 0:
        text = 'macdaily: {}dependency{}: no dependency shown'.format(purple, reset)
        print_term(text, filename, redirect=quiet)

    if args.show_log:
        try:
            subprocess.check_call(['open', '-a', '/Applications/Utilities/Console.app', filename])
        except subprocess.CalledProcessError:
            print_text(traceback.format_exc(), filename, redirect=verbose)
            print('macdaily: {}dependency{}: cannot show log file {!r}'.format(red, reset, filename), file=sys.stderr)

    mode_lst = [command.mode for command in cmd_list]
    mode_str = ', '.join(mode_lst) if mode_lst else 'none'
    text = ('{}{}|🍺|{} {}MacDaily successfully performed dependency process '
            'for {} package managers{}'.format(bold, green, reset, bold, mode_str, reset))
    print_term(text, filename, redirect=quiet)


if __name__ == '__main__':
    sys.exit(dependency())
