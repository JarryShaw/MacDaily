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
# Reinstall Caskroom packages.
#
# Parameter list:
#   1. Log Date
#   2. Log Time
#   3. Quiet Flag
#   4. Verbose Flag
#   5. Package
#       ............
################################################################################


# parameter assignment
logdate=$1
logtime=$2
arg_q=$3
arg_v=$4
arg_pkg=${*:5}


# log file prepare
logfile="/Library/Logs/Scripts/reinstall/$logdate/$logtime.log"
tmpfile="/tmp/log/reinstall.log"


# remove /tmp/log/reinstall.log
rm -f $tmpfile


# create /tmp/log/reinstall.log & /Library/Logs/Scripts/reinstall/logdate.log
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
else
    quiet=""
fi


# if verbose flag set
if ( $arg_v ) ; then
    verbose="--verbose"
else
    verbose=""
fi


# reinstall procedure
for name in $arg_pkg ; do
    flag=`brew cask list -1 | awk "/^$name$/"`
    if [[ -nz $flag ]] ; then
        $logprefix printf "+ ${bold}brew cask reinstall $name $verbose $quiet${reset}\n" | $logsuffix
        if ( $arg_q ) ; then
            $logprefix brew cask reinstall $name $verbose $quiet > /dev/null 2>&1
        else
            $logprefix brew cask reinstall $name $verbose $quiet
        fi
        $logprefix echo | $logsuffix
    else
        $logprefix printf "reinstall: ${yellow}brew${reset}: no formula names $name installed\n" | $logsuffix

        # did you mean
        tmp=`brew list -1 | grep $name | xargs`
        if [[ -nz $tmp ]] ; then
            dym=`python -c "print('${red}' + '${reset}, ${red}'.join(__import__('sys').stdin.read().strip().split()) + '${reset}')" <<< $tmp`
            $logprefix printf "reinstall: ${yellow}brew${reset}: did you mean any of the following formulae: $dym?\n" | $logsuffix
        fi
        $logprefix echo | $logsuffix
    fi
done


# aftermath works
bash ./libprinstall/aftermath.sh $logdate $logtime "reinstall"


# remove /tmp/log/reinstall.log
rm -f $tmpfile


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1
