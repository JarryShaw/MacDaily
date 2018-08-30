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

from macdaily.daily_utility import make_pipe


__all__ = ['parse', 'config', 'launch']


# terminal display
reset  = '\033[0m'      # reset
bold   = '\033[1m'      # bold
under  = '\033[4m'      # underline
red    = '\033[91m'     # bright red foreground
green  = '\033[92m'     # bright green foreground
length = shutil.get_terminal_size().columns
                        # terminal length


# user name
USER = getpass.getuser()


# wrapped print
printw = lambda string: print('\n'.join(textwrap.wrap(string, length)))


# mode list
MODES = {'update', 'uninstall', 'reinstall', 'postinstall', 'dependency', 'logging'}


# AppleScript
scpt = lambda mode, argv: f"""\
#!/usr/bin/osascript

-- show notification
display notification "Daily scheduled script `{mode}` running..." with title "macdaily"

-- run script
do shell script "{sys.executable} -m macdaily {mode} {argv}"
"""


# Property List
plist = collections.OrderedDict(
    Label = '',
    UserName = USER,
    Program = '/usr/bin/osascript',
    ProgramArguments = ['/usr/bin/osascript', '-e', ''],
    RunAtLoad = True,
    RootDirectory = str(pathlib.Path.home()),
    EnvironmentVariables = dict(os.environ),
    StartCalendarInterval = [],
    StandardOutPath = '',
    StandardErrorPath = '',
)


# default config
CONFIG = """\
[Path]
# In this section, paths for log files are specified.
# Please, under any circumstances, make sure they are valid.
logdir = ~/Library/Logs/MacDaily    ; path where logs will be stored
tmpdir = /tmp/dailylog              ; path where temporary runtime logs go
dskdir = /Volumes/Your Disk         ; path where your hard disk lies
arcdir = ${dskdir}/Developers       ; path where ancient logs archive

[Mode]
# In this section, flags for modes are configured.
# If you would like to disable the mode, set it to "false".
apm      = true     ; Atom packages
gem      = true     ; Ruby gems
mas      = true     ; Mac App Store applications
npm      = true     ; Node.js modules
pip      = true     ; Python packages
brew     = true     ; Homebrew Cellars
cask     = true     ; Caskroom Casks
dotapp   = true     ; Applications (*.app)
macapp   = true     ; all applications in /Application folder
system   = true     ; macOS system packages
cleanup  = true     ; cleanup caches
appstore = true     ; Mac App Store applications in /Application folder

[Daemon]
# In this section, scheduled tasks are set up.
# You may append and/or remove the time intervals.
update      = true      ; run update on schedule
uninstall   = false     ; don't run uninstall
reinstall   = false     ; don't run reinstall
postinstall = false     ; don't run postinstall
dependency  = false     ; don't run dependency
logging     = true      ; run logging on schedule
schedule    =           ; scheduled timing (in 24 hours)
    8:00                ; update & logging at 8:00
    22:30-update        ; update at 22:30
    23:00-logging       ; logging at 23:00

[Option]
# In this section, command options are picked.
# Do make sure these options are available for commands.
update  = --all --yes --pre --quiet --restart --show-log
logging = --all --quiet --show-log

[Account]
# In this section, account information are stored.
# You must not modify this part under any circumstances.
"""


class StringIO(io.StringIO):
    def readlines(self, hint=-1):
        if hint >= 0:
            lines = list()
            for _ in range(hint):
                lines.append(super().readline())
            return lines
        return super().readlines()


def get_config():
    config = configparser.ConfigParser(
        inline_comment_prefixes=(';',),
        interpolation=configparser.ExtendedInterpolation())
    config.SECTCRE = re.compile(r'\[\s*(?P<header>[^]]+?)\s*\]')
    config.read_string(CONFIG)
    return config


def loads(rcpath):
    config = get_config()
    try:
        with open(rcpath, 'r') as config_file:
            config.read_file(config_file)
    except configparser.Error as error:
        sys.tracebacklimit = 0
        raise error from None
    return config


def dumps(rcpath):
    global CONFIG
    try:
        PASS = base64.b85encode(getpass.getpass().encode()).decode()
        CONFIG += f'username = {USER}\npassword = {PASS}\n'
        with open(rcpath, 'w') as config_file:
            config_file.write(CONFIG)
    except BaseException as error:
        sys.tracebacklimit = 0
        raise error from None
    return get_config()


