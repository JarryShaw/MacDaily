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
#   1. Log File
#   2. Temp File
#   3. Disk File
#   4. Log Mode
#   5. Homebrew Flag
#   6. Caskroom Flag
#   7. Quiet Flag
################################################################################


# parameter assignment
# echo $1 | cut -c2- | rev | cut -c2- | rev
logfile=`python -c "print(__import__('sys').stdin.readline().strip().strip('\''))" <<< $1`
tmpfile=`python -c "print(__import__('sys').stdin.readline().strip().strip('\''))" <<< $2`
dskfile=`python -c "print(__import__('sys').stdin.readline().strip().strip('\''))" <<< $3`
logmode=$4
arg_brew=$5
arg_cask=$6
arg_q=$7
# arg_v=$8


# remove /tmp/log/logmode.log
rm -f "$tmpfile"


# create /tmp/log/logmode.log & /Library/Logs/Scripts/logmode/logdate.log
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

    # if brew or cask flag set
    if $( $arg_brew || $arg_cask ) ; then
        $logprefix printf "+ ${bold}brew cleanup --verbose $quiet${reset}\n" | $logsuffix
        if ( $arg_q ) ; then
            $logprefix brew cleanup > /dev/null 2>&1
        else
            $logprefix brew cleanup
        fi
        $logprefix echo | $logsuffix
    fi

    # # if cask flag set
    # if ( $arg_cask ) ; then
    #     $logprefix printf "+ ${bold}brew cask cleanup --verbose $quiet${reset}\n" | $logsuffix
    #     if ( $arg_q ) ; then
    #         $logprefix brew cask cleanup --verbose > /dev/null 2>&1
    #     else
    #         $logprefix brew cask cleanup --verbose
    #     fi
    #     $logprefix echo | $logsuffix
    # fi

    # # if brew flag set
    # if ( $arg_brew ) ; then
    #     $logprefix printf "+ ${bold}brew cleanup --verbose $quiet${reset}\n" | $logsuffix
    #     if ( $arg_q ) ; then
    #         $logprefix rm -rf -v $( brew --cache ) > /dev/null 2>&1
    #     else
    #         $logprefix rm -rf -v $( brew --cache )
    #     fi
    #     $logprefix echo | $logsuffix
    # fi
fi


# aftermath works
bash ./libprinstall/aftermath.sh "$logfile" "$tmpfile" $logmode


# remove /tmp/log/logmode.log
rm -f "$tmpfile"


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1
