#!/bin/bash


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1


################################################################################
# Log node modules.

# Parameter list:
#   1. Log Name
################################################################################


# parameter assignment
# echo $1 | cut -c2- | rev | cut -c2- | rev
logfile=`python -c "print(__import__('sys').stdin.readline().strip().strip('\''))" <<< $1`


# log current status
echo "+ /bin/bash $0 $@" >> "$logfile"


# find apps
echo -e "++ npm list --global --depth=0 2> /dev/null | grep '@' | cut -c 5- | sed \"s/\(.*\)*@.*/^INF: \1/\"" >> "$logfile"
npm list --global --depth=0 2> /dev/null | grep '@' | cut -c 5- | sed "s/\(.*\)*@.*/^INF: \1/" >> "$logfile"
echo >> "$logfile"


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1
