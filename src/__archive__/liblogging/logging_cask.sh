#!/bin/bash


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1


################################################################################
# Log applications installed through Homebrew Caskroom.

# Parameter list:
#   1. Log Name
################################################################################


# parameter assignment
# echo $1 | cut -c2- | rev | cut -c2- | rev
logfile=`python -c "print(__import__('sys').stdin.readline().strip().strip('\''))" <<< $1`


# log current status
echo "+ /bin/bash $0 $@" >> "$logfile"


# find apps
echo -e "++ brew cask list -1 | sed \"s/^/INF: /\"" >> "$logfile"
brew cask list -1 2> /dev/null | sed "s/^/INF: /" >> "$logfile"
echo >> "$logfile"


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1
