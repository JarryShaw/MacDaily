#!/bin/bash


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1


################################################################################
# Move temporary logs into log files.
#
# Parameter List:
#   1. Log File
#   2. Temp File
#   3. Interrupted Flag
################################################################################


# parameter assignment
# echo $1 | cut -c2- | rev | cut -c2- | rev
logfile=`python -c "print(__import__('sys').stdin.readline().strip().strip('\''))" <<< $1`
tmpfile=`python -c "print(__import__('sys').stdin.readline().strip().strip('\''))" <<< $2`
interrupred=$3


# create /tmp/log/dependency.log & /Library/Logs/Scripts/dependency/logdate/logtime.log
touch "$logfile"
touch "$tmpfile"


# check if temporary log exists
if [ -e "$tmpfile" ] ; then
    # read /tmp/log/dependency.log line by line then migrate to log file
    while read -r line ; do
        # remove colourised characters
        line=`sed "s/\[[0-9][;0-9]*m//g" <<< $line`
        # plus `+` proceeds in line
        if [[ $line =~ ^(\+\+*\ )(.*)$ ]] ; then
            # add "+" in the beginning, then write to /Library/Logs/Scripts/dependency/logdate/logtime.log
            echo "+$line" >> "$logfile"
        # minus `-` proceeds in line
        elif [[ $line =~ ^(-\ )(.*)$ ]] ; then
            # replace "-" with "+", then write to /Library/Logs/Scripts/dependency/logdate/logtime.log
            echo "$line" | sed "y/-/+/" >> "$logfile"
        # colon `:` in line
        elif [[ $line =~ ^([[:alnum:]][[:alnum:]]*)(:)(.*)$ ]] ; then
            # if this is a dependency logging message
            if [[ $line =~ ^(dependency: )(.*)$ ]] ; then
                # log tag
                prefix="LOG"
                # log content
                suffix=`echo $line`
            # if this is a warning
            elif [[ $( tr "[:upper:]" "[:lower:]" <<< $line ) =~ ^(.*)(warning:\ )(.*) ]] ; then
                # log tag
                prefix="WAR"
                # log content
                suffix=`echo $line | sed ".*warning: //"`
            # if this is an error
            elif [[ $( tr "[:upper:]" "[:lower:]" <<< $line ) =~ ^(.*)(error:\ )(.*)$ ]] ; then
                # log tag
                prefix="ERR"
                # log content
                suffix=`echo $line | sed "s/.*error: //"`
            # if this is asking for password
            elif [[ $line =~ ^(Password:)(.*) ]] ; then
                # log tag
                prefix="PWD"
                # log content
                suffix="content hidden due to security reasons"
            # otherwise, extract its own tag
            else
                # log tag
                prefix=`echo $line | sed "s/\(.*\)*:\ .*/\1/" | cut -c 1-3 | tr "[:lower:]" "[:upper:]"`
                # log content
                suffix=`echo $line | sed "s/.*:\ \(.*\)*.*/\1/"`
            fi
            # write to /Library/Logs/Scripts/dependency/logdate/logtime.log
            echo "$prefix: $suffix" >> "$logfile"
        # colourised `[??m` line
        elif [[ $line =~ ^(.*)(\[[0-9][;0-9]*m)(.*)$ ]] ; then
            # error (red/[31m) line
            if [[ $line =~ ^(.*)(\[[;0-9]*;*31;*[;0-9]*m)(.*)$ ]] ; then
                # add `ERR` tag and remove special characters then write to /Library/Logs/Scripts/dependency/logdate/logtime.log
                echo "ERR: $line" >> "$logfile"
            # warning (yellow/[[01;33m])
            elif [[ $line =~ ^(.*)(\[[;0-9]*;*33;*[;0-9]*m)(.*)$ ]] ; then
                # add `WAR` tag and remove special characters then write to /Library/Logs/Scripts/dependency/logdate/logtime.log
                echo "WAR: $line" >> "$logfile"
            # other colourised line
            else
                # add `INF` tag and remove special characters then write to /Library/Logs/Scripts/dependency/logdate/logtime.log
                echo "INF: $line" >> "$logfile"
            fi
        # empty / blank line
        elif [[ $line =~ ^([[:space:]]*)$ ]] ; then
            # directly write to /Library/Logs/Scripts/dependency/logdate/logtime.log
            echo $line >> "$logfile"
        # non-empty line
        else
            # add `OUT` tag, remove special characters and discard flushed lines then write to /Library/Logs/Scripts/dependency/logdate/logtime.log
            echo "OUT: $line" | sed "s/\[\?25[lh]//g" | sed "/\[K/d" | sed "/##*\ \ *.*%/d" >> "$logfile"
        fi
    done < "$tmpfile"
fi


# if called after KeyboardInterrupt
if [[ ! -z $interrupred ]] ; then
    echo 'ERR: dependency procedure interrupred' >> "$logfile"
fi


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1
