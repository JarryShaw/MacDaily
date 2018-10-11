#!/bin/bash


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1


################################################################################
# Log Homebrew packages.
#
# Parameter list:
#   1. Log File
#   2. Temp File
#   3. Package
#       ............
################################################################################


# parameter assignment
# echo $1 | cut -c2- | rev | cut -c2- | rev
logfile=`python -c "print(__import__('sys').stdin.readline().strip().strip('\''))" <<< $1`
tmpfile=`python -c "print(__import__('sys').stdin.readline().strip().strip('\''))" <<< $2`
arg_pkg=${*:3}


# remove /tmp/log/dependency.log
rm -f "$tmpfile"


# create /tmp/log/dependency.log & /Library/Logs/Scripts/dependency/logdate.log
touch "$logfile"
touch "$tmpfile"


# log current status
echo "- /bin/bash $0 $@" >> "$tmpfile"


# log commands
logprefix="script -aq "$tmpfile""
# logsuffix="grep ^.*$"


# log dependency
for name in $arg_pkg; do
    case $name in
        all)
            echo -e "+ brew leaves" >> "$tmpfile"
            $logprefix brew leaves
            echo >> "$tmpfile" ;;
        *)
            # check if package installed
            flag=`brew list -1 | awk "/^$name$/"`
            if [[ ! -z $flag ]] ; then
                echo -e "+ brew desc $name | sed -e \"s/.*\[1m\(.*\)*:.*/\1/\"" >> ""$tmpfile""
                $logprefix brew desc $name | sed -e "s/.*\[1m\(.*\)*:.*/\1/"
                echo >> "$tmpfile"
            else
                echo -e "Error: no formula names $name installed" >> "$tmpfile"
            fi ;;
    esac
done


# aftermath works
bash ./libdependency/aftermath.sh "$logfile" "$tmpfile"


# remove /tmp/log/dependency.log
rm -f "$tmpfile"


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1
