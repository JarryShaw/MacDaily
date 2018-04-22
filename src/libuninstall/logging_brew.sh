#!/bin/bash


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1


################################################################################
# Log Homebrew packages uninstallation.
#
# Parameter list:
#   1. Log Date
#   2. Log Time
#   3. Ignore-Dependencies Flag
#   4. Uninstalling Package
#       ............
################################################################################


# parameter assignment
logdate=$1
logtime=$2
arg_i=$3
arg_pkg=${*:4}


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
# logsuffix="grep ^.*$"


# log dependency
for name in $arg_pkg; do
    case $name in
        all)
            echo -e "+ brew list -1" >> $tmpfile
            $logprefix brew list -1
            echo >> $tmpfile ;;
        *)
            # check if package installed
            if brew list --versions $name > /dev/null 2&>1 ; then
                # along with dependencies or not
                echo -e "+ brew desc $name | sed -e \"s/\[1m//\" | grep \"$name: \" | sed \"s/\(.*\)*: .*/\1/\"" >> $tmpfile
                $logprefix brew desc $name | sed -e "s/\[1m//" | grep "$name: " | sed "s/\(.*\)*: .*/\1/"
                echo >> $tmpfile

                # if ignore-dependencies flag not set
                if ( ! $arg_i ) ; then
                    echo -e "+ brew deps $name" >> $tmpfile
                    $logprefix brew deps $name
                    echo >> $tmpfile
                fi
            else
                echo -e "Error: no formula names $name installed" >> $tmpfile
            fi ;;
    esac
done


# aftermath works
bash ./libuninstall/aftermath.sh $logdate $logtime


# remove /tmp/log/uninstall.log
rm -f $tmpfile


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1
