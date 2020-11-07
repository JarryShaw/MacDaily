# -*- coding: utf-8 -*-
"""terminal display"""

import shutil

# terminal length
length = shutil.get_terminal_size().columns

# ANSI colours
reset = '\033[0m'           # reset
bold = '\033[1m'            # bold
dim = '\033[2m'             # dim
under = '\033[4m'           # underline
flash = '\033[5m'           # flash

red_dim = '\033[31m'        # dim red foreground
green_dim = '\033[32m'      # dim green foreground
yellow_dim = '\033[33m'     # dim yellow foreground
purple_dim = '\033[34m'     # dim purple foreground
pink_dim = '\033[35m'       # dim pink foreground
blue_dim = '\033[36m'       # dim blue foreground

red_bg_dim = '\033[41m'     # dim red background
green_bg_dim = '\033[42m'   # dim green background
yellow_bg_dim = '\033[43m'  # dim yellow background
purple_bg_dim = '\033[44m'  # dim purple background
pink_bg_dim = '\033[45m'    # dim pink background
blue_bg_dim = '\033[46m'    # dim blue background

grey = '\033[90m'           # bright grey foreground
red = '\033[91m'            # bright red foreground
green = '\033[92m'          # bright green foreground
yellow = '\033[93m'         # bright yellow foreground
purple = '\033[94m'         # bright purple foreground
pink = '\033[95m'           # bright pink foreground
blue = '\033[96m'           # bright blue foreground

grey_bg = '\033[100m'       # bright grey background
red_bg = '\033[101m'        # bright red background
green_bg = '\033[102m'      # bright green background
yellow_bg = '\033[103m'     # bright yellow background
purple_bg = '\033[104m'     # bright purple background
pink_bg = '\033[105m'       # bright pink background
blue_bg = '\033[106m'       # bright blue background
