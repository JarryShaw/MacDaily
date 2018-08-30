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
#   1. Log File
#   2. Temp File
#   3. All Flag
#   4. Quiet Flag
#   5. Verbose Flag
#   6. Outdated Flag
#   7. Package
#       ............
################################################################################


# parameter assignment
# echo $1 | cut -c2- | rev | cut -c2- | rev
logfile=`python -c "print(__import__('sys').stdin.readline().strip().strip('\''))" <<< $1`
tmpfile=`python -c "print(__import__('sys').stdin.readline().strip().strip('\''))" <<< $2`
arg_a=$3
arg_q=$4
arg_v=$5
arg_o=$6
arg_pkg=${*:7}


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
    $logprefix printf "update: ${green}npm${reset}: all ${bold}node modules${reset} have been up-to-date\n\n" | $logsuffix
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
        if [[ ! -z $flag ]] ; then
            $logprefix printf "+ ${bold}npm install $name --global $verbose $quiet${reset}\n" | $logsuffix
            if ( $arg_q ) ; then
                sudo --stdin $logprefix npm install $name --global $verbose $quiet > /dev/null 2>&1
            else
                sudo --stdin $logprefix npm install $name --global $verbose $quiet
            fi
            $logprefix echo | $logsuffix
        else
            $logprefix printf "update: ${yellow}npm${reset}: no node modules names ${red}$name${reset} installed\n" | $logsuffix

            # did you mean
            tmp=`npm list --global --parseable | sed "s/.*\///" | grep $arg_pkg | xargs`
            if [[ ! -z $tmp ]] ; then
                dym=`python -c "print('${red}' + '${reset}, ${red}'.join(__import__('sys').stdin.read().strip().split()) + '${reset}')" <<< $tmp`
                $logprefix printf "update: ${yellow}npm${reset}: did you mean any of the following node modules: $dym?\n" | $logsuffix
            fi
            $logprefix echo | $logsuffix
        fi
    done
fi


# aftermath works
aftermath=`python -c "import os; print(os.path.join(os.path.dirname(os.path.abspath('$0')), 'aftermath.sh'))"`
bash $aftermath "$logfile" "$tmpfile"


# remove /tmp/log/update.log
rm -f "$tmpfile"


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1
