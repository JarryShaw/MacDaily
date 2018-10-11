#!/bin/bash


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1


################################################################################
# Log Caskroom packages updates.
#
# Parameter List
#   1. Log File
#   2. Temp File
#   3. Greedy Flag
#   4. Force Flag
################################################################################


# parameter assignment
# echo $1 | cut -c2- | rev | cut -c2- | rev
logfile=`python -c "print(__import__('sys').stdin.readline().strip().strip('\''))" <<< $1`
tmpfile=`python -c "print(__import__('sys').stdin.readline().strip().strip('\''))" <<< $2`
arg_g=$3
arg_f=$4


# remove /tmp/log/update.log
rm -f "$tmpfile"


# create /tmp/log/update.log & /Library/Logs/Scripts/update/logdate/logtime.log
touch "$logfile"
touch "$tmpfile"


# log current status
echo "- /bin/bash $0 $@" >> "$tmpfile"


# log commands
logprefix="script -aq "$tmpfile""
# logsuffix="grep ^.*$"


# if greedy flag set
if ( $arg_g ) ; then
    greedy="--greedy"
else
    greedy=""
fi


# if force flag set
if ( $arg_f ) ; then
    # following algorithm of Caskroom upgrade cblushits to
    #     @Atais from <apple.stackexchange.com>
    list=`brew cask list -1`
    for cask in $list ; do
        version=$(brew cask info $cask | sed -n "s/$cask:\ \(.*\)/\1/p")
        installed=$(find "/usr/local/Caskroom/$cask" -type d -maxdepth 1 -maxdepth 1 -name "$version")
        if [[ -z $installed ]] ; then
            $logprefix brew cask info $cask | grep "$cask: " | sed "s/\(.*\)*: .*/\1/"
        fi
    done
else
    echo -e "+ brew cask outdated --quiet $greedy" >> "$tmpfile"
    if ( $arg_g ) ; then
        $logprefix brew cask outdated --greedy --quiet
    else
        $logprefix brew cask outdated --greedy | awk '!/latest/' | sed "s/\(.*\)* (.*) .*/\1/"
    fi
    echo >> "$tmpfile"
fi


# aftermath works
aftermath=`python -c "import os; print(os.path.join(os.path.dirname(os.path.abspath('$0')), 'aftermath.sh'))"`
bash $aftermath "$logfile" "$tmpfile"


# remove /tmp/log/update.log
rm -f "$tmpfile"


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1
