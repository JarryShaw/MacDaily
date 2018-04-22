#!/bin/bash


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1


################################################################################
# Log Homebrew packages.
#
# Parameter list:
#   1. Log Date
#   2. Log Time
#   3. Package
#       ............
################################################################################


# parameter assignment
logdate=$1
logtime=$2
arg_pkg=${*:3}


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


# log dependency
for name in $arg_pkg; do
    case $name in
        all)
            echo -e "+ brew leaves" >> $tmpfile
            $logprefix brew leaves
            echo >> $tmpfile ;;
        *)
            # check if package installed
            if brew list --versions $name > /dev/null ; then
                echo -e "+ brew desc $name | sed \"s/\(.*\)*: .*/\1/\"" >> $tmpfile
                $logprefix brew desc $name | sed "s/\(.*\)*: .*/\1/" | $logsuffix
                echo >> $tmpfile
            else
                echo -e "Error: no formula names $name installed" >> $tmpfile
            fi ;;
    esac
done


# aftermath works
bash ./libdependency/aftermath.sh $logdate $logtime


# remove /tmp/log/dependency.log
rm -f $tmpfile


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1
