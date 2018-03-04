#!/bin/bash


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1


# preset terminal output colours
blush="tput setaf 1"    # blush / red
green="tput setaf 2"    # green
reset="tput sgr0"       # reset


################################################################################
# Uninstall Homebrew packages.
#
# Parameter list:
#   1. Log Date
#   2. Force Flag
#   3. Quiet Flag
#   4. Verbose Flag
#   5. Ignore-Dependencies Flag
#   6. Yes Flag
#   7. Package
#       ............
################################################################################


# parameter assignment
logdate=$1
arg_f=$2
arg_q=$3
arg_v=$4
arg_i=$5
arg_Y=$6
arg_pkg=${*:7}


# log file prepare
logfile="/Library/Logs/Scripts/uninstall/$logdate.log"
tmpfile="/tmp/log/uninstall.log"


# remove /tmp/log/uninstall.log
rm -f $tmpfile


# create /tmp/log/uninstall.log & /Library/Logs/Scripts/uninstall/logdate.log
touch $logfile
touch $tmpfile


# log current status
echo "- /bin/bash $0 $@" >> $tmpfile


# log commands
# usage: $logprefix [command] | logcattee | logsuffix
logprefix="script -q /dev/null"
logcattee="tee -a $tmpfile"
if ( $arg_q ) ; then
    logsuffix="grep ^$"
else
    logsuffix="grep ^.*$"
fi


# brew fix missing function usage
#   brew_fixmissing packages
function brew_fixmissing {
    # parameter assignment
    local arg_pkg=${*:1}

    # reinstall missing packages
    for $name in $arg_pkg ; do
        $logprefix echo "+ brew install $name $force $verbose $quiet" | $logcattee | $logsuffix
        $logprefix brew install $name $force $verbose $quiet | $logcattee | $logsuffix
        $logprefix echo | $logcattee | $logsuffix
    done

    # inform if missing packages fixed
    $green
    $logprefix echo "All missing packages installed." | $logcattee | $logsuffix
    $reset
    $logprefix echo | $logcattee | $logsuffix
}


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


# uninstall procedure
for name in $arg_pkg ; do
    case $name in
        all)
            list=`brew list -1`
            for pkg in $list; do
                $logprefix echo "+ brew uninstall $pkg --ignore-dependencies $force $verbose $quiet" | $logcattee | $logsuffix
                $logprefix brew uninstall $pkg --ignore-dependencies $force $verbose $quiet | $logcattee | $logsuffix
                $logprefix echo | $logcattee | $logsuffix
            done ;;
        *)
            # check if package installed
            if brew list --versions $name > /dev/null ; then
                # along with dependencies or not
                $logprefix echo "+ brew uninstall $name --ignore-dependencies $force $verbose $quiet" | $logcattee | $logsuffix
                $logprefix brew uninstall $name --ignore-dependencies $force $verbose $quiet | $logcattee | $logsuffix
                $logprefix echo | $logcattee | $logsuffix

                # if ignore-dependencies flag not set
                if ( ! $arg_i ) ; then
                    list=`brew deps $name`
                    for pkg in $list; do
                        # check if package installed
                        if brew list --versions $pkg > /dev/null ; then
                            $logprefix echo "+ brew uninstall $pkg --ignore-dependencies $force $verbose $quiet" | $logcattee | $logsuffix
                            $logprefix brew uninstall $pkg --ignore-dependencies $force $verbose $quiet | $logcattee | $logsuffix
                            $logprefix echo | $logcattee | $logsuffix
                        fi
                    done
                fi
            else
                $blush
                $logprefix echo "Error: No available formula with the name $name." | $logcattee | $logsuffix
                $reset

                # did you mean
                dym=`brew list -1 | grep $name | xargs | sed "s/ /, /g"`
                if [[ -nz $dym ]] ; then
                    $logprefix echo "Did you mean any of the following packages: $dym?" | $logcattee | $logsuffix
                fi
                $logprefix echo | $logcattee | $logsuffix
            fi ;;
    esac
done


# fix missing brew dependencies
miss=`brew missing | sed "s/.*: \(.*\)*/\1/" | sort -u | xargs`
if [[ -nz $miss ]] ; then
    $logprefix echo "Required packages found missing: ${blush}${miss}${reset}" | $logcattee | $logsuffix
    if ( $arg_Y ) ; then
        brew_fixmissing $miss
    else
        while true ; do
            read -p "Would you like to reinstall? (y/N)" yn
            case $yn in
                [Yy]* )
                    brew_fixmissing $miss
                    break ;;
                [Nn]* )
                    $blush
                    $logprefix echo "Missing packages unfixed." | $logcattee | $logsuffix
                    $reset
                    break ;;
                * )
                    echo "Invalid choice." ;;
            esac
        done
    fi
fi


# read /tmp/log/uninstall.log line by line then migrate to log file
while read -r line ; do
    # plus `+` proceeds in line
    if [[ $line =~ ^(\+\+*\ )(.*)$ ]] ; then
        # add "+" in the beginning, then write to /Library/Logs/Scripts/uninstall/logdate.log
        echo "+$line" >> $logfile
    # minus `-` proceeds in line
    elif [[ $line =~ ^(-\ )(.*)$ ]] ; then
        # replace "-" with "+", then write to /Library/Logs/Scripts/uninstall/logdate.log
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
        # write to /Library/Logs/Scripts/uninstall/logdate.log
        echo "$prefix: $suffix" >> $logfile
    # colourised `[??m` line
    elif [[ $line =~ ^(.*)(\[[0-9][0-9]*m)(.*)$ ]] ; then
        # error (red/[31m) line
        if [[ $line =~ ^(.*)(\[31m)(.*)$ ]] ; then
            # add `ERR` tag and remove special characters then write to /Library/Logs/Scripts/uninstall/logdate.log
            echo "ERR: $line" | sed "s/\[[0-9][0-9]*m//g" >> $logfile
        # warning (yellow/[33m)
        elif [[ $line =~ ^(.*)(\[33m)(.*)$ ]] ; then
            # add `WAR` tag and remove special characters then write to /Library/Logs/Scripts/uninstall/logdate.log
            echo "WAR: $line" | sed "s/\[[0-9][0-9]*m//g" >> $logfile
        # other colourised line
        else
            # add `INF` tag and remove special characters then write to /Library/Logs/Scripts/uninstall/logdate.log
            echo "INF: $line" | sed "s/\[[0-9][0-9]*m//g" >> $logfile
        fi
    # empty / blank line
    elif [[ $line =~ ^([[:space:]]*)$ ]] ; then
        # directlywrite to /Library/Logs/Scripts/uninstall/logdate.log
        echo $line >> $logfile
    # non-empty line
    else
        # add `OUT` tag, remove special characters and discard flushed lines then write to /Library/Logs/Scripts/uninstall/logdate.log
        echo "OUT: $line" | sed "s/\[\?[0-9][0-9]*[a-zA-Z]//g" | sed "/\[[A-Z]/d" | sed "/##*\ \ *.*%/d" >> $logfile
    fi
done < $tmpfile


# remove /tmp/log/uninstall.log
rm -f $tmpfile


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1
