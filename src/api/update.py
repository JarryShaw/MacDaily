# -*- coding: utf-8 -*-

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


def update(argv):
    args = parse_args(argv)
    config = parse_config()

    filename = None
    timeout = None
    password = None
    disk_dir = None
    brew_renew = None

    cmd_list = list()
    for mode in {'apm', 'brew', 'cask', 'gem', 'mas', 'npm', 'pip', 'system'}:
        if getattr(args, f'no_{mode}'):
            continue

        # update package specifications
        packages = getattr(args, f'{mode}_pkgs')
        namespace = getattr(args, mode)
        if not (packages or namespace or args.all):
            continue
        namespace['packages'].extend(packages)

        # run command
        cmd_cls = globals().get(f'{mode.capitalize()}Update')
        command = cmd_cls(namespace, filename, timeout, password, disk_dir, brew_renew)

        # record command
        cmd_list.append(command)
        brew_renew = command.time