def parse():
    rcpath = pathlib.Path('~/.dailyrc').expanduser()
    if rcpath.exists() and rcpath.is_file():
        return loads(rcpath)
    return dumps(rcpath)


def launch(config):
    PIPE = make_pipe(config)
    cfgmode = dict()
    try:
        for mode in MODES:
            ldpath = pathlib.Path(f'/Library/LaunchDaemons/com.macdaily.{mode}.{USER}.plist')
            if ldpath.exists() and ldpath.is_file():
                subprocess.run(['sudo', '--stdin', 'launchctl', 'unload', '-w', ldpath], stdin=PIPE.stdout, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                subprocess.run(['sudo', '--stdin', 'rm', '-f', ldpath], stdin=PIPE.stdout, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            cfgmode[mode] = config['Daemon'].getboolean(mode)
    except BaseException as error:
        sys.tracebacklimit = 0
        raise error from None

    pltmode = collections.defaultdict(list)
    try:
        timing = config['Daemon']['schedule'].strip().split('\n')
        for line in timing:
            if not line:    continue
            temp = re.split(r'\s*-\s*', line)
            time, mode = temp if len(temp) == 2 else (temp[0], 'any')
            ptime = datetime.datetime.strptime(time, '%H:%M')
            if mode == 'any':
                for tmpmode, boolean in cfgmode.items():
                    if boolean: pltmode[tmpmode].append(dict(Hour=ptime.hour, Minute=ptime.minute))
            elif mode in MODES:
                pltmode[mode].append(dict(Hour=ptime.hour, Minute=ptime.minute))
            else:
                raise NameError(f'unrecognised mode {mode}')
    except BaseException as error:
        sys.tracebacklimit = 0
        raise error from None

    print()
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
        subprocess.run(['sudo', '--stdin', 'mv', tmpath, ldpath], stdin=PIPE.stdout, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(['sudo', '--stdin', 'chown', 'root', ldpath], stdin=PIPE.stdout, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(['sudo', '--stdin', 'launchctl', 'load', '-w', ldpath], stdin=PIPE.stdout, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f'macdaily: {green}launch{reset}: new scheduled service for {bold}{mode}{reset} loaded')
    if not pltmode:
        print(f'macdaily: {red}launch{reset}: no scheduled services loaded')


def config():
    config = StringIO(CONFIG)
    printw(f'Entering interactive command line setup procedure...')
    printw(f'Default settings are shown as in the square brackets.')
    printw(f'Please directly {bold}{under}ENTER{reset} if you prefer the default settings.')

    rcpath = pathlib.Path('~/.dailyrc').expanduser()
    try:
        with open(rcpath, 'w') as config_file:
            config_file.writelines(config.readlines(5));    config.readline();  print()
            printw(f'For logging utilities, we recommend you to set up your {bold}hard disk{reset} path.')
            printw(f'You may change other path preferences in configuration `{under}~/.dailyrc{reset}` later.')
            printw(f'Please note that all paths must be valid under all circumstances.')
            dskdir = input('Name of your external hard disk []: ').ljust(17)
            config_file.write(f'dskdir = /Volumes/{dskdir} ; path where your hard disk lies\n')

            config_file.writelines(config.readlines(28));   print()
            printw(f'In default, we will run {bold}update{reset} and {bold}logging{reset} commands twice a day.')
            printw(f'You may change daily commands preferences in configuration `{under}~/.dailyrc{reset}` later.')
            printw(f'Please enter schedule as {bold}{under}HH:MM-CMD{reset} format, and each separates with {under}comma{reset}.')
            timing = (input('Time for daily scripts [8:00,22:30-update,23:00-logging]: ') or '8:00,22:30-update,23:00-logging').split(',')
            config_file.write('\t' + '\n\t'.join(map(lambda s: s.strip(), timing)) + '\n')

            config.readlines(3);    config_file.writelines(config.readlines()); print()
            printw(f'To make sure the daemons will launch as expected, we will record your account information.')
            printw(f'You {bold}must not{reset} modify the information generated by {under}MacDaily{reset}.')
            printw(f'Please enter your login password, and we will keep it in a safe place.')
            passwd = base64.b85encode(getpass.getpass().encode()).decode()
            config_file.write(f'username = {USER}\npassword = {passwd}\n')
    except BaseException as error:
        sys.tracebacklimit = 0
        raise error from None
    launch(parse())
