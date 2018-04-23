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
# Show dependencies of Homebrew packages.
#
# Parameter list:
#   1. Log Date
#   2. Log Time
#   3. Tree Flag
#   4. Package
#       ............
################################################################################


# parameter assignment
logdate=$1
logtime=$2
arg_t=$3
arg_pkg=${*:4}


# log file prepare
logfile="/Library/Logs/Scripts/dependency/$logdate/$logtime.log"
tmpfile="/tmp/log/dependency.log"


# remove /tmp/log/dependency.log
rm -f $tmpfile


# create /tmp/log/dependency.log & /Library/Logs/Scripts/dependency/logdate.log
touch $logfile
touch $tmpfile


# log current status
echo "- /bin/bash $0 $@" >> $tmpfile


# log commands
logprefix="script -aq $tmpfile"
# logsuffix="grep ^.*$"


# if tree flag set
if ( $arg_t ) ; then
    tree="--tree"
else
    tree=""
fi


# show dependencies
for name in $arg_pkg ; do
    case $name in
        all)
            list=`brew leaves`
            for pkg in $list ; do
                $logprefix printf "+ ${bold}brew deps $pkg $tree${reset}\n"
                $logprefix brew deps $pkg $tree
                $logprefix echo
            done ;;
        *)
            # check if package installed
            if brew list --versions $name > /dev/null ; then
                $logprefix printf "+ ${bold}brew deps $name $tree${reset}\n"
                $logprefix brew deps $name $tree
                $logprefix echo
            else
                $logprefix printf "dependency: ${yellow}brew${reset}: no formula names $name installed\n"

                # did you mean
                tmp=`brew list -1 | grep $name | xargs`
                if [[ -nz $tmp ]] ; then
                    dym=`python -c "print('${red}' + '${reset}, ${red}'.join(__import__('sys').stdin.read().strip().split()) + '${reset}')" <<< $tmp`
                    $logprefix printf "dependency: ${yellow}brew${reset}: did you mean any of the following formulae: $dym?\n"
                fi
                $logprefix echo
            fi ;;
    esac
done


# aftermath works
bash ./libdependency/aftermath.sh $logdate $logtime


# remove /tmp/log/dependency.log
rm -f $tmpfile


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1