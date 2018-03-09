#!/bin/bash


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1


# preset terminal output colours
blush="tput setaf 1"    # blush / red
green="tput setaf 2"    # green
reset="tput sgr0"       # reset


################################################################################
# Check Caskroom updates.
#
# Parameter list:
#   1. Log Date
#   2. Quiet Flag
#   3. Verbose Flag
#   4. Force Flag
#   5. Greedy Flag
#   6. Outdated Flag
#   7. Package
#       ............
################################################################################


# parameter assignment
logdate=$1
arg_q=$2
arg_v=$3
arg_f=$4
arg_g=$5
arg_o=$6
arg_pkg=${*:7}


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
logprefix="script -q /dev/null"
logcattee="tee -a $tmpfile"
if ( $arg_q ) ; then
    logsuffix="grep ^$"
else
    logsuffix="grep ^.*$"
fi


# following function of Caskroom upgrade cblushits to
#     @Atais from <apple.stackexchange.com>
#
# caskroom update function usage:
#   caskupdate cask
function caskupdate {
    # parameter assignment
    local cask=$1

    # log function call
    echo "+ caskupdate $@" >> $tmpfile

    # check for versions
    version=$(brew cask info $cask | sed -n "s/$cask:\ \(.*\)/\1/p")
    installed=$(find "/usr/local/Caskroom/$cask" -type d -maxdepth 1 -maxdepth 1 -name "$version")

    if [[ -z $installed ]] ; then
        $blush
        $logprefix echo "$cask requires update." | $logcattee | $logsuffix
        $reset
        sudo printf ""
        $logprefix echo "++ brew cask uninstall $cask --force $verbose $quiet" | $logcattee | $logsuffix
        $logprefix brew cask uninstall --force $cask $verbose $quiet | $logcattee | $logsuffix
        sudo printf ""
        $logprefix echo "++ brew cask install $cask --force $verbose $quiet" | $logcattee | $logsuffix
        $logprefix brew cask install --force $cask $verbose $quiet | $logcattee | $logsuffix
        $logprefix echo | $logcattee | $logsuffix
    else
        $green
        $logprefix echo "$cask is up-to-date." | $logcattee | $logsuffix
        $reset
        $logprefix echo | $logcattee | $logsuffix
    fi
}


# if no outdated packages found
if ( ! $arg_o ) ; then
    $green
    $logprefix echo "All packages have been up-to-date." | $logcattee | $logsuffix
    $reset
else
    # if quiet flag set
    if ( $arg_q ) ; then
        quiet="--quiet"
    else
        quiet=""
    fi

    # if verbose flag set
    if ( $arg_v ) ; then
        verbose="--verbose"
    else
        verbose=""
    fi

    # if force flag set
    if ( $arg_f ) ; then
        force="--force"
    else
        force=""
    fi

    # if greedy flag set
    if ( $arg_g ) ; then
        $logprefix echo "+ brew cask upgrade --greedy $force $verbose $quiet" | $logcattee | $logsuffix
        $logprefix brew cask upgrade --greedy $verbose $forc $quiet | $logcattee | $logsuffix
        $logprefix echo | $logcattee | $logsuffix
    else
        # update procedure
        for name in $arg_pkg ; do
            flag=`brew cask list -1 | awk "/^$name$/"`
            if [[ -nz $flag ]] ; then
                caskupdate $name
            else
                $blush
                $logprefix echo "Error: No available formula with the name $name." | $logcattee | $logsuffix
                $reset

                # did you mean
                dym=`brew cask list -1 | grep $name | xargs | sed "s/ /, /g"`
                if [[ -nz $dym ]] ; then
                    $logprefix echo "Did you mean any of the following casks: $dym?" | $logcattee | $logsuffix
                fi
                $logprefix echo | $logcattee | $logsuffix
            fi
        done
    fi
fi


