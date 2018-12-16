# -*- coding: utf-8 -*-

import collections
import contextlib
import copy
import getpass
import os
import plistlib
import pwd
import shutil
import sys

from macdaily.util.const import ROOT, bold, red, reset, under
from macdaily.util.misc import (make_pipe, make_stderr, print_info, print_misc,
                                print_scpt, print_term, python, run_script)

if sys.version_info[:2] == (3, 4):
    import pathlib2 as pathlib
    import subprocess32 as subprocess
else:
    import pathlib
    import subprocess


def launch_askpass(password=None, quiet=False, verbose=False, logfile=os.devnull, *args, **kwargs):
    text = 'Launching MacDaily SSH-AskPass program'
    print_info(text, logfile, quiet)

    path = f'Macintosh HD{ROOT.replace(os.path.sep, ":")}:img:askpass.icns'
    ASKPASS = ['#!/usr/bin/env osascript',
               '',
               '-- script based on https://github.com/theseal/ssh-askpass',
               '',
               'on run argv',
               '    set args to argv as text',
               '    if args starts with "--help" or args starts with "-h" then',
               '        return "macdaily-askpass [-h|--help] [prompt]"',
               '    end if',
               f'    display dialog args with icon file ("{path}") default button "OK" default answer "" with hidden answer',  # noqa
               "    return result's text returned",
               'end run',
               '']
    askpass = os.path.join(ROOT, 'res', 'askpass.applescript')
    text = f'Making executable {askpass!r}'
    print_misc(text, logfile, verbose)

    user = owner = getpass.getuser()
    if os.path.isfile(askpass):
        owner = pwd.getpwuid(os.stat(askpass).st_uid).pw_name
        if user != owner:
            run_script(['chown', user, askpass], quiet, verbose,
                       sudo=True, password=password, logfile=logfile)
    else:
        try:
            pathlib.Path(askpass).touch()
        except PermissionError:
            owner = 'root'
            run_script(['touch', askpass], quiet, verbose,
                       sudo=True, password=password, logfile=logfile)
            run_script(['chown', user, askpass], quiet, verbose,
                       sudo=True, password=password, logfile=logfile)

    with open(askpass, 'w') as file:
        file.write(os.linesep.join(ASKPASS))
    run_script(['chmod', '+x', askpass], quiet, verbose,
               sudo=True, password=password, logfile=logfile)
    if user != owner:
        run_script(['chown', owner, askpass], quiet, verbose,
                   sudo=True, password=password, logfile=logfile)

    PLIST = collections.OrderedDict(
        Label='com.macdaily.askpass',
        ProgramArguments=['/usr/bin/ssh-agent', '-l'],
        EnvironmentVariables=collections.OrderedDict(
            SSH_ASKPASS=askpass,
            DISPLAY=0,
        ),
        Sockets=collections.OrderedDict(
            Listeners=collections.OrderedDict(
                SecureSocketWithKey='SSH_AUTH_SOCK'
            )
        ),
        EnableTransactions=True,
    )
    plist = os.path.expanduser('~/Library/LaunchAgents/com.macdaily.askpass.plist')
    text = f'Adding Launch Agent {plist!r}'
    print_misc(text, logfile, verbose)
    if os.path.exists(plist):
        run_script(['launchctl', 'unload', '-w', plist], quiet, verbose, logfile=logfile)
    with open(plist, 'wb') as file:
        plistlib.dump(PLIST, file, sort_keys=False)
    run_script(['launchctl', 'load', '-w', plist], quiet, verbose, logfile=logfile)
    with contextlib.suppress(subprocess.CalledProcessError):
        run_script(['ssh-add', '-c'], quiet, verbose, logfile=logfile)

    return askpass


