#!/bin/bash


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1


################################################################################
# Log applications installed through Homebrew Caskroom.

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


# find apps
echo -e "++ brew cask list | sed \"s/^/INF: /\" $daemon" >> $logfile
brew cask list | sed "s/^/INF: /" $daemon >> $logfile 2> /dev/null
echo >> $logfile


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1
