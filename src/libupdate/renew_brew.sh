#!/bin/bash


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1


# terminal display
reset="\033[0m"         # reset
bold="\033[1m"          # bold


################################################################################
# Update global Homebrew status.
#
# Parameter list:
#   1. Log Date
#   2. Quiet Flag
#   3. Verbose Flag
#   4. Force Flag
#   5. Merge Flag
################################################################################


# parameter assignment
logdate=$1
arg_q=$2
arg_v=$3
arg_f=$4
arg_m=$5


# log file prepare
logfile="/Library/Logs/Scripts/update/$logdate.log"
tmpfile="/tmp/log/update.log"


# remove /tmp/log/update.log
rm -f $tmpfile


# create /tmp/log/update.log & /Library/Logs/Scripts/update/logdate.log
touch $logfile
touch $tmpfile


# log current status
echo "- /bin/bash $0 $@" >> $tmpfile


# log commands
logprefix="script -aq $tmpfile"
if ( $arg_q ) ; then
    logsuffix="grep ^$"
else
    logsuffix="grep ^.*$"
fi


# if verbose flag set
if ( $arg_v ) ; then
    verbose="--verbose"
else
    verbose=""
fi


# if force flag set
if ( $arg_f ) ; then
    force="--force"
else
    force=""
fi

# if merge flag set
if ( $arg_m ) ; then
    merge="--merge"
else
    merge=""
fi


# renew brew status
$logprefix printf "+ ${bold}brew update $force $merge $verbose${reset}\n" | $logsuffix
if ( $arg_q ) ; then
    $logprefix brew update $force $merge $verbose > /dev/null 2>&1
else
    $logprefix brew update $force $merge $verbose
fi
$logprefix echo | $logsuffix


# aftermath works
bash libupdate/aftermath.sh $logdate


# remove /tmp/log/update.log
rm -f $tmpfile


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1
