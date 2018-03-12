#!/bin/bash


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1


################################################################################
# Log applications installed in /Application folder.

# Parameter list:
#   1. Log Name
################################################################################


# parameter assignment
logfile=$1


# log current status
echo "+ /bin/bash $0 $@" >> $logfile


# find apps
echo -e "++ ls /Applications | sed \"s/^/INF: /\" $daemon" >> $logfile
ls /Applications 2> /dev/null | sed "s/^/INF: /" $daemon >> $logfile
echo >> $logfile


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1
