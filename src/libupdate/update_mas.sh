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
# Check Mac App Store updates.
#
# Parameter list:
#   1. Log File
#   2. Temp File
#   3. Quiet Flag
#   4. Verbose Flag
#   5. Outdated Flag
#   6. Package
#       ............
################################################################################


# Parameter Assignment
# echo $1 | cut -c2- | rev | cut -c2- | rev
logfile=`python -c "print(__import__('sys').stdin.readline().strip().strip('\''))" <<< $1`
tmpfile=`python -c "print(__import__('sys').stdin.readline().strip().strip('\''))" <<< $2`
arg_q=$3
arg_v=$4
arg_o=$5
arg_pkg=${*:6}


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
    $logprefix printf "update: ${green}mas${reset}: all ${bold}applications${reset} have been up-to-date\n\n" | $logsuffix
else
    # if verbose flag set
    if ( $arg_v ) ; then
        verbose="--verbose"
    else
        verbose=""
    fi

    # if quiet flag set
    if ( $arg_q ) ; then
        quiet="--quiet"
    else
        quiet=""
    fi

    # update procedure
    for name in $arg_pkg ; do
        # All or Specified Packages
        case $name in
            all)
                $logprefix printf "+ ${bold}mas upgrade $verbose $quiet${reset}\n" | $logsuffix
                if ( $arg_q ) ; then
                    sudo --stdin $logprefix mas upgrade $verbose $quiet > /dev/null 2>&1
                else
                    sudo --stdin $logprefix mas upgrade $verbose $quiet
                fi
                $logprefix echo | $logsuffix ;;
            *)
                flag=`mas list | sed "s/[0-9]* \(.*\)* ([0-9.]*)/\1/" | awk "/^$name$/"`
                if [[ ! -z $flag ]] ; then
                    $logprefix printf "+ ${bold}mas upgrade $name $verbose $quiet${reset}\n" | $logsuffix
                    number=`mas list | grep "$name" | sed "s/\([0-9]*\)* .*/\1/"`
                    if ( $arg_q ) ; then
                        sudo --stdin $logprefix mas upgrade $number $verbose $quiet > /dev/null 2>&1
                    else
                        sudo --stdin $logprefix mas upgrade $number $verbose $quiet
                    fi
                    $logprefix echo | $logsuffix
                else
                    $logprefix printf "update: ${yellow}mas${reset}: no application names ${red}$name${reset} installed\n" | $logsuffix

                    # did you mean
                    tmp=`mas list | sed "s/[0-9]* \(.*\)* ([0-9.]*)/\1/" | grep $name | xargs`
                    if [[ ! -z $tmp ]] ; then
                        dym=`python -c "print('${red}' + '${reset}, ${red}'.join(__import__('sys').stdin.read().strip().split()) + '${reset}')" <<< $tmp`
                        $logprefix printf "update: ${yellow}mas${reset}: did you mean any of the following applications: $dym?\n" | $logsuffix
                    fi
                    $logprefix echo | $logsuffix
                fi ;;
        esac
    done
fi


# aftermath works
aftermath=`python -c "import os; print(os.path.join(os.path.dirname(os.path.abspath('$0')), 'aftermath.sh'))"`
bash $aftermath "$logfile" "$tmpfile"


# remove /tmp/log/update.log
rm -f "$tmpfile"


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1