# read /tmp/log/update.log line by line then migrate to log file
while read -r line ; do
    # plus `+` proceeds in line
    if [[ $line =~ ^(\+\+*\ )(.*)$ ]] ; then
        # add "+" in the beginning, then write to /Library/Logs/Scripts/update/logdate.log
        echo "+$line" >> $logfile
    # minus `-` proceeds in line
    elif [[ $line =~ ^(-\ )(.*)$ ]] ; then
        # replace "-" with "+", then write to /Library/Logs/Scripts/update/logdate.log
        echo "$line" | sed "y/-/+/" >> $logfile
    # colon `:` in line
    elif [[ $line =~ ^([[:alnum:]][[:alnum:]]*)(:)(.*)$ ]] ; then
        # if this is a warning
        if [[ $( tr "[:upper:]" "[:lower:]" <<< $line ) =~ ^([[:alnum:]][[:alnum:]]*:\ )(.*)(warning:\ )(.*) ]] ; then
            # log tag
            prefix="WAR"
            # log content
            suffix=`echo $line | sed "s/\[[0-9][0-9]*m//g" | sed "s/warning: //"`
        # if this is an error
        elif [[ $( tr "[:upper:]" "[:lower:]" <<< $line ) =~ ^([[:alnum:]][[:alnum:]]*:\ )(.*)(error:\ )(.*)$ ]] ; then
            # log tag
            prefix="ERR"
            # log content
            suffix=`echo $line | sed "s/\[[0-9][0-9]*m//g" | sed "s/error: //"`
        # if this is asking for password
        elif [[ $line =~ ^(Password:)(.*) ]] ; then
            # log tag
            prefix="PWD"
            # log content
            suffix="content hidden due to security reasons"
        # otherwise, extract its own tag
        else
            # log tag
            prefix=`echo $line | sed "s/\[[0-9][0-9]*m//g" | sed "s/\(.*\)*:\ .*/\1/" | cut -c 1-3 | tr "[:lower:]" "[:upper:]"`
            # log content
            suffix=`echo $line | sed "s/\[[0-9][0-9]*m//g" | sed "s/.*:\ \(.*\)*.*/\1/"`
        fi
        # write to /Library/Logs/Scripts/update/logdate.log
        echo "$prefix: $suffix" >> $logfile
    # colourised `[??m` line
    elif [[ $line =~ ^(.*)(\[[0-9][0-9]*m)(.*)$ ]] ; then
        # error (red/[31m) line
        if [[ $line =~ ^(.*)(\[31m)(.*)$ ]] ; then
            # add `ERR` tag and remove special characters then write to /Library/Logs/Scripts/update/logdate.log
            echo "ERR: $line" | sed "s/\[[0-9][0-9]*m//g" >> $logfile
        # warning (yellow/[33m)
        elif [[ $line =~ ^(.*)(\[33m)(.*)$ ]] ; then
            # add `WAR` tag and remove special characters then write to /Library/Logs/Scripts/update/logdate.log
            echo "WAR: $line" | sed "s/\[[0-9][0-9]*m//g" >> $logfile
        # other colourised line
        else
            # add `INF` tag and remove special characters then write to /Library/Logs/Scripts/update/logdate.log
            echo "INF: $line" | sed "s/\[[0-9][0-9]*m//g" >> $logfile
        fi
    # empty / blank line
    elif [[ $line =~ ^([[:space:]]*)$ ]] ; then
        # directlywrite to /Library/Logs/Scripts/update/logdate.log
        echo $line >> $logfile
    # non-empty line
    else
        # add `OUT` tag, remove special characters and discard flushed lines then write to /Library/Logs/Scripts/update/logdate.log
        echo "OUT: $line" | sed "s/\[\?[0-9][0-9]*[a-zA-Z]//g" | sed "/\[[A-Z]/d" | sed "/##*\ \ *.*%/d" >> $logfile
    fi
done < $tmpfile


# remove /tmp/log/update.log
rm -f $tmpfile


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1
