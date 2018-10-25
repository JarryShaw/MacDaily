# -*- coding: utf-8 -*-

import datetime
import os
import sys
import traceback
import uuid

from macdaily.cli.update import parse_args
from macdaily.cls.update.apm import ApmUpdate
from macdaily.cls.update.brew import BrewUpdate
from macdaily.cls.update.cask import CaskUpdate
from macdaily.cls.update.gem import GemUpdate
from macdaily.cls.update.mas import MasUpdate
from macdaily.cls.update.npm import NpmUpdate
from macdaily.cls.update.pip import PipUpdate
from macdaily.cls.update.system import SystemUpdate
from macdaily.cmd.config import parse_config
from macdaily.util.const import __version__, bold, green, red, reset, yellow
from macdaily.util.misc import make_context, record, script

try:
    import pathlib2 as pathlib
except ImportError:
    import pathlib

try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess


def update(argv):
    # parse args & config
    args = parse_args(argv)
    config = parse_config()

    # fetch current time
    today = datetime.datetime.today()
    logdate = datetime.date.strftime(today, r'%y%m%d')
    logtime = datetime.date.strftime(today, r'%H%M%S')

    # mkdir for logs
    logpath = pathlib.Path(os.path.join(config['Path']['logdir'], logdate))
    logpath.mkdir(parents=True, exist_ok=True)

    # prepare command paras
    filename = os.path.join(logpath, f'{logtime}-{uuid.uuid4()!s}.log')
    timeout = config['Miscellanea']['timeout']
    askpass = config['Miscellanea']['askpass']
    disk_dir = config['Path']['arcdir']
    brew_renew = None

    # redirect stdout if in quiet mode
    with open(os.devnull, 'w') as devnull:
        with make_context(devnull, args.quiet):
            # record program status
            script(['echo', f'{bold}{green}|🚨|{reset} {bold}Running MacDaily '
                    f'version {__version__}{reset}'], filename)
            record(filename, args, today, config, (not args.verbose))

            cmd_list = list()
            for mode in {'apm', 'brew', 'cask', 'gem', 'mas', 'npm', 'pip', 'system'}:
                # skip disabled commands
                if (not config['Mode'].get(mode, False)) or getattr(args, f'no_{mode}', False):
                    with make_context(devnull, (not args.verbose)):
                        script(['echo', f'macdaily-update: {yellow}{mode}{reset}: command disabled'], filename)
                    continue

                # update package specifications
                packages = getattr(args, f'{mode}_pkgs', list())
                namespace = getattr(args, mode, dict())
                if not (packages or namespace or args.all):
                    with make_context(devnull, (not args.verbose)):
                        script(['echo', f'macdaily-update: {yellow}{mode}{reset}: nothing to upgrade'], filename)
                    continue
                namespace['packages'].extend(packages)

                # run command
                cmd_cls = globals()[f'{mode.capitalize()}Update']
                command = cmd_cls(namespace, filename, timeout, askpass, disk_dir, brew_renew)

                # record command
                cmd_list.append(command)
                brew_renew = command.time

            for command in cmd_list:
                pass

            if args.show_log:
                try:
                    subprocess.check_call(['open', '-a', '/Applications/Utilities/Console.app', filename])
                except subprocess.CalledProcessError:
                    with open(filename, 'a') as file:
                        file.write(traceback.format_exc())
                    print(f'macdaily: {red}update{reset}: cannot show log file {filename!r}', file=sys.stderr)

            mode_list = [command.mode for command in cmd_list]
            modes = ', '.join(mode_list) if mode_list else 'none'
            script(['echo', f'{bold}{green}|🍺|{reset} {bold}MacDaily successfully '
                    f'performed update process for {modes} package managers{reset}'], filename)
