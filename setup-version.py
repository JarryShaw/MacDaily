# -*- coding: utf-8 -*-

import os
import re
import sys
import time
import pkg_resources

try:
    __version__ = str(pkg_resources.parse_version(sys.argv[1]))
except IndexError:
    __version__ = str(pkg_resources.parse_version(time.strftime('%Y.%m.%d')))

context = list()
with open(os.path.join(os.path.dirname(__file__), 'macdaily/util/const/macro.py')) as file:
    for line in file:
        match = re.match(r"VERSION = '(.*)'", line)
        if match is None:
            context.append(line)
        else:
            context.append(f"VERSION = {__version__!r}\n")

with open(os.path.join(os.path.dirname(__file__), 'macdaily/util/const/macro.py'), 'w') as file:
    file.writelines(context)

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
                match =re.match(r":Date: (.*)", line)
                if match is None:
                    context.append(line)
                else:
                    context.append(f":Date: {time.strftime('%B %d, %Y')}\n")
            else:
                context.append(f':Version: v{__version__}\n')

    with open(os.path.join(os.path.dirname(__file__), 'contrib', rst), 'w') as file:
        file.writelines(context)
