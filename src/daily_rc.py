# -*- coding: utf-8 -*-


import collections
import configparser
import datetime
import io
import pathlib
import plistlib
import re
import shlex
import subprocess
import sys


__all__ = ['parse', 'config', 'launch']


# terminal display
reset  = '\033[0m'      # reset
bold   = '\033[1m'      # bold
under  = '\033[4m'      # underline
red    = '\033[91m'     # bright red foreground
green  = '\033[92m'     # bright green foreground


# AppleScript
scpt = lambda mode: f"""\
#!/usr/bin/osascript

display notification "Daily scheduled script `{mode}` running..." with title "jsdaily"
tell application "Terminal"
    activate
    do script "jsdaily {mode} --all"
end tell
"""


# Property List
plist = collections.OrderedDict(
    Label = 'com.jsdaily.launchd.plist',
    RunAtLoad = True,
    Program = '/usr/bin/osascript',
    ProgramArguments = ['/usr/bin/osascript', '-e', ''],
    StartCalendarInterval = [],
    StandardOutPath = '',
    StandardErrorPath = '',
)


# default config
CONFIG = """\
[Path]
# In this section, paths for log files are specified.
# Please, under any circumstances, make sure they are valid.
logdir = /Library/Logs/Scripts      ; path where logs will be stored
tmpdir = /tmp/log                   ; path where temporary runtime logs go
dskdir = /Volumes/Your Disk         ; path where your hard disk lies
arcdir = ${dskdir}/Developers       ; path where ancient logs archive

[Mode]
# In this section, flags for modes are configured.
# If you would like to disable the mode, set it to "false".
apm      = true     ; Atom packages
gem      = true     ; Ruby gems
npm      = true     ; Node.js modules
pip      = true     ; Python packages
brew     = true     ; Homebrew Cellars
cask     = true     ; Caskroom Casks
dotapp   = true     ; Applications (*.app)
macapp   = true     ; applications in /Application folder
cleanup  = true     ; cleanup caches
appstore = true     ; Mac App Store applications

[Setup]
# In this section, scheduled tasks are set up.
# You may append and/or remove the time intervals.
update      = true      ; run update on schedule
uninstall   = false     ; don't run uninstall
reinstall   = false     ; don't run reinstall
postinstall = false     ; don't run postinstall
dependency  = false     ; don't run dependency
logging     = true      ; run logging on schedule
timing  =               ; scheduled timing (in 24 hours)
    8:00
    22:30
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
    config.SECTCRE = re.compile(r"\[ *(?P<header>[^]]+?) *\]")
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
    try:
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
    try:
        logdir = config['Path']['logdir']
        timing = config['Setup']['timing'].split()
        for time in timing:
            ptime = datetime.datetime.strptime(time, '%H:%M')
            plist['StartCalendarInterval'].append(dict(Hour=ptime.hour, Minute=ptime.minute))
    except BaseException as error:
        sys.tracebacklimit = 0
        raise error from None

    flag = False
    for mode in {'update', 'uninstall', 'reinstall', 'postinstall', 'dependency', 'logging'}:
        lapath = pathlib.Path(f'~/Library/LaunchAgents/com.jsdaily.{mode}.plist').expanduser()
        if lapath.exists() and lapath.is_file():
            subprocess.run(shlex.split(f'launchctl unload -w {lapath}'), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if config['Setup'].getboolean(mode):
            flag = True
            plist['ProgramArguments'][2] = scpt(mode)
            plist['StandardOutPath'] = f'{logdir}/{mode}/stdout.log'
            plist['StandardErrorPath'] = f'{logdir}/{mode}/stderr.log'
            with open(lapath, 'wb') as plist_file:
                plistlib.dump(plist, plist_file, sort_keys=False)
            subprocess.run(shlex.split(f'launchctl load -w {lapath}'), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f'jsdaily: {green}launch{reset}: new scheduled service for {bold}{mode}{reset} loaded')
    if not flag:
        print(f'jsdaily: {red}launch{reset}: no scheduled services loaded')


def config():
    cfg = StringIO(CONFIG)
    print(f'Entering interactive command line setup procedure...')
    print(f'Default settings are shown as in the square brackets.')
    print(f'Please directly {bold}{under}ENTER{reset} if you prefer the default settings.')

    rcpath = pathlib.Path('~/.dailyrc').expanduser()
    try:
        with open(rcpath, 'w') as config_file:
            config_file.writelines(cfg.readlines(5))
            cfg.readline()
            print(f'\nFor logging utilities, we recommend you to set up your {bold}hard disk{reset} path.')
            print(f'You may change other path preferences in configuration `{under}~/.dailyrc{reset}` later.')
            print(f'Please note that all paths must be valid under all circumstances.')
            dskdir = input('Name of your hard disk []: ').ljust(17)
            config_file.write(f'dskdir = /Volumes/{dskdir} ; path where your hard disk lies\n')

            config_file.writelines(cfg.readlines(26))
            print(f'\nIn default, we will run {bold}update{reset} and {bold}logging{reset} commands twice a day.')
            print(f'You may change daily commands preferences in configuration `{under}~/.dailyrc{reset}` later.')
            print(f'Please enter time as HH:MM format, and each time seperated with comma.')
            timing = (input('Time for daily scripts [8:00,22:30]: ') or '8:00,22:30').split(',')
            config_file.write('\t' + '\n\t'.join(map(lambda s: s.strip(), timing)) + '\n')
    except BaseException as error:
        sys.tracebacklimit = 0
        raise error from None
    launch(parse())
