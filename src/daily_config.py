# -*- coding: utf-8 -*-

import base64
import collections
import configparser
import datetime
import getpass
import io
import os
import pathlib
import plistlib
import re
import shutil
import subprocess
import sys
import textwrap

from macdaily.daily_utility import (ConfigNotFoundError, ModeError, bold,
                                    check, green, length, make_pipe, red,
                                    reset, sudo_timeout, under)

# user name
USER = getpass.getuser()

# mode list
MODES = {'update', 'uninstall', 'reinstall', 'postinstall', 'dependency', 'logging'}

# default config
CONFIG = ['[Path]\n',
          '# In this section, paths for log files are specified.\n',
          '# Please, under any circumstances, make sure they are valid.\n',
          'logdir = ~/Library/Logs/MacDaily    ; path where logs will be stored\n',
          'tmpdir = /tmp/dailylog              ; path where temporary runtime logs go\n',
          'dskdir = /Volumes/Your Disk         ; path where your hard disk lies\n',
          'arcdir = ${dskdir}/Developers       ; path where ancient logs archive\n',
          '\n',
          '[Mode]\n',
          '# In this section, flags for modes are configured.\n',
          '# If you would like to disable the mode, set it to "false".\n',
          'apm      = true     ; Atom packages\n',
          'gem      = true     ; Ruby gems\n',
          'mas      = true     ; Mac App Store applications\n',
          'npm      = true     ; Node.js modules\n',
          'pip      = true     ; Python packages\n',
          'brew     = true     ; Homebrew Cellars\n',
          'cask     = true     ; Caskroom Casks\n',
          'dotapp   = true     ; Applications (*.app)\n',
          'macapp   = true     ; all applications in /Application folder\n',
          'system   = true     ; macOS system packages\n',
          'cleanup  = true     ; cleanup caches\n',
          'appstore = true     ; Mac App Store applications in /Application folder\n',
          '\n',
          '[Daemon]\n',
          '# In this section, scheduled tasks are set up.\n',
          '# You may append and/or remove the time intervals.\n',
          'update      = true      ; run update on schedule\n',
          "uninstall   = false     ; don't run uninstall\n",
          "reinstall   = false     ; don't run reinstall\n",
          "postinstall = false     ; don't run postinstall\n",
          "dependency  = false     ; don't run dependency\n",
          'logging     = true      ; run logging on schedule\n',
          'schedule    =           ; scheduled timing (in 24 hours)\n',
          '    8:00                ; update & logging at 8:00\n',
          '    22:30-update        ; update at 22:30\n',
          '    23:00-logging       ; logging at 23:00\n',
          '\n',
          '[Option]\n',
          '# In this section, command options are picked.\n',
          '# Do make sure these options are available for commands.\n',
          'update  = --all --yes --pre --quiet --show-log --no-cask\n',
          'logging = --all --quiet --show-log\n',
          '\n',
          '[Account]\n',
          '# In this section, account information are stored.\n',
          '# You must not modify this part under any circumstances.\n',
          'username = ...\n',
          'password = ********\n',
          '\n',
          '[Environment]\n',
          '# In this section, environment specifications are set up.\n',
          '# Please, under any circumstances, make sure all fields are valid.\n',
          'bash-timeout = 1_000    ; timeout limit for each shell script in seconds\n',
          'sudo-timeout = 5m       ; sudo command timeout as specified in '
          '/etc/sudoers\n']

# Property List
plist = collections.OrderedDict(
    Label='',
    UserName=USER,
    Program='/usr/bin/osascript',
    ProgramArguments=['/usr/bin/osascript', '-e', ''],
    # RunAtLoad=True,
    RootDirectory=str(pathlib.Path.home()),
    EnvironmentVariables=dict(os.environ),
    StartCalendarInterval=[],
    StandardOutPath='',
    StandardErrorPath='',
)


def printw(string):
    """Wrapped print."""
    print('\n'.join(textwrap.wrap(string, length)))


