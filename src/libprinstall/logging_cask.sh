#!/bin/bash


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1


################################################################################
# Log Caskroom reinstalling packages.
#
# Parameter List
#   1. Log File
#   2. Temp File
#   3. Log Mode
#   4. Start Package
#   5. End Package
#   6. Package
#       ............
################################################################################


# parameter assignment
# echo $1 | cut -c2- | rev | cut -c2- | rev
logfile=`python -c "print(__import__('sys').stdin.readline().strip().strip('\''))" <<< $1`
tmpfile=`python -c "print(__import__('sys').stdin.readline().strip().strip('\''))" <<< $2`
logmode=$3
arg_s=$4
arg_e=$5
arg_pkg=${*:6}


# remove /tmp/log/logmode.log
rm -f "$tmpfile"


# create /tmp/log/logmode.log & /Library/Logs/Scripts/logmode/logdate.log
touch "$logfile"
touch "$tmpfile"


# log current status
echo "- /bin/bash $0 $@" >> "$tmpfile"


# log commands
logprefix="script -aq "$tmpfile""
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
            # check for reinstalling packages
            list=`brew cask list -1`
            for pkg in $list ; do
                if [[ $pkg > $start ]] && [[ $pkg < $end ]] ; then
                    echo -e "+ brew cask info $pkg | grep  \"$pkg: \" | sed \"s/\(.*\)*: .*/\1/\"" >> "$tmpfile"
                    $logprefix brew cask info $pkg | grep "$pkg: " | sed "s/\(.*\)*: .*/\1/"
                    echo >> "$tmpfile"
                fi
            done ;;
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
bash ./libprinstall/aftermath.sh "$logfile" "$tmpfile" $logmode


# remove /tmp/log/logmode.log
rm -f "$tmpfile"


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1
