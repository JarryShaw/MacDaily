# -*- coding: utf-8 -*-

import collections
import configparser
import contextlib
import datetime
import os
import re
import shlex
import sys

from macdaily.cmd.launch import launch_askpass, launch_confirm, launch_daemons
from macdaily.util.const import ROOT, bold, purple, reset, under
from macdaily.util.error import ConfigNotFoundError
from macdaily.util.misc import (get_pass, print_misc, print_term, print_wrap,
                                run_script)

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
          '[Miscellaneous]',
          '# In this section, miscellaneous specifications are assigned.',
          '# Please, under any circumstances, make sure all fields are valid.',
          'askpass = ...                                               ; SUDO_ASKPASS utility for Homebrew Casks',
          'confirm = ...                                               ; confirm utility for MacDaily',
          'limit   = 1000                                              ; timeout limit for shell scripts in seconds',
          'retry   = 60                                                ; retry timeout for input prompts in seconds',
          '']


def get_config():
    config = configparser.ConfigParser(allow_no_value=True,
                                       inline_comment_prefixes=(';',),
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

    # Miscellaneous section
    askpass = os.path.realpath(config['Miscellaneous']['askpass'])
    if not os.access(askpass, os.X_OK):
        askpass = os.path.join(ROOT, 'res', 'askpass.applescript')
        run_script(['sudo', 'chmod', '+x', askpass], quiet, verbose)

    confirm = os.path.realpath(config['Miscellaneous']['confirm'])
    if not os.access(confirm, os.X_OK):
        confirm = os.path.join(ROOT, 'res', 'confirm.applescript')
        run_script(['sudo', 'chmod', '+x', confirm], quiet, verbose)

    limit = config['Miscellaneous'].getint('limit', 1000)
    retry = config['Miscellaneous'].getint('retry', 60)

    cfg_dict['Miscellaneous']['askpass'] = askpass
    cfg_dict['Miscellaneous']['confirm'] = confirm
    cfg_dict['Miscellaneous']['limit'] = limit
    cfg_dict['Miscellaneous']['retry'] = retry

    # set up environment variables
    os.environ['TIMEOUT'] = str(retry)
    os.environ['SSH_ASKPASS'] = askpass
    os.environ['SUDO_ASKPASS'] = askpass

    return dict(cfg_dict)


def make_config(quiet=False, verbose=False):
    if not sys.stdin.isatty():
        raise OSError(5, 'Input/output error')

    print_wrap('Entering interactive command line setup procedure...'.format())
    print_wrap('Default settings are shown as in the square brackets.'.format())
    print_wrap('Please directly {}{}ENTER{} if you prefer the default settings.'.format(bold, under, reset))

    rcpath = os.path.expanduser('~/.dailyrc')
    try:
        with open(rcpath, 'w') as config_file:
            config_file.writelines(map(lambda s: '{}{}'.format(s, os.linesep), CONFIG[:4]))
            print()
            print_wrap('For logging utilities, we recommend you to set up your {}hard disk{} path.'.format(bold, reset))
            print_wrap('You may change other path preferences in configuration `{}~/.dailyrc{}` later.'.format(under, reset))
            print_wrap('Please note that all paths must be valid under all circumstances.'.format())
            dskdir = input('Name of your external hard disk []: ').ljust(41)
            config_file.write('dskdir = /Volumes/{} ; path where your hard disk lies\n'.format(dskdir))

            config_file.writelines(map(lambda s: '{}{}'.format(s, os.linesep), CONFIG[5:38]))
            print()
            print_wrap('In default, we will run {}update{} and {}logging{} commands twice a day.'.format(bold, reset, bold, reset))
            print_wrap('You may change daily commands preferences in configuration `{}~/.dailyrc{}` later.'.format(under, reset))
            print_wrap('Please enter schedule as {}{}HH:MM-CMD{} format, '
                       'and each separates with {}comma{}.'.format(bold, under, reset, under, reset))
            timing = input('Time for daily scripts [8:00,22:30-update,23:00-logging]: ')
            if timing:
                config_file.writelines(['\t', '\n\t'.join(map(lambda s: s.strip(), timing.split(','))), '\n'])
            else:
                config_file.writelines(map(lambda s: '{}{}'.format(s, os.linesep), CONFIG[38:41]))

            config_file.writelines(map(lambda s: '{}{}'.format(s, os.linesep), CONFIG[41:51]))
            print()
            print_wrap('For better stability, {}MacDaily{} depends on several helper programs.'.format(bold, reset))
            print_wrap('Your password may be necessary during the launch process.')
            askpass = launch_askpass(quiet=quiet, verbose=verbose)
            confirm = launch_confirm(quiet=quiet, verbose=verbose)

            config_file.write('askpass = {} ; SUDO_ASKPASS utility for Homebrew Casks\n'.format(askpass.ljust(49)))
            config_file.write('confirm = {} ; confirm utility for MacDaily\n'.format(confirm.ljust(49)))
            print()
            print_wrap('Also, {}MacDaily{} supports several different environment setups.'.format(bold, reset))
            print_wrap('You may set up these variables here, '
                       'or later manually in configuration `{}~/.dailyrc{}`.'.format(under, reset))
            print_wrap('Please enter these specifications as instructed below.'.format())
            shtout = (input('Timeout limit for shell scripts in seconds [1,000]: ') or '1000').ljust(49)
            config_file.write('limit = {} ; timeout limit for shell scripts in seconds\n'.format(shtout))
            retout = (input('Retry timeout for input prompts in seconds [60]:') or '60').ljust(49)
            config_file.write('retry = {} ; retry timeout for input prompts in seconds\n'.format(retout))
            print()
            print_wrap('Configuration for {}MacDaily{} finished. Now launching...\n'.format(bold, reset))
    except BaseException:
        os.remove(rcpath)
        print(reset)
        raise

    # parse config
    config = parse_config(quiet, verbose)
    askpass = config['Miscellaneous']['askpass']

    # ask for password
    text = '{}{}|🔑|{} {}Your {}sudo{}{} password may be necessary{}'.format(bold, purple, reset, bold, under, reset, bold, reset)
    print_term(text, os.devnull, redirect=quiet)
    password = get_pass(askpass)

    # launch daemons
    path = launch_daemons(config, password, quiet, verbose)
    text = 'Launched helper program {}daemons{}{} at {}{}{}'.format(under, reset, bold, under, path, reset)
    print_misc(text, os.devnull, redirect=quiet)
