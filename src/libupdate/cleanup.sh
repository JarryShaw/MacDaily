#!/bin/bash


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1


################################################################################
# Clean up caches.
#
# Parameter List:
#   1. Log Date
#   2. Ruby Flag
#   3. Node.js Flag
#   4. Python Flag
#   5. Homebrew Flag
#   6. Caskroom Flag
#   7. Quiet Flag
################################################################################


# parameter assignment
logdate=$1
arg_gem=$2
arg_npm=$3
arg_pip=$4
arg_brew=$5
arg_cask=$6
arg_q=$7
# arg_v=$8


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


# gem cleanup
if ( $arg_gem ) ; then
    if ( $arg_q ) ; then
        $logprefix echo "+ gem cleanup --verbose $quiet" > /dev/null 2>&1
        sudo $logprefix gem cleanup --verbose $quiet > /dev/null 2>&1
        $logprefix echo > /dev/null 2>&1
    else
        $logprefix echo "+ gem cleanup --verbose $quiet"
        sudo $logprefix gem cleanup --verbose $quiet
        $logprefix echo
    fi
fi


# npm dedupe & cache clean
if ( $arg_npm ) ; then
    if ( $arg_q ) ; then
        $logprefix echo "+ npm dedupe --global --verbose $quiet" > /dev/null 2>&1
        sudo $logprefix npm dedupe --global --verbose $quiet > /dev/null 2>&1
        $logprefix echo > /dev/null 2>&1

        $logprefix echo "+ npm cache clean --force --global --verbose $quiet" > /dev/null 2>&1
        sudo $logprefix npm cache clean --force --global --verbose $quiet > /dev/null 2>&1
        $logprefix echo > /dev/null 2>&1
    else
        $logprefix echo "+ npm dedupe --global --verbose $quiet"
        sudo $logprefix npm dedupe --global --verbose $quiet
        $logprefix echo

        $logprefix echo "+ npm cache clean --force --global --verbose $quiet"
        sudo $logprefix npm cache clean --force --global --verbose $quiet
        $logprefix echo
    fi
fi


# pip cleanup
if ( $arg_pip ) ; then
    if ( $arg_q ) ; then
        $logprefix echo "+ pip cleanup --verbose $quiet" > /dev/null 2>&1
        sudo $logprefix rm -rf -v $cmd_q ~/Library/Caches/pip > /dev/null 2>&1
        sudo $logprefix rm -rf -v $cmd_q /var/root/Library/Caches/pip > /dev/null 2>&1
        $logprefix echo > /dev/null 2>&1
    else
        $logprefix echo "+ pip cleanup --verbose $quiet"
        sudo $logprefix rm -rf -v $cmd_q ~/Library/Caches/pip
        sudo $logprefix rm -rf -v $cmd_q /var/root/Library/Caches/pip
        $logprefix echo
    fi
fi


# brew prune
if ( $arg_brew || $arg_cask ) ; then
    if ( $arg_q ) ; then
        $logprefix echo "+ brew prune --verbose $quiet" > /dev/null 2>&1
        $logprefix brew prune --verbose $quiet > /dev/null 2>&1
        $logprefix echo > /dev/null 2>&1
    else
        $logprefix echo "+ brew prune --verbose $quiet"
        $logprefix brew prune --verbose $quiet
        $logprefix echo
    fi
fi


# archive caches if hard disk attached
if [ -e /Volumes/Jarry\ Shaw/ ] ; then
    # check if cache directory exists
    if [ -e $(brew --cache) ] ; then
        # move caches
        if ( $arg_q ) ; then
            $logprefix echo "+ cp -rf -v cache archive $quiet" > /dev/null 2>&1
            $logprefix cp -rf -v $(brew --cache) /Volumes/Jarry\ Shaw/Developers/ > /dev/null 2>&1
            $logprefix echo > /dev/null 2>&1
        else
            $logprefix echo "+ cp -rf -v cache archive $quiet"
            $logprefix cp -rf -v $(brew --cache) /Volumes/Jarry\ Shaw/Developers/
            $logprefix echo
        fi
    fi

    # if cask flag set
    if ( $arg_cask ) ; then
        if ( $arg_q ) ; then
            $logprefix echo "+ brew cask cleanup --verbose $quiet" > /dev/null 2>&1
            $logprefix brew cask cleanup --verbose > /dev/null 2>&1
            $logprefix echo > /dev/null 2>&1
        else
            $logprefix echo "+ brew cask cleanup --verbose $quiet"
            $logprefix brew cask cleanup --verbose
            $logprefix echo
        fi
    fi

    # if brew flag set
    if ( $arg_brew ) ; then
        if ( $arg_q ) ; then
            $logprefix echo "+ brew cleanup --verbose $quiet" > /dev/null 2>&1
            $logprefix rm -rf -v $( brew --cache ) > /dev/null 2>&1
            $logprefix echo > /dev/null 2>&1
        else
            $logprefix echo "+ brew cleanup --verbose $quiet"
            $logprefix rm -rf -v $( brew --cache )
            $logprefix echo
        fi
    fi
fi


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
        # if this is a update logging message
        if [[ $line =~ ^(update: )(.*)$ ]] ; then
            echo "LOG: $line" >> $logfile
        # if this is a warning
        elif [[ $( tr "[:upper:]" "[:lower:]" <<< $line ) =~ ^([[:alnum:]][[:alnum:]]*:\ )(.*)(warning:\ )(.*) ]] ; then
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
