# -*- coding: utf-8 -*-
"""terminal display"""

import shutil

# terminal display
reset = '\033[0m'       # reset
bold = '\033[1m'        # bold
under = '\033[4m'       # underline
flash = '\033[5m'       # flash
red = '\033[91m'        # bright red foreground
green = '\033[92m'      # bright green foreground
blue = '\033[96m'       # bright blue foreground
blush = '\033[101m'     # bright red background
purple = '\033[104m'    # bright purple background

# terminal length
length = shutil.get_terminal_size().columns
