# -*- coding: utf-8 -*-

import contextlib
import os
import re
import shlex
import sys

from macdaily.util.const.term import blue, bold, dim, grey, length, purple, reset, under


def print_environ(file=sys.stdout, value_only=False, no_term=False,
                  prefix='  - ', suffix=' {}({}value{}{}: %s){}'.format(grey, under, reset, grey, reset)):
    if no_term:
        bold = green = reset = ''  # pylint: disable=redefined-outer-name
    else:
        from macdaily.util.const.term import bold, green, reset  # pylint: disable=reimported

    with contextlib.redirect_stdout(file):
        if not value_only:
            print('The following environment variables can be set, to do various things:')
            print()

        def print_value(environ, default=None):
            env = os.getenv(environ, default)
            if env is None:
                value = 'null'
            else:
                value = shlex.quote(env)
            print('{}{}{}{}{}'.format(prefix, bold, environ, reset, suffix) % value)

        print_value('SUDO_PASSWORD')
        print_value('NULL_PASSWORD', 'false')
        print_value('MACDAILY_NO_CHECK', 'false')
        print_value('MACDAILY_NO_CONFIG', 'false')
        print_value('MACDAILY_LOGDIR', '~/Library/Logs/MacDaily')
        print_value('MACDAILY_DSKDIR')
        print_value('MACDAILY_ARCDIR', '${MACDAILY_DSKDIR}/Developers')
        print_value('MACDAILY_LIMIT', '1,000')
        print_value('MACDAILY_RETRY', '60')
        print_value('MACDAILY_CLEANUP', 'true')
        print_value('MACDAILY_APM', 'true')
        print_value('MACDAILY_APP', 'true')
        print_value('MACDAILY_BREW', 'true')
        print_value('MACDAILY_CASK', 'true')
        print_value('MACDAILY_GEM', 'true')
        print_value('MACDAILY_MAS', 'true')
        print_value('MACDAILY_NPM', 'true')
        print_value('MACDAILY_PIP', 'true')
        print_value('MACDAILY_SYSTEM', 'true')
        print_value('MACDAILY_TAP', 'true')
        print_value('MACDAILY_DEVMODE', 'false')

        if not value_only:
            print()
            print('You can learn more at:')
            print('  {}{}https://github.com/JarryShaw/MacDaily#environment{}'.format(green, under, reset))


def print_info(text, file, redirect=False):
    flag = text.endswith(os.linesep)
    if not redirect:
        end = str() if flag else os.linesep
        print_wrap('{}{}|💼|{} {}{}{}'.format(bold, blue, reset, bold, text, reset), end=end)
    with open(file, 'a') as fd:
        context = re.sub(r'(\033\[[0-9][0-9;]*m)|(\^D\x08\x08)', r'',
                         (text if flag else '{}{}'.format(text, os.linesep)), flags=re.IGNORECASE)
        fd.write('|💼| {}'.format(context))


def print_misc(text, file, redirect=False):
    flag = text.endswith(os.linesep)
    if not redirect:
        end = str() if flag else os.linesep
        print_wrap('{}{}|📌|{} {}{}{}'.format(bold, grey, reset, bold, text, reset), end=end)
    with open(file, 'a') as fd:
        context = re.sub(r'(\033\[[0-9][0-9;]*m)|(\^D\x08\x08)', r'',
                         (text if flag else '{}{}'.format(text, os.linesep)), flags=re.IGNORECASE)
        fd.write('|📌| {}'.format(context))


def print_scpt(text, file, redirect=False):
    if not isinstance(text, str):
        text = ' '.join(text)
    flag = text.endswith(os.linesep)
    if not redirect:
        end = str() if flag else os.linesep
        print_wrap('{}{}|📜|{} {}{}{}'.format(bold, purple, reset, bold, text, reset), end=end)
    with open(file, 'a') as fd:
        context = re.sub(r'(\033\[[0-9][0-9;]*m)|(\^D\x08\x08)', r'',
                         (text if flag else '{}{}'.format(text, os.linesep)), flags=re.IGNORECASE)
        fd.write('|📜| {}'.format(context))


def print_term(text, file, redirect=False):
    flag = text.endswith(os.linesep)
    if not redirect:
        end = str() if flag else os.linesep
        print_wrap(text, end=end)
    with open(file, 'a') as fd:
        context = re.sub(r'(\033\[[0-9][0-9;]*m)|(\^D\x08\x08)', r'',
                         (text if flag else '{}{}'.format(text, os.linesep)), flags=re.IGNORECASE)
        fd.write(context)


def print_text(text, file, redirect=False):
    flag = text.endswith(os.linesep)
    if not redirect:
        end = str() if flag else os.linesep
        print_wrap('{}{}{}'.format(dim, text, reset), end=end)
    with open(file, 'a') as fd:
        context = re.sub(r'(\033\[[0-9][0-9;]*m)|(\^D\x08\x08)', r'',
                         (text if flag else '{}{}'.format(text, os.linesep)), flags=re.IGNORECASE)
        fd.write(context)


def print_wrap(text, length=length, **kwargs):  # pylint: disable=redefined-outer-name
    print(wrap_text(text, length), **kwargs)


def wrap_text(string, length=length):  # pylint: disable=redefined-outer-name,unused-argument
    # text = '\n'.join(textwrap.wrap(string, length))
    # if string.endswith(os.linesep):
    #     return f'{text}{os.linesep}'
    # return text
    return string
