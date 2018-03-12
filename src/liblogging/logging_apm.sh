#!/bin/bash


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1


################################################################################
# Log packages installed through apm.

# Parameter list:
#   1. Log Name
################################################################################


# parameter assignment
logfile=$1


# log current status
echo "+ /bin/bash $0 $@" >> $logfile


# find packages
echo -e "++ apm list --bare | sed \"s/\(.*\)*@.*/INF: \1/\"" >> $logfile
apm list --bare 2> /dev/null | sed "s/\(.*\)*@.*/INF: \1/" >> $logfile
echo >> $logfile


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1
