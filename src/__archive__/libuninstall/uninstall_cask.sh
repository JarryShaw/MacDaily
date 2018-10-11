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
#   1. Encrypted Password
#   2. Log File
#   3. Temp File
#   4. Quiet Flag
#   5. Verbose Flag
#   6. Force Flag
#   7. Package
#       ............
################################################################################


# parameter assignment
password=`python -c "print(__import__('base64').b64decode(__import__('sys').stdin.readline().strip()).decode())" <<< $1`
# echo $1 | cut -c2- | rev | cut -c2- | rev
logfile=`python -c "print(__import__('sys').stdin.readline().strip().strip('\''))" <<< $2`
tmpfile=`python -c "print(__import__('sys').stdin.readline().strip().strip('\''))" <<< $3`
arg_q=$4
arg_v=$5
arg_f=$6
arg_pkg=${*:7}


# remove /tmp/log/uninstall.log
rm -f "$tmpfile"


# create /tmp/log/uninstall.log & /Library/Logs/Scripts/uninstall/logdate.log
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


# uninstall procedure
for name in $arg_pkg ; do
    case $name in
        all)
            list=`brew cask list -1`
            for pkg in $list ; do
                # ask for password up-front
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
            flag=`brew cask list -1 | awk "/^$name$/"`
            if [[ ! -z $flag ]] ; then
                $logprefix printf "+ ${bold}brew cask uninstall $name $force $verbose $quiet${reset}\n" | $logsuffix
                if ( $arg_q ) ; then
                    $logprefix brew cask uninstall $name $force $verbose $quiet > /dev/null 2>&1
                else
                    $logprefix brew cask uninstall $name $force $verbose $quiet
                fi
                $logprefix echo | $logsuffix
            else
                $logprefix printf "uninstall: ${yellow}cask${reset}: no Cask names ${red}$name${reset} installed\n" | $logsuffix

                # did you mean
                tmp=`brew cask list -1 | grep $name | xargs`
                if [[ ! -z $tmp ]] ; then
                    dym=`python -c "print('${red}' + '${reset}, ${red}'.join(__import__('sys').stdin.read().strip().split()) + '${reset}')" <<< $tmp`
                    $logprefix printf "uninstall: ${yellow}brew${reset}: did you mean any of the following formulae: $dym?\n" | $logsuffix
                fi
                $logprefix echo | $logsuffix
            fi ;;
    esac
done


# kill the validation daemon
kill -0 $pid > /dev/null 2>&1


# aftermath works
aftermath=`python -c "import os; print(os.path.join(os.path.dirname(os.path.abspath('$0')), 'aftermath.sh'))"`
bash $aftermath "$logfile" "$tmpfile"


# remove /tmp/log/uninstall.log
rm -f "$tmpfile"


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1
