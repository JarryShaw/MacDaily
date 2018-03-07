#!/bin/bash


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1


################################################################################
# Log Caskroom packages updates.
#
# Parameter List
#   1. Log Date
#   2. Greedy Flag
################################################################################


# parameter assignment
logdate=$1
arg_g=$2


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
logprefix="script -q /dev/null"
logcattee="tee -a $tmpfile"
logsuffix="grep ^.*$"


# if greedy flag set
if ( $arg_g ) ; then
    echo -e "+ brew cask outdated --quiet --greedy" >> $tmpfile
    $logprefix brew cask outdated --quiet --greedy | $logcattee | $logsuffix
    echo >> $tmpfile
else
    # check for oudated packages "
    list=`brew cask list -1`
    for cask in $list ; do
        version=$(brew cask info $cask | sed -n "s/$cask:\ \(.*\)/\1/p")
        installed=$(find "/usr/local/Caskroom/$cask" -type d -maxdepth 1 -maxdepth 1 -name "$version")
        if [[ -z $installed ]] ; then
            $logprefix brew cask info $cask | grep "$cask: " | sed "s/\(.*\)*: .*/\1/" | $logcattee | $logsuffix
        fi
    done
fi


# read /tmp/log/update.log line by line then migrate to log file
while read -r line ; do
    # plus `+` proceeds in line
    if [[ $line =~ ^(\+\+*\ )(.*)$ ]] ; then
        # add "+" in the beginning, then write to /Library/Logs/Scripts/update/logdate.log
        echo "+$line" >> $logfile
    # minus `-` proceeds in line
    elif [[ $line =~ ^(-\ )(.*)$ ]] ; then
        # replace "-" with "+", then write to /Library/Logs/Scripts/update/logdate.log
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
        # write to /Library/Logs/Scripts/update/logdate.log
        echo "$prefix: $suffix" >> $logfile
    # colourised `[??m` line
    elif [[ $line =~ ^(.*)(\[[0-9][0-9]*m)(.*)$ ]] ; then
        # error (red/[31m) line
        if [[ $line =~ ^(.*)(\[31m)(.*)$ ]] ; then
            # add `ERR` tag and remove special characters then write to /Library/Logs/Scripts/update/logdate.log
            echo "ERR: $line" | sed "s/\[[0-9][0-9]*m//g" >> $logfile
        # warning (yellow/[33m)
        elif [[ $line =~ ^(.*)(\[33m)(.*)$ ]] ; then
            # add `WAR` tag and remove special characters then write to /Library/Logs/Scripts/update/logdate.log
            echo "WAR: $line" | sed "s/\[[0-9][0-9]*m//g" >> $logfile
        # other colourised line
        else
            # add `INF` tag and remove special characters then write to /Library/Logs/Scripts/update/logdate.log
            echo "INF: $line" | sed "s/\[[0-9][0-9]*m//g" >> $logfile
        fi
    # empty / blank line
    elif [[ $line =~ ^([[:space:]]*)$ ]] ; then
        # directlywrite to /Library/Logs/Scripts/update/logdate.log
        echo $line >> $logfile
    # non-empty line
    else
        # add `OUT` tag, remove special characters and discard flushed lines then write to /Library/Logs/Scripts/update/logdate.log
        echo "OUT: $line" | sed "s/\[\?[0-9][0-9]*[a-zA-Z]//g" | sed "/\[[A-Z]/d" | sed "/##*\ \ *.*%/d" >> $logfile
    fi
done < $tmpfile


# remove /tmp/log/update.log
rm -f $tmpfile


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1
