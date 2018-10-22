# -*- coding: utf-8 -*-

import datetime
import os
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
from macdaily.util.const import __version__
from macdaily.util.misc import make_context
from macdaily.util.tool import record, script

try:
    import pathlib2 as pathlib
except ImportError:
    import pathlib


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
    devnull = open(os.devnull, 'w')
    with make_context(devnull, args.quiet):
        script(['echo', f'|🚨| Running MacDaily version {__version__}'], filename)

        # record program status
        with make_context(devnull, (not args.verbose)):
            record(filename, args, today, config)

        cmd_list = list()
        for mode in {'apm', 'brew', 'cask', 'gem', 'mas', 'npm', 'pip', 'system'}:
            # skip disabled commands
            if not config['Mode'].get(mode, False):
                continue
            if getattr(args, f'no_{mode}', False):
                continue

            # update package specifications
            packages = getattr(args, f'{mode}_pkgs', list())
            namespace = getattr(args, mode, dict())
            if not (packages or namespace or args.all):
                continue
            namespace['packages'].extend(packages)

            # run command
            cmd_cls = globals()[f'{mode.capitalize()}Update']
            command = cmd_cls(namespace, filename, timeout, askpass, disk_dir, brew_renew)

            # record command
            cmd_list.append(command)
            brew_renew = command.time

    devnull.close()
