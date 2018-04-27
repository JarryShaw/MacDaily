#!/bin/bash


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1


################################################################################
# Log applications installed from Mac App Store.

# Parameter list:
#   1. Log Name
################################################################################


# parameter assignment
# echo $1 | cut -c2- | rev | cut -c2- | rev
logfile=`python -c "print(__import__('sys').stdin.readline().strip().strip('\''))" <<< $1`


# log current status
echo "+ /bin/bash $0 $@" >> "$logfile"


# find apps
echo -e "++ find /Applications -path \"*Contents/_MASReceipt/receipt\" -maxdepth 4 -print | sed \"s#.app/Contents/_MASReceipt/receipt#.app#g; s#/Applications/##\" | sed \"s/^/INF: \1/\"" >> "$logfile"
find /Applications -path "*Contents/_MASReceipt/receipt" -maxdepth 4 -print 2> /dev/null | sed "s#.app/Contents/_MASReceipt/receipt#.app#g; s#/Applications/##" | sed "s/^/INF: /" >> "$logfile"
echo >> "$logfile"


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1
