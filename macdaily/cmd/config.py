# -*- coding: utf-8 -*-

import collections
import configparser
import contextlib
import datetime
import os
import re
import shlex
import sys

from macdaily.cmd.launch import launch_askpass, launch_confirm, run_script
from macdaily.util.const import ROOT
from macdaily.util.error import ConfigNotFoundError


CONFIG = ['[Path]',
          '# In this section, paths for log files are specified.',
          '# Please, under any circumstances, make sure they are valid.',
          'logdir = ~/Library/Logs/MacDaily                            ; path where logs will be stored',
          'dskdir = /Volumes/Your Disk                                 ; path where your hard disk lies',
          'arcdir = ${dskdir}/Developers                               ; path where ancient logs archive',
          '',
          '[Mode]',
          '# In this section, flags for modes are configured.',
          '# If you would like to disable the mode, set it to "false".',
          'apm     = true                                              ; Atom plug-ins',
          'app     = true                                              ; macOS Applications',
          'brew    = true                                              ; Homebrew Formulae',
          'cask    = true                                              ; Homebrew Casks',
          'cleanup = true                                              ; cleanup caches',
          'gem     = true                                              ; Ruby gems',
          'mas     = true                                              ; Mac App Store applications',
          'npm     = true                                              ; Node.js modules',
          'pip     = true                                              ; Python packages',
          'system  = true                                              ; macOS software',
          'tap     = true                                              ; Homebrew Taps',
          '',
          '[Daemon]',
          '# In this section, scheduled tasks are set up.',
          '# You may append and/or remove the time intervals.',
          'archive     = false                                         ; archive logs',
          'bundle      = false                                         ; bundle packages',
          'cleanup     = false                                         ; cleanup caches',
          'config      = false                                         ; config MacDaily',
          'dependency  = false                                         ; show dependencies',
          'install     = false                                         ; install packages',
          'launch      = false                                         ; launch daemons',
          'logging     = true                                          ; log installed packages',
          'postinstall = false                                         ; postinstall packages',
          'reinstall   = false                                         ; reinstall packages',
          'uninstall   = false                                         ; uninstall packages',
          'update      = true                                          ; update packages',
          'schedule    =                                               ; scheduled timing (in 24 hours)',
          '    8:00                                                    ; update & logging at 8:00',
          '    22:30-update                                            ; update at 22:30',
          '    23:00-logging                                           ; logging at 23:00',
          '',
          '[Command]',
          '# In this section, command options are picked.',
          '# Do make sure these options are available for commands.',
          'update  = --all --quiet --show-log',
          'logging = --all --quiet --show-log',
          '',
          '[Miscellanea]',
          '# In this section, miscellaneous specifications are assigned.',
          '# Please, under any circumstances, make sure all fields are valid.',
          'askpass = ...                                               ; SUDO_ASKPASS utility for Homebrew Casks',
          'confirm = ...                                               ; confirm utility for MacDaily',
          'timeout = 300                                               ; timeout limit for shell commands in seconds',
          '']


def get_config():
    config = configparser.ConfigParser(inline_comment_prefixes=(';',),
                                       interpolation=configparser.ExtendedInterpolation())
    config.SECTCRE = re.compile(r'\[\s*(?P<header>[^]]+?)\s*\]')
    config.read_string(os.linesep.join(CONFIG))
    return config


def dump_config(rcpath, quiet=False, verbose=False):
    if not sys.stdin.isatty():
        raise ConfigNotFoundError(2, 'No such file or directory', rcpath)

    askpass = launch_askpass(quiet=quiet, verbose=verbose)
    confirm = launch_confirm(quiet=quiet, verbose=verbose)

    CONFIG[51] = 'askpass = {} ; SUDO_ASKPASS utility for Homebrew Casks'.format(askpass.ljust(49))
    CONFIG[52] = 'confirm = {} ; confirm utility for MacDaily'.format(confirm.ljust(49))

    with open(rcpath, 'w') as file:
        file.write(os.linesep.join(CONFIG))
    return get_config()


def load_config(rcpath):
    config = get_config()
    with open(rcpath) as file:
        config.read_file(file)
    return config


def parse_config(quiet=False, verbose=False):
    rcpath = os.path.expanduser('~/.dailyrc')
    if os.path.isfile(rcpath):
        config = load_config(rcpath)
    else:
        config = dump_config(rcpath, quiet, verbose)
    cfg_dict = collections.defaultdict(dict)

    # Path section
    for name, path in config['Path'].items():
        cfg_dict['Path'][name] = os.path.realpath(os.path.expanduser(path))

    # Mode section
    for mode in config['Mode'].keys():
        cfg_dict['Mode'][mode] = config['Mode'].getboolean(mode, False)

    # Daemon section
    daemon_list = list()
    for mode in {'archive', 'bundle', 'cleanup', 'config', 'dependency', 'launch',
                 'logging', 'postinstall', 'reinstall', 'uninstall', 'update'}:
        if config['Daemon'].getboolean(mode, False):
            daemon_list.append(mode)

    daemon_dict = collections.defaultdict(list)
    for daemon in config['Daemon']['schedule'].strip().splitlines():
        union = re.split(r'\s*-\s*', daemon)
        with contextlib.suppress(ValueError):
            time = datetime.datetime.strptime(union[0], r'%H:%M')
            if len(union) == 2:
                daemon_dict[union[1]].append(dict(Hour=time.hour, Minute=time.minute))
            else:
                for mode in daemon_list:
                    daemon_dict[mode].append(dict(Hour=time.hour, Minute=time.minute))
    cfg_dict['Daemon'].update(daemon_dict)

    # Command section
    for mode, argv in config['Command'].items():
        cfg_dict['Command'][mode] = shlex.split(argv)

    # Miscellanea section
    askpass = os.path.realpath(config['Miscellanea']['askpass'])
    if not os.access(askpass, os.X_OK):
        askpass = os.path.join(ROOT, 'res', 'askpass.applescript')
        run_script(['sudo', 'chmod', 'u+x', askpass], quiet, verbose)

    confirm = os.path.realpath(config['Miscellanea']['confirm'])
    if not os.access(confirm, os.X_OK):
        confirm = os.path.join(ROOT, 'res', 'confirm.applescript')
        run_script(['sudo', 'chmod', 'u+x', confirm], quiet, verbose)

    cfg_dict['Miscellanea']['askpass'] = askpass
    cfg_dict['Miscellanea']['confirm'] = confirm
    cfg_dict['Miscellanea']['timeout'] = config['Miscellanea'].getint('timeout', None)

    return dict(cfg_dict)
