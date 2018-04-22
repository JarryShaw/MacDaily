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
# Uninstall Caskroom packages.
#
# Parameter list:
#   1. Log Date
#   2. Log Time
#   3. Quiet Flag
#   4. Verbose Flag
#   5. Force Flag
#   6. Package
#       ............
################################################################################


# parameter assignment
logdate=$1
logtime=$2
arg_q=$3
arg_v=$4
arg_f=$5
arg_pkg=${*:6}


# log file prepare
logfile="/Library/Logs/Scripts/uninstall/$logdate/$logtime.log"
tmpfile="/tmp/log/uninstall.log"


# remove /tmp/log/uninstall.log
rm -f $tmpfile


# create /tmp/log/uninstall.log & /Library/Logs/Scripts/uninstall/logdate.log
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


# if force flag set
if ( $arg_f ) ; then
    force="--force"
else
    force=""
fi


# uninstall procedure
for name in $arg_pkg ; do
    case $name in
        all)
            list=`brew cask list -1`
            for pkg in $list ; do
                $logprefix printf "+ ${bold}brew cask uninstall $pkg $force $verbose $quiet${reset}\n" | $logsuffix
                if ( $arg_q ) ; then
                    $logprefix brew cask uninstall $pkg $force $verbose $quiet > /dev/null 2>&1
                else
                    $logprefix brew cask uninstall $pkg $force $verbose $quiet
                fi
                $logprefix echo | $logsuffix
            done ;;
        *)
            # check if package installed
            if brew cask list $name > /dev/null 2>&1 ; then
                $logprefix printf "+ ${bold}brew cask uninstall $name $force $verbose $quiet${reset}\n" | $logsuffix
                if ( $arg_q ) ; then
                    $logprefix brew cask uninstall $name $force $verbose $quiet > /dev/null 2>&1
                else
                    $logprefix brew cask uninstall $name $force $verbose $quiet
                fi
                $logprefix echo | $logsuffix
            else
                $logprefix printf "uninstall: ${yellow}cask${reset}: no Cask names $name installed\n" | $logsuffix

                # did you mean
                tmp=`brew cask list -1 | grep $name | xargs`
                if [[ -nz $tmp ]] ; then
                    dym=`python -c "print('${red}' + '${reset}, ${red}'.join(__import__('sys').stdin.read().strip().split()) + '${reset}')" <<< $tmp`
                    $logprefix printf "uninstall: ${yellow}brew${reset}: did you mean any of the following formulae: $dym?\n" | $logsuffix
                fi
                $logprefix echo | $logsuffix
            fi ;;
    esac
done


# aftermath works
bash ./libuninstall/aftermath.sh $logdate $logtime


# remove /tmp/log/uninstall.log
rm -f $tmpfile


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1
