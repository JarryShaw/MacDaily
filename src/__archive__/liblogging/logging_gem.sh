#!/bin/bash


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1


################################################################################
# Log Ruby gems.

# Parameter list:
#   1. Log Name
################################################################################


# parameter assignment
# echo $1 | cut -c2- | rev | cut -c2- | rev
logfile=`python -c "print(__import__('sys').stdin.readline().strip().strip('\''))" <<< $1`


# log current status
echo "+ /bin/bash $0 $@" >> "$logfile"


# find apps
echo -e "++ gem list | sed \"s/\(.*\)* (.*)/INF: \1/\"" >> "$logfile"
gem list 2>/dev/null | sed "s/\(.*\)* (.*)/INF: \1/" >> "$logfile"
echo >> "$logfile"


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1
