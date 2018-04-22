#!/bin/bash


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1


# terminal display
reset="\033[0m"         # reset
bold="\033[1m"          # bold


################################################################################
# Clean up caches.
#
# Parameter List:
#   1. Log Date
#   2. Log Time
#   3. Ruby Flag
#   4. Node.js Flag
#   5. Python Flag
#   6. Homebrew Flag
#   7. Caskroom Flag
#   8. Quiet Flag
################################################################################


# parameter assignment
logdate=$1
logtime=$2
arg_gem=$3
arg_npm=$4
arg_pip=$5
arg_brew=$6
arg_cask=$7
arg_q=$8
# arg_v=$9


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
    $logprefix printf "+ ${bold}gem cleanup --verbose $quiet${reset}\n" | $logsuffix
    if ( $arg_q ) ; then
        sudo $logprefix gem cleanup --verbose $quiet > /dev/null 2>&1
    else
        sudo $logprefix gem cleanup --verbose $quiet
    fi
    $logprefix echo | $logsuffix
fi


# npm dedupe & cache clean
if ( $arg_npm ) ; then
    $logprefix printf "+ ${bold}npm dedupe --global --verbose $quiet${reset}\n" | $logsuffix
    if ( $arg_q ) ; then
        sudo $logprefix npm dedupe --global --verbose $quiet > /dev/null 2>&1
    else
        sudo $logprefix npm dedupe --global --verbose $quiet
    fi
    $logprefix echo | $logsuffix

    $logprefix printf "+ ${bold}npm cache clean --force --global --verbose $quiet${reset}\n" | $logsuffix
    if ( $arg_q ) ; then
        sudo $logprefix npm cache clean --force --global --verbose $quiet > /dev/null 2>&1
    else
        sudo $logprefix npm cache clean --force --global --verbose $quiet
    fi
    $logprefix echo | $logsuffix
fi


# pip cleanup
if ( $arg_pip ) ; then
    $logprefix printf "+ ${bold}pip cleanup --verbose $quiet${reset}\n" | $logsuffix
    if ( $arg_q ) ; then
        sudo $logprefix rm -rf -v $cmd_q ~/Library/Caches/pip > /dev/null 2>&1
        sudo $logprefix rm -rf -v $cmd_q /var/root/Library/Caches/pip > /dev/null 2>&1
    else
        sudo $logprefix rm -rf -v $cmd_q ~/Library/Caches/pip
        sudo $logprefix rm -rf -v $cmd_q /var/root/Library/Caches/pip
    fi
    $logprefix echo | $logsuffix
fi


# brew prune
if ( $arg_brew || $arg_cask ) ; then
    $logprefix printf "+ ${bold}brew prune --verbose $quiet${reset}\n" | $logsuffix
    if ( $arg_q ) ; then
        $logprefix brew prune --verbose $quiet > /dev/null 2>&1
    else
        $logprefix brew prune --verbose $quiet
    fi
    $logprefix echo | $logsuffix
fi


# archive caches if hard disk attached
if [ -e /Volumes/Jarry\ Shaw/ ] ; then
    # check if cache directory exists
    if [ -e $(brew --cache) ] ; then
        # move caches
        $logprefix printf "+ ${bold}cp -rf -v cache archive $quiet${reset}\n" | $logsuffix
        if ( $arg_q ) ; then
            $logprefix cp -rf -v $(brew --cache) /Volumes/Jarry\ Shaw/Developers/ > /dev/null 2>&1
        else
            $logprefix cp -rf -v $(brew --cache) /Volumes/Jarry\ Shaw/Developers/
        fi
        $logprefix echo | $logsuffix
    fi

    # if cask flag set
    if ( $arg_cask ) ; then
        $logprefix printf "+ ${bold}brew cask cleanup --verbose $quiet${reset}\n" | $logsuffix
        if ( $arg_q ) ; then
            $logprefix brew cask cleanup --verbose > /dev/null 2>&1
        else
            $logprefix brew cask cleanup --verbose
        fi
        $logprefix echo | $logsuffix
    fi

    # if brew flag set
    if ( $arg_brew ) ; then
        $logprefix printf "+ ${bold}brew cleanup --verbose $quiet${reset}\n" | $logsuffix
        if ( $arg_q ) ; then
            $logprefix rm -rf -v $( brew --cache ) > /dev/null 2>&1
        else
            $logprefix rm -rf -v $( brew --cache )
        fi
        $logprefix echo | $logsuffix
    fi
fi


# aftermath works
bash ./libupdate/aftermath.sh $logdate $logtime


# remove /tmp/log/update.log
rm -f $tmpfile


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1
