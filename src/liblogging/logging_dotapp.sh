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


# find apps
echo -e "++ sudo -H find / ! -path \"/Volumes\" -type d -iname *.app | sed \"s/^/INF: /\"" >> "$logfile"
sudo find / ! -path "/Volumes" -type d -iname *.app 2> /dev/null | sed "s/^/INF: /" >> "$logfile"
echo >> "$logfile"


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1
