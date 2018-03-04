#!/bin/bash


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1


# preset terminal output colours
blush="tput setaf 1"    # blush / red
green="tput setaf 2"    # green
reset="tput sgr0"       # reset


################################################################################
# Show dependencies of Homebrew packages.
#
# Parameter list:
#   1. Log Date
#   2. Tree Flag
#   3. Package
#       ............
################################################################################


# parameter assignment
logdate=$1
arg_t=$2
arg_pkg=${*:3}


# log file prepare
logfile="/Library/Logs/Scripts/dependency/$logdate.log"
tmpfile="/tmp/log/dependency.log"


# remove /tmp/log/dependency.log
rm -f $tmpfile


# create /tmp/log/dependency.log & /Library/Logs/Scripts/dependency/logdate.log
touch $logfile
touch $tmpfile


# log current status
echo "- /bin/bash $0 $@" >> $tmpfile


# log commands
# usage: $logprefix [command] | logcattee | logsuffix
logprefix="script -q /dev/null"
logcattee="tee -a $tmpfile"
logsuffix="grep ^.*$"


# if tree flag set
if ( $arg_t ) ; then
    tree="--tree"
else
    tree=""
fi


# show dependencies
for name in $arg_pkg ; do
    case $name in
        all)
            list=`brew leaves`
            for pkg in $list ; do
                $logprefix echo "+ brew deps $pkg $tree" | $logcattee | $logsuffix
                $logprefix brew deps $pkg $tree | $logcattee | $logsuffix
                $logprefix echo | $logcattee | $logsuffix
            done ;;
        *)
            # check if package installed
            if brew list --versions $name > /dev/null ; then
                # along with dependencies or not
                $logprefix echo "+ brew deps $name $tree" | $logcattee | $logsuffix
                $logprefix brew deps $name $tree | $logcattee | $logsuffix
                $logprefix echo | $logcattee | $logsuffix
            else
                $blush
                $logprefix echo "Error: No available formula with the name $name." | $logcattee | $logsuffix
                $reset

                # did you mean
                dym=`brew list -1 | grep $name | xargs | sed "s/ /, /g"`
                if [[ -nz $dym ]] ; then
                    $logprefix echo "Did you mean any of the following packages: $dym?" | $logcattee | $logsuffix
                fi
                $logprefix echo | $logcattee | $logsuffix
            fi ;;
    esac
done


# read /tmp/log/dependency.log line by line then migrate to log file
while read -r line ; do
    # plus `+` proceeds in line
    if [[ $line =~ ^(\+\+*\ )(.*)$ ]] ; then
        # add "+" in the beginning, then write to /Library/Logs/Scripts/dependency/logdate.log
        echo "+$line" >> $logfile
    # minus `-` proceeds in line
    elif [[ $line =~ ^(-\ )(.*)$ ]] ; then
        # replace "-" with "+", then write to /Library/Logs/Scripts/dependency/logdate.log
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
        # write to /Library/Logs/Scripts/dependency/logdate.log
        echo "$prefix: $suffix" >> $logfile
    # colourised `[??m` line
    elif [[ $line =~ ^(.*)(\[[0-9][0-9]*m)(.*)$ ]] ; then
        # error (red/[31m) line
        if [[ $line =~ ^(.*)(\[31m)(.*)$ ]] ; then
            # add `ERR` tag and remove special characters then write to /Library/Logs/Scripts/dependency/logdate.log
            echo "ERR: $line" | sed "s/\[[0-9][0-9]*m//g" >> $logfile
        # warning (yellow/[33m)
        elif [[ $line =~ ^(.*)(\[33m)(.*)$ ]] ; then
            # add `WAR` tag and remove special characters then write to /Library/Logs/Scripts/dependency/logdate.log
            echo "WAR: $line" | sed "s/\[[0-9][0-9]*m//g" >> $logfile
        # other colourised line
        else
            # add `INF` tag and remove special characters then write to /Library/Logs/Scripts/dependency/logdate.log
            echo "INF: $line" | sed "s/\[[0-9][0-9]*m//g" >> $logfile
        fi
    # empty / blank line
    elif [[ $line =~ ^([[:space:]]*)$ ]] ; then
        # directlywrite to /Library/Logs/Scripts/dependency/logdate.log
        echo $line >> $logfile
    # non-empty line
    else
        # add `OUT` tag, remove special characters and discard flushed lines then write to /Library/Logs/Scripts/dependency/logdate.log
        echo "OUT: $line" | sed "s/\[\?[0-9][0-9]*[a-zA-Z]//g" | sed "/\[[A-Z]/d" | sed "/##*\ \ *.*%/d" >> $logfile
    fi
done < $tmpfile


# remove /tmp/log/dependency.log
rm -f $tmpfile


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1
