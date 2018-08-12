#!/bin/bash


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1


################################################################################
# Log all applications (*.app) installed on this Mac.

# Parameter list:
#   1. Log Name
################################################################################


# parameter assignment
# echo $1 | cut -c2- | rev | cut -c2- | rev
logfile=`python -c "print(__import__('sys').stdin.readline().strip().strip('\''))" <<< $1`


# log current status
echo "+ /bin/bash $0 $@" >> "$logfile"


# safely find function usage:
#   find_ng path
function find_ng {
    # assign parameters
    local path=$1

    # # log function call
    # echo "+++ find_ng $@" >> "$logfile"

    # # create subprocess
    # (
    #     # walk directory
    #     list=`ls -AF $path 2>/dev/null`
    #     for item in $list ; do
    #         temp="$path$item"
    #         # recursive DFS
    #         if [ -L "$temp" ] ; then
    #             continue
    #         elif [ -d "$temp" ] ; then
    #             if [[ "$temp" =~ ^(/Volumes)(.*)$ ]] ; then
    #                 continue
    #             elif [[ "$temp" =~ ^(.*)(\.app)(/)$ ]] ; then
    #                 echo "$temp" | rev | cut -c 2- | rev
    #             fi
    #             find_ng "$temp"
    #         fi
    #     done
    # )

    # run python script
    sudo --user root --set-home python << EOF
from __future__ import print_function
import os, re

def find(root):
    temp = os.listdir(root)
    for file in temp:
        path = os.path.join(root, file)
        if os.path.islink(path):
            continue
        if os.path.isdir(path):
            match = re.match('^/Volumes', path)
            if match is None:
                if os.path.splitext(path)[1] == '.app':
                    print(path)
                find(path)

find('$path')
EOF
}


# find apps
echo -e "++ sudo find_ng / | sed \"s/^/INF: /\"" >> "$logfile"
# sudo find / ! -path "/Volumes" -type d -iname *.app 2> /dev/null | sed "s/^/INF: /" >> "$logfile"
find_ng / 2>/dev/null | sed "s/^/INF: /" >> "$logfile"
echo >> "$logfile"


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1
