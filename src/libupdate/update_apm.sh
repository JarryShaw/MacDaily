#!/bin/bash


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1


# preset terminal output colours
blush="tput setaf 1"    # blush / red
green="tput setaf 2"    # green
reset="tput sgr0"       # reset


################################################################################
# Check Atom updates.
#
# Parameter list:
#   1. Log Date
#   2. Quiet Flag
#   3. Verbose Flag
#   4. Outdated Flag
#   5. Package
#       ............
################################################################################


# parameter assignment
logdate=$1
arg_q=$2
arg_v=$3
arg_o=$4
arg_pkg=${*:5}


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
if ( $arg_q ) ; then
    logsuffix="grep ^$"
else
    logsuffix="grep ^.*$"
fi


# if no outdated packages found
if ( ! $arg_o ) ; then
    $green
    $logprefix echo "All packages have been up-to-date." | $logcattee | $logsuffix
    $reset
else
    # if quiet flag set
    if ( $arg_q ) ; then
        quiet="--quiet"
    else
        quiet=""
    fi

    # if verbose flag set
    if ( $arg_v ) ; then
        verbose="--verbose"
    else
        verbose=""
    fi

    # update procedure
    for name in $arg_pkg ; do
        flag=`apm list --bare --no-color | sed "s/@.*//" | awk "/^$arg_pkg$/"`
        if [[ -nz $flag ]] ; then
            # ask for confirmation
            while true ; do
                read -p "Would you like to install ${name}? (yes)" answer

                # check answer
                case $answer in
                    [yY]*)
                        $logprefix echo "+ apm upgrade $arg_pkg $verbose $quiet" | $logcattee | $logsuffix
                        $logprefix apm upgrade $arg_pkg $verbose $quiet -y | $logcattee | $logsuffix
                        $logprefix echo | $logcattee | $logsuffix
                        break ;;
                    [nN]*)
                        $blush
                        $logprefix echo "Update procedure for ${name} declined." | $logcattee | $logsuffix
                        $reset
                        break ;;
                    * )
                        echo "Invalid choice." ;;
                esac
            done
        else
            $blush
            $logprefix echo "Error: No Atom package names $arg_pkg installed." | $logcattee | $logsuffix
            $reset

            # did you mean
            dym=`apm list --bare --no-color | sed "s/@.*//" | grep $arg_pkg | xargs | sed "s/ /, /g"`
            if [[ -nz $dym ]] ; then
                $logprefix echo "Did you mean any of the following packages: $dym?" | $logcattee | $logsuffix
            fi
            $logprefix echo | $logcattee | $logsuffix
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
