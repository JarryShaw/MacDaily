#!/bin/bash


# parameter assignment
verbose=$1


# check brew installed
which brew > /dev/null 2>&1
if [ $? -ne 0 ] ; then
    exit 1
fi


# dump procedure
brew tap 2> /dev/null | sed "s/\(.*\)*/tap \"\1\"/" | sort | uniq >> ~/.Macfile
