#!/bin/bash


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1


# terminal display
reset="\033[0m"         # reset
bold="\033[1m"          # bold
red="\033[91m"          # bright red foreground
green="\033[92m"        # bright green foreground
yellow="\033[93m"       # bright yellow foreground


################################################################################
# Check Node.js updates.
#
# Parameter list:
#   1. Log Date
#   2. All Flag
#   3. Quiet Flag
#   4. Verbose Flag
#   5. Outdated Flag
#   6. Package
#       ............
################################################################################


# parameter assignment
logdate=$1
arg_a=$2
arg_q=$3
arg_v=$4
arg_o=$5
arg_pkg=${*:6}


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


# if no outdated packages found
if ( ! $arg_o ) ; then
    $logprefix printf "update: ${green}npm${reset}: all ${bold}node modules${reset} have been up-to-date\n" | $logsuffix
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
        if ( $arg_a ) ; then
            flag=$name
        else
            flag=`npm list --global --parseable | sed "s/.*\///" | awk "/^$name$/"`
        fi
        if [[ -nz $flag ]] ; then
            $logprefix printf "+ ${bold}npm install $name --global $verbose $quiet${reset}\n" | $logsuffix
            if ( $arg_q ) ; then
                sudo $logprefix npm install $name --global $verbose $quiet > /dev/null 2>&1
            else
                sudo $logprefix npm install $name --global $verbose $quiet
            fi
            $logprefix echo | $logsuffix
        else
            $logprefix printf "update: ${yellow}npm${reset}: no node modules names ${red}$name${reset} installed\n" | $logsuffix

            # did you mean
            tmp=`npm list --global --parseable | sed "s/.*\///" | grep $arg_pkg | xargs`
            if [[ -nz $tmp ]] ; then
                dym=`python -c "print('${red}' + '${reset}, ${red}'.join(__import__('sys').stdin.read().strip().split()) + '${reset}')" <<< $tmp`
                $logprefix printf "update: ${yellow}npm${reset}: did you mean any of the following node modules: $dym?\n" | $logsuffix
            fi
            $logprefix echo | $logsuffix
        fi
    done
fi


# aftermath works
bash libupdate/aftermath.sh $logdate


# remove /tmp/log/update.log
rm -f $tmpfile


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1
