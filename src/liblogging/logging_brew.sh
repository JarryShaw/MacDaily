#!/bin/bash


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1


################################################################################
# Log packages installed through Homebrew.

# Parameter list:
#   1. Log Name
################################################################################


# parameter assignment
logfile=$1
arg_d=$2


# log current status
echo "+ /bin/bash $0 $@" >> $logfile


# find packages
echo -e "++ brew list | sed \"s/^/INF: /\"" >> $logfile
brew list 2> /dev/null | sed "s/^/INF: /" >> $logfile
echo >> $logfile


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1
