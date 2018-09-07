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
#   2. Log File
#   3. Temp File
#   4. Disk File
#   5. Ruby Flag
#   6. Node.js Flag
#   7. Python Flag
#   8. Homebrew Flag
#   9. Caskroom Flag
#  10. Quiet Flag
################################################################################


# parameter assignment
password=`python -c "print(__import__('base64').b64decode(__import__('sys').stdin.readline().strip()).decode())" <<< $1`
# echo $1 | cut -c2- | rev | cut -c2- | rev
logfile=`python -c "print(__import__('sys').stdin.readline().strip().strip('\''))" <<< $2`
tmpfile=`python -c "print(__import__('sys').stdin.readline().strip().strip('\''))" <<< $3`
dskfile=`python -c "print(__import__('sys').stdin.readline().strip().strip('\''))" <<< $4`
arg_gem=$5
arg_npm=$6
arg_pip=$7
arg_brew=$8
arg_cask=$9
arg_q=${10}
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


# gem cleanup
if ( $arg_gem ) ; then
    # ask for password up-front
    sudo --reset-timestamp
    sudo --stdin --validate <<< $password ; echo

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
    # ask for password up-front
    sudo --reset-timestamp
    sudo --stdin --validate <<< $password ; echo

    $logprefix printf "+ ${bold}npm dedupe --global --verbose $quiet${reset}\n" | $logsuffix
    if ( $arg_q ) ; then
        sudo $logprefix npm dedupe --global --verbose $quiet > /dev/null 2>&1
    else
        sudo $logprefix npm dedupe --global --verbose $quiet
    fi
    $logprefix echo | $logsuffix

    # ask for password up-front
    sudo --reset-timestamp
    sudo --stdin --validate <<< $password ; echo

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
    # ask for password up-front
    sudo --reset-timestamp
    sudo --stdin --validate <<< $password ; echo

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

    # if cask flag set
    if ( $arg_cask ) ; then
        $logprefix printf "+ ${bold}brew cleanup $quiet${reset}\n" | $logsuffix
        if ( $arg_q ) ; then
            $logprefix brew cleanup > /dev/null 2>&1
        else
            $logprefix brew cleanup
        fi
        $logprefix echo | $logsuffix
    fi

    # if brew flag set
    if ( $arg_brew ) ; then
        $logprefix printf "+ ${bold}rm -rf -v cache $quiet${reset}\n" | $logsuffix
        if ( $arg_q ) ; then
            $logprefix rm -rf -v $( brew --cache ) > /dev/null 2>&1
        else
            $logprefix rm -rf -v $( brew --cache )
        fi
        $logprefix echo | $logsuffix
    fi
fi


# aftermath works
aftermath=`python -c "import os; print(os.path.join(os.path.dirname(os.path.abspath('$0')), 'aftermath.sh'))"`
bash $aftermath "$logfile" "$tmpfile"


# remove /tmp/log/update.log
rm -f "$tmpfile"


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1
