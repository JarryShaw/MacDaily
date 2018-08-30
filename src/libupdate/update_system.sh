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
# Check system software updates.
#
# Parameter list:
#   1. Encrypted Password
#   2. Log File
#   3. Temp File
#   4. Quiet Flag
#   5. Verbose Flag
#   6. Restart Flag
#   7. Outdated Flag
#   8. Package
#       ............
################################################################################


# Parameter Assignment
password=`python -c "print(__import__('base64').b64decode(__import__('sys').stdin.readline().strip()).decode())" <<< $1`
# echo $1 | cut -c2- | rev | cut -c2- | rev
logfile=`python -c "print(__import__('sys').stdin.readline().strip().strip('\''))" <<< $2`
tmpfile=`python -c "print(__import__('sys').stdin.readline().strip().strip('\''))" <<< $3`
arg_q=$4
arg_v=$5
arg_r=$6
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
    $logprefix printf "update: ${green}system${reset}: all ${bold}applications${reset} have been up-to-date\n\n" | $logsuffix
else
    # if quiet flag set
    if ( $arg_q ) ; then
        quiet="--quiet"
    else
        quiet=""
    fi

    # if restart flag set
    if ( $arg_r ) ; then
        restart="--restart"
    else
        restart=""
    fi

    # update procedure
    for name in $arg_pkg ; do
        # All or Specified Packages
        case $name in
            all)
                # ask for password up-front
                sudo --reset-timestamp
                sudo --stdin --validate <<< $password ; echo

                $logprefix printf "+ ${bold}softwareupdate --install --no-scan --all $restart $verbose $quiet${reset}\n" | $logsuffix
                if ( $arg_q ) ; then
                    sudo $logprefix softwareupdate --install --no-scan --all $restart $verbose $quiet > /dev/null 2>&1
                else
                    sudo $logprefix softwareupdate --install --no-scan --all $restart $verbose $quiet
                fi
                $logprefix echo | $logsuffix ;;
            *)
                installed="find /Applications -path \"*Contents/_MASReceipt/receipt\" -maxdepth 4 -print | sed \"s#.app/Contents/_MASReceipt/receipt#.app#g; s#/Applications/##\""
                flag=`$installed | sed "s/.app//" | awk "/^$name$/"`
                if [[ ! -z $flag ]] ; then
                    # ask for password up-front
                    sudo --reset-timestamp
                    sudo --stdin --validate <<< $password ; echo

                    $logprefix printf "+ ${bold}softwareupdate --install --no-scan $name $restart $verbose $quiet${reset}\n" | $logsuffix
                    if ( $arg_q ) ; then
                        sudo $logprefix softwareupdate --install --no-scan $name $restart $verbose $quiet > /dev/null 2>&1
                    else
                        sudo $logprefix softwareupdate --install --no-scan $name $restart $verbose $quiet
                    fi
                    $logprefix echo | $logsuffix
                else
                    $logprefix printf "update: ${yellow}system${reset}: no application names ${red}$name${reset} installed\n" | $logsuffix

                    # did you mean
                    tmp=`$installed | sed "s/.app//" | grep $name | xargs`
                    if [[ ! -z $tmp ]] ; then
                        dym=`python -c "print('${red}' + '${reset}, ${red}'.join(__import__('sys').stdin.read().strip().split()) + '${reset}')" <<< $tmp`
                        $logprefix printf "update: ${yellow}system${reset}: did you mean any of the following applications: $dym?\n" | $logsuffix
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
