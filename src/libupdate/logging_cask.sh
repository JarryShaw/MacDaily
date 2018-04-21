#!/bin/bash


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1


################################################################################
# Log Caskroom packages updates.
#
# Parameter List
#   1. Log Date
#   2. Greedy Flag
################################################################################


# parameter assignment
logdate=$1
arg_g=$2


# log file prepare
logfile="/Library/Logs/Scripts/update/$logdate.log"
tmpfile="/tmp/log/update.log"


# remove /tmp/log/update.log
rm -f $tmpfile


# create /tmp/log/update.log & /Library/Logs/Scripts/update/logdate.log
touch $logfile
touch $tmpfile


# log current status
echo "- /bin/bash $0 $@" >> $tmpfile


# log commands
logprefix="script -aq $tmpfile"
# logsuffix="grep ^.*$"


# if greedy flag set
if ( $arg_g ) ; then
    echo -e "+ brew cask outdated --quiet --greedy" >> $tmpfile
    $logprefix brew cask outdated --quiet --greedy
    echo >> $tmpfile
else
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
fi


# aftermath works
bash libupdate/aftermath.sh $logdate


# remove /tmp/log/update.log
rm -f $tmpfile


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1
