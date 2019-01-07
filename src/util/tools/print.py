# -*- coding: utf-8 -*-

import os
import re

from macdaily.util.const.term import (blue, bold, dim, grey, length, purple,
                                      reset)


def print_info(text, file, redirect=False):
    flag = text.endswith(os.linesep)
    if not redirect:
        end = str() if flag else os.linesep
        print_wrap(f'{bold}{blue}|💼|{reset} {bold}{text}{reset}', end=end)
    with open(file, 'a') as fd:
        context = re.sub(r'(\033\[[0-9][0-9;]*m)|(\^D\x08\x08)', r'',
                         (text if flag else f'{text}{os.linesep}'), flags=re.IGNORECASE)
        fd.write(f'|💼| {context}')


def print_misc(text, file, redirect=False):
    flag = text.endswith(os.linesep)
    if not redirect:
        end = str() if flag else os.linesep
        print_wrap(f'{bold}{grey}|📌|{reset} {bold}{text}{reset}', end=end)
    with open(file, 'a') as fd:
        context = re.sub(r'(\033\[[0-9][0-9;]*m)|(\^D\x08\x08)', r'',
                         (text if flag else f'{text}{os.linesep}'), flags=re.IGNORECASE)
        fd.write(f'|📌| {context}')


def print_scpt(text, file, redirect=False):
    if not isinstance(text, str):
        text = ' '.join(text)
    flag = text.endswith(os.linesep)
    if not redirect:
        end = str() if flag else os.linesep
        print_wrap(f'{bold}{purple}|📜|{reset} {bold}{text}{reset}', end=end)
    with open(file, 'a') as fd:
        context = re.sub(r'(\033\[[0-9][0-9;]*m)|(\^D\x08\x08)', r'',
                         (text if flag else f'{text}{os.linesep}'), flags=re.IGNORECASE)
        fd.write(f'|📜| {context}')


def print_term(text, file, redirect=False):
    flag = text.endswith(os.linesep)
    if not redirect:
        end = str() if flag else os.linesep
        print_wrap(text, end=end)
    with open(file, 'a') as fd:
        context = re.sub(r'(\033\[[0-9][0-9;]*m)|(\^D\x08\x08)', r'',
                         (text if flag else f'{text}{os.linesep}'), flags=re.IGNORECASE)
        fd.write(context)


def print_text(text, file, redirect=False):
    flag = text.endswith(os.linesep)
    if not redirect:
        end = str() if flag else os.linesep
        print_wrap(f'{dim}{text}{reset}', end=end)
    with open(file, 'a') as fd:
        context = re.sub(r'(\033\[[0-9][0-9;]*m)|(\^D\x08\x08)', r'',
                         (text if flag else f'{text}{os.linesep}'), flags=re.IGNORECASE)
        fd.write(context)


def print_wrap(text, length=length, **kwargs):
    print(wrap_text(text, length), **kwargs)


def wrap_text(string, length=length):
    # text = '\n'.join(textwrap.wrap(string, length))
    # if string.endswith(os.linesep):
    #     return f'{text}{os.linesep}'
    # return text
    return string
