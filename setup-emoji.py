# -*- coding: utf-8 -*-

import os
import re
import subprocess

RESP_BEER = subprocess.check_output(['unbuffer', '-p', 'echo', '🍺']).strip().decode()

context = list()
with open(os.path.join(os.path.dirname(__file__), 'macdaily/util/const/macro.py')) as file:
    for line in file:
        match = re.match(r"RESP_BEER = '(.*)'", line)
        if match is None:
            context.append(line)
        else:
            context.append(f'RESP_BEER = {RESP_BEER!r}\n')

with open(os.path.join(os.path.dirname(__file__), 'macdaily/util/const/macro.py'), 'w') as file:
    file.writelines(context)
