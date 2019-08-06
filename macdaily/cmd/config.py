# -*- coding: utf-8 -*-

import collections
import configparser
import contextlib
import datetime
import getpass
import os
import pwd
import re
import shlex
import sys

from macdaily.cmd.launch import launch_askpass, launch_confirm, launch_daemons
from macdaily.util.const.macro import ROOT, USER
from macdaily.util.const.term import bold, purple, reset, under
from macdaily.util.error import ConfigNotFoundError
from macdaily.util.tools.get import get_boolean, get_int, get_logfile, get_pass, get_path
from macdaily.util.tools.misc import run_script
from macdaily.util.tools.print import print_info, print_misc, print_term, print_wrap

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
          'archive     = true                                          ; archive logs',
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
          '    10:00-update                                            ; update at 10:00',
          '    22:00-logging                                           ; logging at 22:00',
          '    23:00-archive                                           ; archive at 23:00',
          '',
          '[Command]',
          '# In this section, command options are picked.',
          '# Do make sure these options are available for commands.',
          'archive = --all --quiet',
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
    print_info('Creating a config file (.dailyrc) for {}...'.format(USER), get_logfile(), redirect=quiet)

    dskdir = input('Name of your external hard disk []: ')
    CONFIG[4] = 'dskdir = /Volumes/{} ; path where your hard disk lies'.format(dskdir.ljust(41))

    askpass = launch_askpass(quiet=quiet, verbose=verbose)
    confirm = launch_confirm(quiet=quiet, verbose=verbose)

    CONFIG[52] = 'askpass = {} ; SUDO_ASKPASS utility for Homebrew Casks'.format(askpass.ljust(49))
    CONFIG[53] = 'confirm = {} ; confirm utility for MacDaily'.format(confirm.ljust(49))

    with open(rcpath, 'w') as file:
        file.write(os.linesep.join(CONFIG))
    return get_config()


def load_config(rcpath):
    config = get_config()
    with open(rcpath) as file:
        config.read_file(file)
    return config


def parse_config(quiet=False, verbose=False):
    if get_boolean('MACDAILY_NO_CONFIG'):
        config = get_config()
    else:
        rcpath = os.path.expanduser('~/.dailyrc')
        if os.path.isfile(rcpath):
            config = load_config(rcpath)
        else:
            config = dump_config(rcpath, quiet, verbose)
    cfg_dict = collections.defaultdict(dict)

    # Path section
    for name, path in config['Path'].items():
        cfg_dict['Path'][name] = get_path('MACDAILY_{}'.format(name.upper()), path)

    # Mode section
    for mode in config['Mode'].keys():
        cfg_dict['Mode'][mode] = get_boolean('MACDAILY_{}'.format(mode.upper()),
                                             config['Mode'].getboolean(mode, False))

    # Daemon section
    daemon_list = list()
    for command in {'archive', 'bundle', 'cleanup', 'config', 'dependency', 'launch',
                    'logging', 'postinstall', 'reinstall', 'uninstall', 'update'}:
        if config['Daemon'].getboolean(command, False):
            daemon_list.append(command)

    daemon_dict = collections.defaultdict(list)
    for daemon in config['Daemon']['schedule'].strip().splitlines():
        union = re.split(r'\s*-\s*', daemon)
        with contextlib.suppress(ValueError):
            time = datetime.datetime.strptime(union[0], r'%H:%M')
            if len(union) == 2:
                daemon_dict[union[1]].append(dict(Hour=time.hour, Minute=time.minute))
            else:
                for command in daemon_list:
                    daemon_dict[command].append(dict(Hour=time.hour, Minute=time.minute))
    cfg_dict['Daemon'].update(dict(daemon_dict))

    # Command section
    for mode, argv in config['Command'].items():
        cfg_dict['Command'][mode] = shlex.split(argv)

    # Miscellaneous section
    # askpass = os.path.realpath(config['Miscellaneous']['askpass'])
    askpass = os.path.join(ROOT, 'res', 'askpass.applescript')
    if not os.access(askpass, os.X_OK):
        user = getpass.getuser()
        owner = pwd.getpwuid(os.stat(askpass).st_uid).pw_name
        if user == owner:
            run_script(['chmod', '+x', askpass], quiet, verbose)
        else:
            run_script(['sudo', 'chmod', '+x', askpass], quiet, verbose)

    # confirm = os.path.realpath(config['Miscellaneous']['confirm'])
    confirm = os.path.join(ROOT, 'res', 'confirm.applescript')
    if not os.access(confirm, os.X_OK):
        user = getpass.getuser()
        owner = pwd.getpwuid(os.stat(confirm).st_uid).pw_name
        if user == owner:
            run_script(['chmod', '+x', confirm], quiet, verbose)
        else:
            run_script(['sudo', 'chmod', '+x', confirm], quiet, verbose)

    limit = get_int('MACDAILY_LIMIT',
                    config['Miscellaneous'].getint('limit', 1000))
    retry = get_int('MACDAILY_RETRY',
                    config['Miscellaneous'].getint('retry', 60))

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
            config_file.writelines(map(lambda s: '{}{}'.format(s, os.linesep), CONFIG[:4]))  # pylint: disable=map-builtin-not-iterating
            print()
            print_wrap('For logging utilities, we recommend you to set up your {}hard disk{} path.'.format(bold, reset))
            print_wrap('You may change other path preferences in configuration `{}~/.dailyrc{}` later.'.format(under, reset))
            print_wrap('Please note that all paths must be valid under all circumstances.'.format())
            dskdir = input('Name of your external hard disk []: ').ljust(41)
            config_file.write('dskdir = /Volumes/{} ; path where your hard disk lies\n'.format(dskdir))

            config_file.writelines(map(lambda s: '{}{}'.format(s, os.linesep), CONFIG[5:38]))  # pylint: disable=map-builtin-not-iterating
            print()
            print_wrap('In default, we will run {}update{} and {}logging{} commands twice a day.'.format(bold, reset, bold, reset))
            print_wrap('You may change daily commands preferences in configuration `{}~/.dailyrc{}` later.'.format(under, reset))
            print_wrap('Please enter schedule as {}{}HH:MM[-CMD]{} format, '
                       'and each separates with {}comma{}.'.format(bold, under, reset, under, reset))
            timing = input('Time for daily scripts [10:00-update,22:30-logging,23:00-archive]: ')
            if timing:
                config_file.writelines(['\t', '\n\t'.join(map(lambda s: s.strip(), timing.split(','))), '\n'])
            else:
                config_file.writelines(map(lambda s: '{}{}'.format(s, os.linesep), CONFIG[38:41]))  # pylint: disable=map-builtin-not-iterating

            config_file.writelines(map(lambda s: '{}{}'.format(s, os.linesep), CONFIG[41:52]))  # pylint: disable=map-builtin-not-iterating
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
    print_term(text, get_logfile(), redirect=quiet)
    password = get_pass(askpass)

    # launch daemons
    path = launch_daemons(config, password, quiet, verbose)
    text = 'Launched helper program {}daemons{}{} at {}{}{}'.format(under, reset, bold, under, path, reset)
    print_misc(text, get_logfile(), redirect=quiet)
