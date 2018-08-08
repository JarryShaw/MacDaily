# #!/bin/bash


# parameter assignment
arg_v=$1


# dump procedure
if ( $arg_v ) ; then
    # fetch description for verbose output
    list=`mas list | sed "s/\([0-9]*\)* .*/\1/" | sort | uniq | xargs`
    for temp in $list ; do
        mas info $temp | head -1 | sed "s/^/# /" >> ~/.Macfile
        name=`mas list | grep $temp | sed "s/[0-9]* \(.*\)* ([0-9.]*)/\1/"`
        echo mas "$name", id: $temp >> ~/.Macfile
    done
else
    mas list | sed "s/\([0-9]*\)* \([[:print:]]*\)* ([0-9.]*)/mas \"\2\", id: \1/" | sort | uniq >> ~/.Macfile
fi
