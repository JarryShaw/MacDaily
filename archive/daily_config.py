# -*- coding: utf-8 -*-

import base64
import collections
import configparser
import datetime
import getpass
import io
import os
import plistlib
import re
import shutil
import sys
import textwrap

from macdaily.daily_utility import (ConfigNotFoundError, ModeError, bold,
                                    check, green, length, make_pipe, red,
                                    reset, sudo_timeout, under)

try:
    import pathlib2 as pathlib
except ImportError:
    import pathlib

try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess

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
            f'display notification "Daily scheduled script `{mode}` running..." with title "MacDaily"\n'
            '\n'
            '-- run script\n'
            f'do shell script "{sys.executable} -m macdaily {mode} {argv}"\n')


def get_config():
    config = configparser.ConfigParser(inline_comment_prefixes=(';',),
                                       interpolation=configparser.ExtendedInterpolation())
    config.SECTCRE = re.compile(r'\[\s*(?P<header>[^]]+?)\s*\]')
    config.read_string(''.join(CONFIG))
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

    CONFIG[47] = f'username = {USER}\n'
    CONFIG[48] = f'password = {PASS}\n'
    CONFIG[54] = f'sudo-timeout = {timeout} ; sudo command timeout as specified in /etc/sudoers\n'

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
    def _config_mode():
        cfgmode = dict()
        for mode in MODES:
            ldpath = pathlib.Path(f'/Library/LaunchDaemons/com.macdaily.{mode}.{USER}.plist')
            if ldpath.exists() and ldpath.is_file():
                subprocess.run(['sudo', '--stdin', 'launchctl', 'unload', '-w', ldpath],
                               stdin=PIPE.stdout, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                subprocess.run(['sudo', '--stdin', 'rm', '-f', ldpath],
                               stdin=PIPE.stdout, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            cfgmode[mode] = config['Daemon'].getboolean(mode)
        return cfgmode

    def _plist_mode():
        pltmode = collections.defaultdict(list)
        timing = config['Daemon']['schedule'].strip().split('\n')
        for line in filter(None, timing):
            temp = re.split(r'\s*-\s*', line)
            time, mode = temp if len(temp) == 2 else (temp[0], 'any')
            ptime = datetime.datetime.strptime(time, r'%H:%M')
            if mode == 'any':
                for tmpmode, _ in filter(lambda i: i[1], cfgmode.items()):
                    pltmode[tmpmode].append(dict(Hour=ptime.hour, Minute=ptime.minute))
            elif mode in MODES:
                pltmode[mode].append(dict(Hour=ptime.hour, Minute=ptime.minute))
            else:
                raise ModeError(f'unrecognised mode: {mode!r}')
        return pltmode

    def _launch_daemon():
        if not pltmode:
            print(f'macdaily: {red}launch{reset}: no scheduled services loaded')
            return
        tmpdir = os.path.expanduser(config['Path']['tmpdir'])
        logdir = os.path.expanduser(config['Path']['logdir'])
        pathlib.Path(tmpdir).mkdir(exist_ok=True, parents=True)
        for mode, schedule in pltmode.items():
            tmpath = f'{tmpdir}/com.macdaily.{mode}.{USER}.plist'
            ldpath = f'/Library/LaunchDaemons/com.macdaily.{mode}.{USER}.plist'
            plist['Label'] = f'com.macdaily.{mode}.{USER}.plist'
            plist['ProgramArguments'][2] = scpt(mode, config['Option'].get(mode, ''))
            plist['StartCalendarInterval'] = schedule
            plist['StandardOutPath'] = f'{logdir}/{mode}/stdout.log'
            plist['StandardErrorPath'] = f'{logdir}/{mode}/stderr.log'
            with open(tmpath, 'wb') as plist_file:
                plistlib.dump(plist, plist_file, sort_keys=False)
            subprocess.run(['sudo', '--stdin', 'mv', tmpath, ldpath],
                           stdin=PIPE.stdout, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(['sudo', '--stdin', 'chown', 'root', ldpath],
                           stdin=PIPE.stdout, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(['sudo', '--stdin', 'launchctl', 'load', '-w', ldpath],
                           stdin=PIPE.stdout, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f'macdaily: {green}launch{reset}: new scheduled service for {bold}{mode}{reset} loaded')

    with make_pipe(config) as PIPE:
        cfgmode = _config_mode()
        pltmode = _plist_mode()
        _launch_daemon()


def config():
    printw(f'Entering interactive command line setup procedure...')
    printw(f'Default settings are shown as in the square brackets.')
    printw(f'Please directly {bold}{under}ENTER{reset} if you prefer the default settings.')

    rcpath = pathlib.Path('~/.dailyrc').expanduser()
    try:
        with open(rcpath, 'w') as config_file:
            config_file.writelines(CONFIG[:5])
            print()
            printw(f'For logging utilities, we recommend you to set up your {bold}hard disk{reset} path.')
            printw(f'You may change other path preferences in configuration `{under}~/.dailyrc{reset}` later.')
            printw(f'Please note that all paths must be valid under all circumstances.')
            dskdir = input('Name of your external hard disk []: ').ljust(17)
            config_file.write(f'dskdir = /Volumes/{dskdir} ; path where your hard disk lies\n')

            config_file.writelines(CONFIG[7:34])
            print()
            printw(f'In default, we will run {bold}update{reset} and {bold}logging{reset} commands twice a day.')
            printw(f'You may change daily commands preferences in configuration `{under}~/.dailyrc{reset}` later.')
            printw(f'Please enter schedule as {bold}{under}HH:MM-CMD{reset} format, '
                   f'and each separates with {under}comma{reset}.')
            timing = (input('Time for daily scripts [8:00,22:30-update,23:00-logging]: ')
                      or '8:00,22:30-update,23:00-logging').split(',')
            config_file.writelines(['\t', '\n\t'.join(map(lambda s: s.strip(), timing)), '\n'])

            config_file.writelines(CONFIG[37:47])
            print()
            printw(f'To make sure the daemons will launch as expected, we will record your account information.')
            printw(f'You {bold}must not{reset} modify the information generated by {under}MacDaily{reset}.')
            printw(f'Please enter your login password, and we will keep it in a safe place.')
            passwd = getpass.getpass('Password:')
            PASS = base64.b85encode(passwd.encode()).decode()
            config_file.write(f'username = {USER}\npassword = {PASS}\n')

            config_file.writelines(CONFIG[49:53])
            print()
            printw(f'Also, {under}MacDaily{reset} supports several different environment setups.')
            printw('You may set up these variables here, '
                   f'or later manually in configuration `{under}~/.dailyrc{reset}`.')
            printw(f'Please enter these specifications as instructed below.')
            shtout = (input('Timeout limit for shell scripts in seconds [1,000]: ') or '1000').ljust(8)
            config_file.write(f'bash-timeout = {shtout} ; timeout limit for each shell script in seconds\n')
            config_file.write(f'sudo-timeout = {sudo_timeout(passwd).ljust(8)} '
                              '; sudo command timeout as specified in /etc/sudoers\n')
            print()
            printw(f'Configuration for {under}MacDaily{reset} finished. Now launching...\n')
    except BaseException:
        os.remove(rcpath)
        raise
    launch(parse())


if __name__ == '__main__':
    sys.tracebacklimit = 0
    sys.exit(config())