def scpt(mode, argv):
    """AppleScript"""
    return ('#!/usr/bin/osascript\n'
            '\n'
            '-- show notification\n'
            'display notification "Daily scheduled script `{}` running..." with title "MacDaily"\n'
            '\n'
            '-- run script\n'
            'do shell script "{} -m macdaily {} {}"\n'.format(mode, sys.executable, mode, argv))


def get_config():
    config = configparser.ConfigParser(inline_comment_prefixes=(';',),
                                       interpolation=configparser.ExtendedInterpolation())
    config.SECTCRE = re.compile(r'\[\s*(?P<header>[^]]+?)\s*\]')
    config.read_string(CONFIG)
    return config


def loads(rcpath):
    config = get_config()
    with open(rcpath, 'r') as config_file:
        config.read_file(config_file)
    return config


def dumps(rcpath):
    if not sys.stdin.isatty():
        raise ConfigNotFoundError(2, 'No such file or directory', rcpath)

    password = getpass.getpass('Password:')
    timeout = sudo_timeout(password).rjust(8)
    PASS = base64.b85encode(password.encode()).decode()

    CONFIG[47] = 'username = {}\n'.format(USER)
    CONFIG[48] = 'password = {}\n'.format(PASS)
    CONFIG[54] = 'sudo-timeout = {} ; sudo command timeout as specified in /etc/sudoers\n'.format(timeout)

    with open(rcpath, 'w') as config_file:
        config_file.writelines(CONFIG)
    return get_config()


@check
def parse():
    rcpath = pathlib.Path('~/.dailyrc').expanduser()
    if rcpath.exists() and rcpath.is_file():
        return loads(rcpath)
    return dumps(rcpath)


