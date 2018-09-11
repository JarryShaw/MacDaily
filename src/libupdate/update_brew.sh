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
# Check Homebrew updates.
#
# Parameter list:
#   1. Encrypted Password
#   2. Timeout Limit
#   3. Log File
#   4. Temp File
#   5. Quiet Flag
#   6. Verbose Flag
#   7. Outdated Flag
#   8. Package
#       ............
################################################################################


# parameter assignment
password=`python -c "print(__import__('base64').b64decode(__import__('sys').stdin.readline().strip()).decode())" <<< $1`
timeout=$2
# echo $1 | cut -c2- | rev | cut -c2- | rev
logfile=`python -c "print(__import__('sys').stdin.readline().strip().strip('\''))" <<< $3`
tmpfile=`python -c "print(__import__('sys').stdin.readline().strip().strip('\''))" <<< $4`
arg_q=$5
arg_v=$6
arg_o=$7
arg_pkg=${*:8}


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


# if no outdated packages found
if ( ! $arg_o ) ; then
    $logprefix printf "update: ${green}brew${reset}: all ${bold}formulae${reset} have been up-to-date\n\n" | $logsuffix
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

    # create deamon for validation
    sudo --reset-timestamp
    while true ; do
        yes $password | sudo --stdin --validate
        echo ; sleep ${timeout:-300}
    done &
    pid=$!

    # update procedure
    for name in $arg_pkg ; do
        flag=`brew list -1 | awk "/^$name$/"`
        if [[ ! -z $flag ]] ; then
            $logprefix printf "+ ${bold}brew upgrade $name --cleanup $verbose $quiet${reset}\n" | $logsuffix
            if ( $arg_q ) ; then
                $logprefix brew upgrade $name --cleanup $verbose $quiet > /dev/null 2>&1
            else
                $logprefix brew upgrade $name --cleanup $verbose $quiet
            fi
            $logprefix echo | $logsuffix
        else
            $logprefix printf "update: ${yellow}brew${reset}: no formula names ${red}$name${reset} installed\n" | $logsuffix

            # did you mean
            tmp=`brew list -1 | grep $name | xargs`
            if [[ ! -z $tmp ]] ; then
                dym=`python -c "print('${red}' + '${reset}, ${red}'.join(__import__('sys').stdin.read().strip().split()) + '${reset}')" <<< $tmp`
                $logprefix printf "update: ${yellow}brew${reset}: did you mean any of the following formulae: $dym?\n" | $logsuffix
            fi
            $logprefix echo | $logsuffix
        fi
    done

    # kill the validation daemon
    kill -2 $pid
fi


# aftermath works
aftermath=`python -c "import os; print(os.path.join(os.path.dirname(os.path.abspath('$0')), 'aftermath.sh'))"`
bash $aftermath "$logfile" "$tmpfile"


# remove /tmp/log/update.log
rm -f "$tmpfile"


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1
