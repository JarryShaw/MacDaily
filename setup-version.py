# -*- coding: utf-8 -*-

import os
import re

with open(os.path.join(os.path.dirname(__file__), 'macdaily/util/const.py')) as file:
    for line in file:
        match = re.match(r"__version__ = '(.*)'", line)
        if match is None:
            continue
        __version__ = match.groups()[0]
        break

context = list()
with open(os.path.join(os.path.dirname(__file__), 'setup.py')) as file:
    for line in file:
        match = re.match(r"__version__ = '(.*)'", line)
        if match is None:
            context.append(line)
        else:
            context.append(f'__version__ = {__version__!r}\n')

with open(os.path.join(os.path.dirname(__file__), 'setup.py'), 'w') as file:
    file.writelines(context)

for rst in os.listdir(os.path.join(os.path.dirname(__file__), 'contrib')):
    if os.path.splitext(rst)[1] != '.rst':
        continue

    context = list()
    with open(os.path.join(os.path.dirname(__file__), 'contrib', rst)) as file:
        for line in file:
            match = re.match(r":Version: (.*)", line)
            if match is None:
                context.append(line)
            else:
                context.append(f':Version: {__version__}\n')

    with open(os.path.join(os.path.dirname(__file__), 'contrib', rst), 'w') as file:
        file.writelines(context)
