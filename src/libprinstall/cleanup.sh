#!/bin/bash


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1


################################################################################
# Clean up caches.
#
# Parameter List:
#   1. Log Date
#   2. Log Mode
#   3. Homebrew Flag
#   4. Caskroom Flag
#   5. Quiet Flag
################################################################################


# parameter assignment
logdate=$1
logmode=$2
arg_brew=$3
arg_cask=$4
arg_q=$5
# arg_v=$6


# log file prepare
logfile="/Library/Logs/Scripts/$logmode/$logdate.log"
tmpfile="/tmp/log/$logmode.log"


# remove /tmp/log/logmode.log
rm -f $tmpfile


# create /tmp/log/logmode.log & /Library/Logs/Scripts/logmode/logdate.log
touch $logfile
touch $tmpfile


# log current status
echo "- /bin/bash $0 $@" >> $tmpfile


# log commands
logprefix="script -q /dev/null"
logcattee="tee -a $tmpfile"
if ( $arg_q ) ; then
    logsuffix="grep ^$"
else
    logsuffix="grep ^.*$"
fi


# if quiet flag set
if ( $arg_q ) ; then
    quiet="--quiet"
    cmd_q="-q"
else
    quiet=""
    cmd_q=""
fi


# # if verbose flag not set
# if ( $arg_v ) ; then
#     verbose="--verbose"
#     # cmd_v="-v"
# else
#     verbose=""
#     # cmd_v=""
# fi


# brew prune
$logprefix echo "+ brew prune --verbose $quiet" | $logcattee | $logsuffix
$logprefix brew prune --verbose $quiet | $logcattee | $logsuffix
$logprefix echo | $logcattee | $logsuffix


# archive caches if hard disk attached
if [ -e /Volumes/Jarry\ Shaw/ ] ; then
    # check if cache directory exists
    if [ -e $(brew --cache) ] ; then
        # move caches
        $logprefix echo "+ cp -rf -v cache archive $quiet" | $logcattee | $logsuffix
        $logprefix cp -rf -v $(brew --cache) /Volumes/Jarry\ Shaw/Developers/ | $logcattee | $logsuffix
        $logprefix echo | $logcattee | $logsuffix
    fi

    # if cask flag set
    if ( $arg_cask ) ; then
        $logprefix echo "+ brew cask cleanup --verbose $quiet" | $logcattee | $logsuffix
        $logprefix brew cask cleanup --verbose | $logcattee | $logsuffix
        $logprefix echo | $logcattee | $logsuffix
    fi

    # if brew flag set
    if ( $arg_brew ) ; then
        $logprefix echo "+ brew cleanup --verbose $quiet" | $logcattee | $logsuffix
        $logprefix rm -rf -v $( brew --cache ) | $logcattee | $logsuffix
        $logprefix echo | $logcattee | $logsuffix
    fi
fi


while read -r line ; do
    # plus `+` proceeds in line
    if [[ $line =~ ^(\+\+*\ )(.*)$ ]] ; then
        # add "+" in the beginning, then write to /Library/Logs/Scripts/logmode/logdate.log
        echo "+$line" >> $logfile
    # minus `-` proceeds in line
    elif [[ $line =~ ^(-\ )(.*)$ ]] ; then
        # replace "-" with "+", then write to /Library/Logs/Scripts/logmode/logdate.log
        echo "$line" | sed "y/-/+/" >> $logfile
    # colon `:` in line
    elif [[ $line =~ ^([[:alnum:]][[:alnum:]]*)(:)(.*)$ ]] ; then
        # if this is a warning
        if [[ $( tr "[:upper:]" "[:lower:]" <<< $line ) =~ ^([[:alnum:]][[:alnum:]]*:\ )(.*)(warning:\ )(.*) ]] ; then
            # log tag
            prefix="WAR"
            # log content
            suffix=`echo $line | sed "s/\[[0-9][0-9]*m//g" | sed "s/warning: //"`
        # if this is an error
        elif [[ $( tr "[:upper:]" "[:lower:]" <<< $line ) =~ ^([[:alnum:]][[:alnum:]]*:\ )(.*)(error:\ )(.*)$ ]] ; then
            # log tag
            prefix="ERR"
            # log content
            suffix=`echo $line | sed "s/\[[0-9][0-9]*m//g" | sed "s/error: //"`
        # if this is asking for password
        elif [[ $line =~ ^(Password:)(.*) ]] ; then
            # log tag
            prefix="PWD"
            # log content
            suffix="content hidden due to security reasons"
        # otherwise, extract its own tag
        else
            # log tag
            prefix=`echo $line | sed "s/\[[0-9][0-9]*m//g" | sed "s/\(.*\)*:\ .*/\1/" | cut -c 1-3 | tr "[:lower:]" "[:upper:]"`
            # log content
            suffix=`echo $line | sed "s/\[[0-9][0-9]*m//g" | sed "s/.*:\ \(.*\)*.*/\1/"`
        fi
        # write to /Library/Logs/Scripts/logmode/logdate.log
        echo "$prefix: $suffix" >> $logfile
    # colourised `[??m` line
    elif [[ $line =~ ^(.*)(\[[0-9][0-9]*m)(.*)$ ]] ; then
        # error (red/[31m) line
        if [[ $line =~ ^(.*)(\[31m)(.*)$ ]] ; then
            # add `ERR` tag and remove special characters then write to /Library/Logs/Scripts/logmode/logdate.log
            echo "ERR: $line" | sed "s/\[[0-9][0-9]*m//g" >> $logfile
        # warning (yellow/[33m)
        elif [[ $line =~ ^(.*)(\[33m)(.*)$ ]] ; then
            # add `WAR` tag and remove special characters then write to /Library/Logs/Scripts/logmode/logdate.log
            echo "WAR: $line" | sed "s/\[[0-9][0-9]*m//g" >> $logfile
        # other colourised line
        else
            # add `INF` tag and remove special characters then write to /Library/Logs/Scripts/logmode/logdate.log
            echo "INF: $line" | sed "s/\[[0-9][0-9]*m//g" >> $logfile
        fi
    # empty / blank line
    elif [[ $line =~ ^([[:space:]]*)$ ]] ; then
        # directlywrite to /Library/Logs/Scripts/logmode/logdate.log
        echo $line >> $logfile
    # non-empty line
    else
        # add `OUT` tag, remove special characters and discard flushed lines then write to /Library/Logs/Scripts/logmode/logdate.log
        echo "OUT: $line" | sed "s/\[\?[0-9][0-9]*[a-zA-Z]//g" | sed "/\[[A-Z]/d" | sed "/##*\ \ *.*%/d" >> $logfile
    fi
done < $tmpfile


# remove /tmp/log/logmode.log
rm -f $tmpfile


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1
