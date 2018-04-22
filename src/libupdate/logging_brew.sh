#!/bin/bash


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1


################################################################################
# Log Homebrew packages updates.
#
# Parameter List
#   1. Log Date
#   2. Log Time
################################################################################


# parameter assignment
logdate=$1
logtime=$2


# log file prepare
logfile="/Library/Logs/Scripts/update/$logdate/$logtime.log"
tmpfile="/tmp/log/update.log"


# remove /tmp/log/update.log
rm -f $tmpfile


# create /tmp/log/update.log & /Library/Logs/Scripts/update/logdate/logtime.log
touch $logfile
touch $tmpfile


# log current status
echo "- /bin/bash $0 $@" >> $tmpfile


# log commands
logprefix="script -aq $tmpfile"
# logsuffix="grep ^.*$"


# check for oudated packages
echo -e "+ brew outdated --quiet" >> $tmpfile
$logprefix brew outdated --quiet
echo >> $tmpfile


# aftermath works
bash ./libupdate/aftermath.sh $logdate $logtime


# remove /tmp/log/update.log
rm -f $tmpfile


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1
