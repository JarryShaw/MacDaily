#!/bin/bash


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1


################################################################################
# Log Caskroom packages uninstallation.
#
# Parameter list:
#   1. Log File
#   2. Temp File
#   3. Uninstalling Package
#       .........
################################################################################


# parameter assignment
# echo $1 | cut -c2- | rev | cut -c2- | rev
logfile=`python -c "print(__import__('sys').stdin.readline().strip().strip('\''))" <<< $1`
tmpfile=`python -c "print(__import__('sys').stdin.readline().strip().strip('\''))" <<< $2`
arg_pkg=${*:3}


# remove /tmp/log/uninstall.log
rm -f "$tmpfile"


# create /tmp/log/uninstall.log & /Library/Logs/Scripts/uninstall/logdate.log
touch "$logfile"
touch "$tmpfile"


# log current status
echo "- /bin/bash $0 $@" >> "$tmpfile"


# log commands
logprefix="script -aq "$tmpfile""
# logsuffix="grep ^.*$"


# log packages
for name in $arg_pkg; do
    case $name in
        all)
            echo -e "+ brew cask list -1" >> "$tmpfile"
            $logprefix brew cask list -1
            echo >> "$tmpfile" ;;
        *)
            # check if package installed
            flag=`brew cask list -1 | awk "/^$name$/"`
            if [[ ! -z $flag ]] ; then
                echo -e "+ brew cask info $name | grep  \"$name: \" | sed \"s/\(.*\)*: .*/\1/\"" >> "$tmpfile"
                $logprefix brew cask info $name | grep "$name: " | sed "s/\(.*\)*: .*/\1/"
                echo >> "$tmpfile"
            else
                echo -e "Error: no Cask names $name installed" >> "$tmpfile"
            fi ;;
    esac
done


# aftermath works
bash ./libuninstall/aftermath.sh "$logfile" "$logdate"


# remove /tmp/log/uninstall.log
rm -f "$tmpfile"


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1
