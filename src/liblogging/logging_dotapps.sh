#!/bin/bash


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1


################################################################################
# Log all applications (*.app) installed on this Mac.

# Parameter list:
#   1. Log Name
################################################################################


# parameter assignment
logfile=$1


# log current status
echo "+ /bin/bash $0 $@" >> $logfile


# find apps
echo "++ sudo -H find / -type d -iname *.app -path \"/Volumes/Macintosh HD/*\"" >> $logfile
sudo -H find / -type d -iname *.app -path "/Volumes/Macintosh HD/*" >> $logfile 2> /dev/null
echo >> $logfile


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1