def launch(config):
    PIPE = make_pipe(config)
    cfgmode = dict()
    for mode in MODES:
        ldpath = pathlib.Path('/Library/LaunchDaemons/com.macdaily.{}.{}.plist'.format(mode, USER))
        if ldpath.exists() and ldpath.is_file():
            subprocess.run(['sudo', '--stdin', 'launchctl', 'unload', '-w', ldpath],
                           stdin=PIPE.stdout, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(['sudo', '--stdin', 'rm', '-f', ldpath],
                           stdin=PIPE.stdout, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        cfgmode[mode] = config['Daemon'].getboolean(mode)

    pltmode = collections.defaultdict(list)
    timing = config['Daemon']['schedule'].strip().split('\n')
    for line in filter(None, timing):
        temp = re.split(r'\s*-\s*', line)
        time, mode = temp if len(temp) == 2 else (temp[0], 'any')
        ptime = datetime.datetime.strptime(time, r'%H:%M')
        if mode == 'any':
            for tmpmode, _ in filter(lambda _, b: b, cfgmode.items()):
                pltmode[tmpmode].append(dict(Hour=ptime.hour, Minute=ptime.minute))
        elif mode in MODES:
            pltmode[mode].append(dict(Hour=ptime.hour, Minute=ptime.minute))
        else:
            raise ModeError('unrecognised mode: {!r}'.format(mode))

    tmpdir = os.path.expanduser(config['Path']['tmpdir'])
    logdir = os.path.expanduser(config['Path']['logdir'])
    pathlib.Path(tmpdir).mkdir(exist_ok=True, parents=True)
    for mode, schedule in pltmode.items():
        tmpath = '{}/com.macdaily.{}.{}.plist'.format(tmpdir, mode, USER)
        ldpath = '/Library/LaunchDaemons/com.macdaily.{}.{}.plist'.format(mode, USER)
        plist['Label'] = 'com.macdaily.{}.{}.plist'.format(mode, USER)
        plist['ProgramArguments'][2] = scpt(mode, config['Option'].get(mode, ''))
        plist['StartCalendarInterval'] = schedule
        plist['StandardOutPath'] = '{}/{}/stdout.log'.format(logdir, mode)
        plist['StandardErrorPath'] = '{}/{}/stderr.log'.format(logdir, mode)
        with open(tmpath, 'wb') as plist_file:
            plistlib.dump(plist, plist_file, sort_keys=False)
        subprocess.run(['sudo', '--stdin', 'mv', tmpath, ldpath],
                       stdin=PIPE.stdout, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(['sudo', '--stdin', 'chown', 'root', ldpath],
                       stdin=PIPE.stdout, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(['sudo', '--stdin', 'launchctl', 'load', '-w', ldpath],
                       stdin=PIPE.stdout, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print('macdaily: {}launch{}: new scheduled service for {}{}{} loaded'.format(green, reset, bold, mode, reset))
    if not pltmode:
        print('macdaily: {}launch{}: no scheduled services loaded'.format(red, reset))


def config():
    printw('Entering interactive command line setup procedure...'.format())
    printw('Default settings are shown as in the square brackets.'.format())
    printw('Please directly {}{}ENTER{} if you prefer the default settings.'.format(bold, under, reset))

    rcpath = pathlib.Path('~/.dailyrc').expanduser()
    try:
        with open(rcpath, 'w') as config_file:
            config_file.writelines(CONFIG[:5])
            print()
            printw('For logging utilities, we recommend you to set up your {}hard disk{} path.'.format(bold, reset))
            printw('You may change other path preferences in configuration `{}~/.dailyrc{}` later.'.format(under, reset))
            printw('Please note that all paths must be valid under all circumstances.'.format())
            dskdir = input('Name of your external hard disk []: ').ljust(17)
            config_file.write('dskdir = /Volumes/{} ; path where your hard disk lies\n'.format(dskdir))

            config_file.writelines(CONFIG[7:34])
            print()
            printw('In default, we will run {}update{} and {}logging{} commands twice a day.'.format(bold, reset, bold, reset))
            printw('You may change daily commands preferences in configuration `{}~/.dailyrc{}` later.'.format(under, reset))
            printw('Please enter schedule as {}{}HH:MM-CMD{} format, '
                   'and each separates with {}comma{}.'.format(bold, under, reset, under, reset))
            timing = (input('Time for daily scripts [8:00,22:30-update,23:00-logging]: ')
                      or '8:00,22:30-update,23:00-logging').split(',')
            config_file.writelines(['\t', '\n\t'.join(map(lambda s: s.strip(), timing)), '\n'])

            config_file.writelines(CONFIG[37:47])
            print()
            printw('To make sure the daemons will launch as expected, we will record your account information.'.format())
            printw('You {}must not{} modify the information generated by {}MacDaily{}.'.format(bold, reset, under, reset))
            printw('Please enter your login password, and we will keep it in a safe place.'.format())
            passwd = getpass.getpass('Password:')
            PASS = base64.b85encode(passwd.encode()).decode()
            config_file.write('username = {}\npassword = {}\n'.format(USER, PASS))

            config_file.writelines(CONFIG[49:53])
            print()
            printw('Also, {}MacDaily{} supports several different environment setups.'.format(under, reset))
            printw('You may set up these variables here, '
                   'or later manually in configuration `{}~/.dailyrc{}`.'.format(under, reset))
            printw('Please enter these specifications as instructed below.'.format())
            shtout = (input('Timeout limit for shell scripts in seconds [1,000]: ') or '1000').ljust(8)
            config_file.write('bash-timeout = {} ; timeout limit for each shell script in seconds\n'.format(shtout))
            config_file.write('sudo-timeout = {} '
                              '; sudo command timeout as specified in /etc/sudoers\n'.format(sudo_timeout(passwd).ljust(8)))
            print()
            printw('Configuration for {}MacDaily{} finished. Now launching...\n'.format(under, reset))
    except BaseException:
        os.remove(rcpath)
        raise
    launch(parse())


if __name__ == '__main__':
    sys.tracebacklimit = 0
    sys.exit(config())
