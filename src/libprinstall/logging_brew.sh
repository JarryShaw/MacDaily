#!/bin/bash


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1


################################################################################
# Log Homebrew packages reinstallation.
#
# Parameter List
#   1. Log Date
#   2. Log Time
#   3. Log Mode
#   4. Start Package
#   5. End Package
#   6. Package
#       ............
################################################################################


# parameter assignment
logdate=$1
logtime=$2
logmode=$3
arg_s=$4
arg_e=$5
arg_pkg=${*:6}


# log file prepare
logfile="/Library/Logs/Scripts/$logmode/$logdate/$logtime.log"
tmpfile="/tmp/log/$logmode.log"


# remove /tmp/log/logmode.log
rm -f $tmpfile


# create /tmp/log/logmode.log & /Library/Logs/Scripts/logmode/logdate.log
touch $logfile
touch $tmpfile


# log current status
echo "- /bin/bash $0 $@" >> $tmpfile


# log commands
logprefix="script -aq $tmpfile"
# logsuffix="grep ^.*$"


# if start package set
case $arg_s in
    none)
        # perl -CA -le "print chr shift" 64
        start="@" ;;    # ASCII 64 (A - 65)
    *)
        start=$arg_s ;;
esac


# if end package set
case $arg_e in
    none)
        # perl -CA -le "print chr shift" 123
        end="{" ;;      # ASCII 123 (z - 122)
    *)
        end=$arg_e ;;
esac


# check for reinstalling packages
for name in $arg_pkg ; do
    case $name in
        all)
            list=`brew list -1`
            for pkg in $list ; do
                if [[ $pkg > $start ]] && [[ $pkg < $end ]] ; then
                    echo -e "+ brew desc $pkg | sed -e \"s/\[1m//\" | grep \"$pkg: \" | sed \"s/\(.*\)*:.*/\1/\"" >> $tmpfile
                    $logprefix brew desc $pkg | sed -e "s/\[1m//" | grep "$pkg: " | sed "s/\(.*\)*:.*/\1/"
                    echo >> $tmpfile
                fi
            done ;;
        *)
            # check if package installed
            if brew list --versions $name > /dev/null ; then
                echo -e "+ brew desc $name | sed -e \"s/\[1m//\" | grep \"$name: \" | sed \"s/\(.*\)*:.*/\1/\"" >> $tmpfile
                $logprefix brew desc $name | sed -e "s/\[1m//" | grep "$name: " | sed "s/\(.*\)*:.*/\1/"
                echo >> $tmpfile
            else
                echo -e "Error: no formula names $name installed" >> $tmpfile
            fi ;;
    esac
done


# aftermath works
bash ./libprinstall/aftermath.sh $logdate $logtime $logmode


# remove /tmp/log/logmode.log
rm -f $tmpfile


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1
