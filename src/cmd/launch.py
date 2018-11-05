# -*- coding: utf-8 -*-

import collections
import os
import plistlib

from macdaily.util.const import ROOT, bold, red, reset
from macdaily.util.misc import print_info, print_misc, print_scpt, print_term

try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess


def run_script(argv, quiet, verbose):
    args = ' '.join(argv)
    print_scpt(args, os.devnull, verbose)
    stderr = subprocess.DEVNULL if quiet else None
    try:
        subprocess.check_call(argv, stdout=subprocess.DEVNULL, stderr=stderr)
    except subprocess.CalledProcessError:
        text = f"macdaily: {red}config{reset}: command `{bold}{args!r}{reset} failed"
        print_term(text, os.devnull, quiet)
        raise


def launch_askpass(quiet=False, verbose=False):
    text = 'Launching MacDaily SSH-AskPass program'
    print_info(text, os.devnull, quiet)

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
               f'    display dialog args with icon file ("{path}") default button "OK" default answer "" with hidden answer',
               "    return result's text returned",
               'end run',
               '']
    askpass = os.path.join(ROOT, 'res', 'askpass.applescript')
    text = f'Making executable {askpass!r}'
    print_misc(text, os.devnull, verbose)
    with open(askpass, 'w') as file:
        file.write(os.linesep.join(ASKPASS))
    run_script(['chmod', 'u+x', askpass], quiet, verbose)

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
    print_misc(text, os.devnull, verbose)
    if os.path.exists(plist):
        run_script(['launchctl', 'unload', '-w', plist], quiet, verbose)
    with open(plist, 'wb') as file:
        plistlib.dump(PLIST, file, sort_keys=False)
    run_script(['launchctl', 'load', '-w', plist], quiet, verbose)
    run_script(['ssh-add', '-c'], quiet, verbose)

    return askpass


def launch_confirm(quiet=False, verbose=False):
    text = 'Launching MacDaily Confirmation program'
    print_info(text, os.devnull, quiet)

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
    print_misc(text, os.devnull, verbose)
    with open(confirm, 'w') as file:
        file.write(os.linesep.join(ASKPASS))
    run_script(['chmod', 'u+x', confirm], quiet, verbose)

    return confirm
