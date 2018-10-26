#!/bin/bash


# parameter assignment
verbose=$1


# check apm installed
which apm > /dev/null 2>&1
if [ $? -ne 0 ] ; then
    exit 1
fi


# dump procedure
if ( $verbose ) ; then
    # fetch description for verbose output
    list=`apm list --bare 2> /dev/null | sed "s/\(.*\)*@.*/\1/" | sort | uniq | xargs`
    for name in $list ; do
        apm show $name 2> /dev/null | awk "NR==4" | sed "s/├── /# /" >> ~/.Macfile
        version=`apm show $name 2> /dev/null | awk "NR==2" | sed "s/├── .\[33m\(.*\)*.\[39m/\1/"`
        echo -e apm \"$name\", version: $version >> ~/.Macfile
    done
else
    apm list --bare 2> /dev/null | grep '@' | sed "s/\(.*\)*@\(.*\)*/apm \"\1\", version: \2/" | sort | uniq >> ~/.Macfile
fi
