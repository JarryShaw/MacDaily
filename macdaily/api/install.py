# -*- coding: utf-8 -*-

import datetime
import os
import sys
import traceback
import uuid

from macdaily.cli.install import parse_args
from macdaily.cls.install.apm import ApmInstall  # pylint: disable=unused-import
from macdaily.cls.install.brew import BrewInstall  # pylint: disable=unused-import
from macdaily.cls.install.cask import CaskInstall  # pylint: disable=unused-import
from macdaily.cls.install.gem import GemInstall  # pylint: disable=unused-import
from macdaily.cls.install.mas import MasInstall  # pylint: disable=unused-import
from macdaily.cls.install.npm import NpmInstall  # pylint: disable=unused-import
from macdaily.cls.install.pip import PipInstall  # pylint: disable=unused-import
from macdaily.cls.install.system import SystemInstall  # pylint: disable=unused-import
from macdaily.cmd.archive import make_archive
from macdaily.cmd.config import parse_config
from macdaily.util.compat import pathlib, subprocess
from macdaily.util.const.macro import VERSION as __version__
from macdaily.util.const.term import bold, green, purple, red, reset, under, yellow
from macdaily.util.tools.deco import beholder
from macdaily.util.tools.get import get_pass
from macdaily.util.tools.make import make_description, make_namespace
from macdaily.util.tools.misc import record
from macdaily.util.tools.print import print_misc, print_term, print_text


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
    filename = os.path.join(logpath, f'{logtime}-{uuid.uuid4()!s}.log')
    os.environ['MACDAILY_LOGFILE'] = filename

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

    cmd_list = list()
    for mode in {'apm', 'brew', 'cask', 'gem', 'mas', 'npm', 'pip', 'system'}:
        # skip disabled commands
        if not config['Mode'].get(mode, False):
            text = f'macdaily-install: {yellow}{mode}{reset}: command disabled'
            print_term(text, filename, redirect=verbose)
            continue

        # skip commands with no package spec
        packages = getattr(args, f'{mode}_pkgs', list())
        namespace = getattr(args, mode, None)
        if not (packages or namespace):
            text = f'macdaily-install: {yellow}{mode}{reset}: nothing to install'
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
        cmd_cls = globals()[f'{mode.capitalize()}Install']
        command = cmd_cls(make_namespace(namespace), filename, timeout,
                          confirm, askpass, password, disk_dir, brew_renew)

        # record command
        cmd_list.append(command)
        brew_renew = command.time

    archive = None
    if not args.no_cleanup:
        archive = make_archive(config, 'install', today, quiet=quiet, verbose=verbose, logfile=filename)

    text = f'{bold}{green}|📖|{reset} {bold}MacDaily report of install command{reset}'
    print_term(text, filename, redirect=quiet)

    for command in cmd_list:
        desc = make_description(command)
        pkgs = f'{reset}{bold}, {green}'.join(command.packages)
        fail = f'{reset}{bold}, {red}'.join(command.failed)

        if pkgs:
            flag = (len(pkgs) == 1)
            text = f'Installed following {under}{desc(flag)}{reset}{bold}: {green}{pkgs}{reset}'
            print_misc(text, filename, redirect=quiet)
        else:
            text = f'No {under}{desc(False)}{reset}{bold} installed'
            print_misc(text, filename, redirect=quiet)

        if fail:
            flag = (len(fail) == 1)
            text = f'Installation of following {under}{desc(flag)}{reset}{bold} failed: {red}{fail}{reset}'
            print_misc(text, filename, redirect=quiet)
        else:
            verb, noun = ('s', '') if len(fail) == 1 else ('', 's')
            text = f'All {under}{desc(False)}{reset}{bold} installation{noun} succeed{verb}'
            print_misc(text, filename, redirect=verbose)

    if archive:
        formatted_list = f'{reset}{bold}, {under}'.join(archive)
        text = (f'Archived following ancient logs: {under}{formatted_list}{reset}')
        print_misc(text, filename, redirect=quiet)

    if len(cmd_list) == 0:  # pylint: disable=len-as-condition
        text = f'macdaily: {purple}install{reset}: no packages installed'
        print_term(text, filename, redirect=quiet)

    if args.show_log:
        try:
            subprocess.check_call(['open', '-a', '/Applications/Utilities/Console.app', filename])
        except subprocess.CalledProcessError:
            print_text(traceback.format_exc(), filename, redirect=verbose)
            print(f'macdaily: {red}install{reset}: cannot show log file {filename!r}', file=sys.stderr)

    mode_lst = [command.mode for command in cmd_list]
    mode_str = ', '.join(mode_lst) if mode_lst else 'none'
    text = (f'{bold}{green}|🍺|{reset} {bold}MacDaily successfully performed install process '
            f'for {mode_str} package managers{reset}')
    print_term(text, filename, redirect=quiet)


if __name__ == '__main__':
    sys.exit(install())
