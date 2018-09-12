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
#   1. Encrypted Password
#   2. Timeout Limit
#   3. Log File
#   4. Temp File
#   5. Disk File
#   6. Ruby Flag
#   7. Node.js Flag
#   8. Python Flag
#   9. Homebrew Flag
#  10. Caskroom Flag
#  11. Quiet Flag
################################################################################


# parameter assignment
password=`python -c "print(__import__('base64').b64decode(__import__('sys').stdin.readline().strip()).decode())" <<< $1`
timeout=$2
# echo $1 | cut -c2- | rev | cut -c2- | rev
logfile=`python -c "print(__import__('sys').stdin.readline().strip().strip('\''))" <<< $3`
tmpfile=`python -c "print(__import__('sys').stdin.readline().strip().strip('\''))" <<< $4`
dskfile=`python -c "print(__import__('sys').stdin.readline().strip().strip('\''))" <<< $5`
arg_gem=$6
arg_npm=$7
arg_pip=$8
arg_brew=$9
arg_cask=${10}
arg_q=${11}
# arg_v=${10}


# remove /tmp/log/update.log
rm -f "$tmpfile"


# create /tmp/log/update.log & /Library/Logs/Scripts/update/logdate/logtime.log
touch "$logfile"
touch "$tmpfile"


# log current status
echo "- /bin/bash $0 $@" >> "$tmpfile"


# log commands
logprefix="script -aq "$tmpfile""
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


# create deamon for validation
sudo --reset-timestamp
while [ -f "$tmpfile" ] ; do
    yes $password | sudo --stdin --validate
    echo ; sleep ${timeout:-150}
done &
pid=$!


# make traps
trap "exit 2" 1 2 3 15
trap "rm -f $tmpfile" 1 2 3 15
trap "kill $pid > /dev/null 2>&1" 0


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
        sudo $logprefix rm -rf -v $cmd_q ~/Library/Caches/pip/*/ > /dev/null 2>&1
        sudo $logprefix rm -rf -v $cmd_q /var/root/Library/Caches/pip/*/ > /dev/null 2>&1
    else
        sudo $logprefix rm -rf -v $cmd_q ~/Library/Caches/pip/*/
        sudo $logprefix rm -rf -v $cmd_q /var/root/Library/Caches/pip/*/
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
if [ -e "$dskfile" ] ; then
    # check if cache directory exists
    if [ -e $(brew --cache) ] ; then
        # move caches
        $logprefix printf "+ ${bold}cp -rf -v cache archive $quiet${reset}\n" | $logsuffix
        if ( $arg_q ) ; then
            $logprefix cp -rf -v $(brew --cache) "$dskfile" > /dev/null 2>&1
        else
            $logprefix cp -rf -v $(brew --cache) "$dskfile"
        fi
        $logprefix echo | $logsuffix

        # remove incomplete caches
        $logprefix printf "+ ${bold}rm -rf -v incomplete $quiet${reset}\n" | $logsuffix
        if ( $arg_q ) ; then
            $logprefix rm -rf -v "${dskfile}/Homebrew/*.incomplete" > /dev/null 2>&1
            $logprefix rm -rf -v "${dskfile}/Homebrew/Cask/*.incomplete" > /dev/null 2>&1
        else
            $logprefix rm -rf -v "${dskfile}/Homebrew/*.incomplete" 2> /dev/null
            $logprefix rm -rf -v "${dskfile}/Homebrew/Cask/*.incomplete" 2> /dev/null
        fi
        $logprefix echo | $logsuffix
    fi

    # # if brew or cask flag set
    # if $( $arg_brew || $arg_cask ) ; then
    #     $logprefix printf "+ ${bold}brew cleanup $quiet${reset}\n" | $logsuffix
    #     if ( $arg_q ) ; then
    #         $logprefix brew cleanup > /dev/null 2>&1
    #     else
    #         $logprefix brew cleanup
    #     fi
    #     $logprefix echo | $logsuffix
    # fi

    # if brew flag set
    if ( $arg_brew ) ; then
        $logprefix printf "+ ${bold}brew cleanup $quiet${reset}\n" | $logsuffix
        if ( $arg_q ) ; then
            $logprefix brew cleanup > /dev/null 2>&1
        else
            $logprefix brew cleanup
        fi
        $logprefix echo | $logsuffix
    fi

    # if brew or cask flag set
    if ( $arg_brew || $arg_cask ) ; then
        $logprefix printf "+ ${bold}rm -rf -v cache $quiet${reset}\n" | $logsuffix
        if ( $arg_q ) ; then
            $logprefix rm -rf -v $( brew --cache ) > /dev/null 2>&1
        else
            $logprefix rm -rf -v $( brew --cache )
        fi
        $logprefix echo | $logsuffix
    fi
fi


# kill the validation daemon
kill -0 $pid > /dev/null 2>&1


# aftermath works
aftermath=`python -c "import os; print(os.path.join(os.path.dirname(os.path.abspath('$0')), 'aftermath.sh'))"`
bash $aftermath "$logfile" "$tmpfile"


# remove /tmp/log/update.log
rm -f "$tmpfile"


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1
