#!/bin/bash


# terminal display
reset="\033[0m"         # reset
red="\033[91m"          # bright red foreground
yellow="\033[93m"       # bright yellow foreground


# check if Macfile exists
if [ -e ~/.Macfile ] ; then
    # read Macfile line by line
    while read -r line ; do
        # skip comment lines
        if [[ $line =~ ^(#\ )(.*)$ ]] ; then
            continue
        fi

        # make script path
        mode=`sed "s/^\([a-z0-9.]*\)* .*/\1/" <<< $line`
        path=`python -c "import os; print(os.path.join(os.path.dirname(os.path.abspath('$0')), 'load_${mode}.sh'))"`
        
        # check prefix
        if [ -e $path ] ; then
            bash $path $line
        else
            echo -e "bundle: ${yellow}load${reset}: Unexpected prefix ${mode}"
        fi
    done < ~/.Macfile
else
    echo -e "bundle: ${red}load${reset}: No Macfile found"
fi