def launch_confirm(password=None, quiet=False, verbose=False, logfile=os.devnull, *args, **kwargs):
    text = 'Launching MacDaily Confirmation program'
    print_info(text, logfile, quiet)

    path = f'Macintosh HD{ROOT.replace(os.path.sep, ":")}:img:confirm.icns'
    ASKPASS = ['#!/usr/bin/env osascript',
               '',
               'on run argv',
               '    set args to argv as text',
               '    if args starts with "--help" or args starts with "-h" then',
               '        return "macdaily-confirm [-h|--help] [prompt]"',
               '    end if',
               f'    display dialog args with icon file ("{path}") default button "Cancel"',
               "    return result's button returned",
               'end run',
               '']
    confirm = os.path.join(ROOT, 'res', 'confirm.applescript')
    text = f'Making executable {confirm!r}'
    print_misc(text, logfile, verbose)

    user = owner = getpass.getuser()
    if os.path.isfile(confirm):
        owner = pwd.getpwuid(os.stat(confirm).st_uid).pw_name
        if user != owner:
            run_script(['chown', user, confirm], quiet, verbose,
                       sudo=True, password=password, logfile=logfile)
    else:
        try:
            pathlib.Path(confirm).touch()
        except PermissionError:
            owner = 'root'
            run_script(['touch', confirm], quiet, verbose,
                       sudo=True, password=password, logfile=logfile)
            run_script(['chown', user, confirm], quiet, verbose,
                       sudo=True, password=password, logfile=logfile)

    with open(confirm, 'w') as file:
        file.write(os.linesep.join(ASKPASS))
    run_script(['chmod', '+x', confirm], quiet, verbose,
               sudo=True, password=password, logfile=logfile)
    if user != owner:
        run_script(['chown', owner, confirm], quiet, verbose,
                   sudo=True, password=password, logfile=logfile)

    return confirm


def launch_daemons(config, password, quiet=False, verbose=False, logfile=os.devnull):
    text = 'Launching MacDaily LaunchAgent program'
    print_info(text, logfile, quiet)

    def make_daemon(mode, argv):
        DAEMON = ['#!/usr/bin/env osascript',
                  '',
                  '-- show notification',
                  f'display notification "Running scheduled {mode} scripts..." with title "MacDaily"',
                  '',
                  '-- run script',
                  f'do shell script "{python} -m macdaily {mode} {argv}"',
                  '']
        return os.linesep.join(DAEMON)

    # Property List
    osascript = shutil.which('osascript')
    PLIST_BASE = collections.OrderedDict(
        Label=str(),
        UserName=getpass.getuser(),
        Program=osascript,
        ProgramArguments=[osascript, ''],
        # RunAtLoad=True,
        RootDirectory=str(pathlib.Path.home()),
        EnvironmentVariables=dict(os.environ),
        StartCalendarInterval=list(),
        StandardOutPath=str(),
        StandardErrorPath=str(),
    )

    root = pathlib.Path(config['Path']['logdir'])
    for mode, time in config['Daemon'].items():
        (root / mode).mkdir(parents=True, exist_ok=True)

        name = f'com.macdaily.{mode}'
        path = os.path.join(ROOT, 'res', f'daemon-{mode}.applescript')
        pout = str(root / mode / 'stdout.log')
        perr = str(root / mode / 'stderr.log')
        argv = ' '.join(config['Command'].get(mode)) or '--help'

        text = f'Adding {under}{mode}{reset}{bold} command LaunchAgent {name!r}'
        print_misc(text, logfile, quiet)

        user = owner = getpass.getuser()
        if os.path.isfile(path):
            owner = pwd.getpwuid(os.stat(path).st_uid).pw_name
            if user != owner:
                run_script(['chown', user, path], quiet, verbose,
                           sudo=True, password=password, logfile=logfile)
        else:
            try:
                pathlib.Path(path).touch()
            except PermissionError:
                owner = 'root'
                run_script(['touch', path], quiet, verbose,
                           sudo=True, password=password, logfile=logfile)
                run_script(['chown', user, path], quiet, verbose,
                           sudo=True, password=password, logfile=logfile)

        with open(path, 'w') as file:
            file.write(make_daemon(mode, argv))
        run_script(['chmod', '+x', path], quiet, verbose,
                   sudo=True, password=password, logfile=logfile)
        if user != owner:
            run_script(['chown', owner, path], quiet, verbose,
                       sudo=True, password=password, logfile=logfile)

        PLIST = copy.copy(PLIST_BASE)
        PLIST['Label'] = name
        PLIST['ProgramArguments'][1] = path
        PLIST['StartCalendarInterval'] = time
        PLIST['StandardOutPath'] = pout
        PLIST['StandardErrorPath'] = perr

        plist = os.path.expanduser(f'~/Library/LaunchAgents/{name}.plist')
        text = f'Adding Launch Agent {name!r}'
        print_misc(text, logfile, verbose)
        if os.path.exists(plist):
            run_script(['launchctl', 'unload', '-w', plist], quiet, verbose, logfile=logfile)
        with open(plist, 'wb') as file:
            plistlib.dump(PLIST, file, sort_keys=False)
        run_script(['launchctl', 'load', '-w', plist], quiet, verbose, logfile=logfile)

    return os.path.expanduser('~/Library/LaunchAgents/')
