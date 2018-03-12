#!/bin/bash


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1


################################################################################
# Log packages installed through Homebrew.

# Parameter list:
#   1. Log Name
#   2. Daemon Flag
################################################################################


# parameter assignment
logfile=$1
arg_d=$2


# log current status
echo "+ /bin/bash $0 $@" >> $logfile


# if daemon flag set
if ( $arg_d ) ; then
    daemon="&"
else
    daemon=""
fi


# find packages
echo -e "++ brew list | sed \"s/^/INF: /\" $daemon" >> $logfile
brew list | sed "s/^/INF: /" $daemon >> $logfile 2> /dev/null
echo >> $logfile


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1
