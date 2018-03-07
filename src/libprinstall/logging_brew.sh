#!/bin/bash


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1


################################################################################
# Log Homebrew packages reinstallation.
#
# Parameter List
#   1. Log Date
#   2. Log Mode
#   3. Start Package
#   4. End Package
#   5. Package
#       ............
################################################################################


# parameter assignment
logdate=$1
logmode=$2
arg_s=$3
arg_e=$4
arg_pkg=${*:5}


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
logsuffix="grep ^.*$"


# if start package set
case $arg_s in
    none)
        # perl -CA -le "print chr shift" 64
        start="@" ;;    # ASCII 64 (A - 65)
    *)
        start=$arg_s ;;
esac


# if end package set
case $arg_e in
    none)
        # perl -CA -le "print chr shift" 123
        end="{" ;;      # ASCII 123 (z - 122)
    *)
        end=$arg_e ;;
esac


# check for reinstalling packages
for name in $arg_pkg ; do
    case $name in
        all)
            list=`brew list -1`
            for pkg in $list ; do
                if [[ $pkg > $start ]] && [[ $pkg < $end ]] ; then
                    echo -e "+ brew desc $pkg | sed -e \"s/\[1m//\" | sed \"s/\(.*\)*:.*/\1/\"" >> $tmpfile
                    $logprefix brew desc $pkg | sed -e "s/\[1m//" | sed "s/\(.*\)*:.*/\1/" | $logcattee | $logsuffix
                    echo >> $tmpfile
                fi
            done ;;
        *)
            # check if package installed
            if brew list --versions $name > /dev/null 2&>1 ; then
                echo -e "+ brew desc $name | sed \"s/\(.*\)*: .*/\1/\"" >> $tmpfile
                $logprefix brew desc $name | sed "s/\(.*\)*: .*/\1/" | $logcattee | $logsuffix
                echo >> $tmpfile
            else
                echo -e "Error: No available formula with the name \"$name\"\n" >> $tmpfile
            fi ;;
    esac
done


# read /tmp/log/logmode.log line by line then migrate to log file
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
