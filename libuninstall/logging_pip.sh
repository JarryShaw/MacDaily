#!/bin/bash


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1


################################################################################
# Log Python site packages uninstall dependencies.
#
# Parameter list:
#   1. Log Date
#   2. System Flag
#   3. Cellar Flag
#   4. CPython Flag
#   5. PyPy Flag
#   6. Version
#       |-> 1 : Both
#       |-> 2 : Python 2.*
#       |-> 3 : Python 3.*
#   7. Ignore-Dependencies Flag
#   8. Package
#       ............
################################################################################


# parameter assignment
logdate=$1
arg_s=$2
arg_b=$3
arg_c=$4
arg_y=$5
arg_V=$6
arg_i=$7
arg_pkg=${*:8}


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
logprefix="script -q /dev/null"
logcattee="tee -a $tmpfile"
logsuffix="grep ^.*$"


# pip logging function usage:
#   piplogging mode
function piplogging {
    # parameter assignment
    local mode=$1

    # log function call
    echo "+ piplogging $@" >> $tmpfile


    # make prefix & suffix of pip
    case $mode in
        1)  # pip_sys
            prefix="/Library/Frameworks/Python.framework/Versions/2.7/bin"
            suffix=""
            pprint="_sys" ;;
        2)  # pip_sys3
            prefix="/Library/Frameworks/Python.framework/Versions/3.6/bin"
            suffix="3"
            pprint="_sys3" ;;
        3)  # pip
            prefix="/usr/local/opt/python2/bin"
            suffix=""
            pprint="" ;;
        4)  # pip3
            prefix="/usr/local/opt/python3/bin"
            suffix="3"
            pprint="3" ;;
        5)  # pip_pypy
            prefix="/usr/local/opt/pypy2/bin"
            suffix="_pypy"
            pprint="_pypy" ;;
        6)  # pip_pypy3
            prefix="/usr/local/opt/pypy3/bin"
            suffix="_pypy3"
            pprint="_pypy3" ;;
    esac

    # if executive exits
    if [ -e $prefix/pip$suffix ] ; then
        # check dependencies for each package
        for name in $arg_pkg ; do
            case $name in
                all)
                    echo -e "++ pip$pprint list --format legacy | sed \"s/\(.*\)* (.*).*/\1/\"" >> $tmpfile
                    $logprefix $prefix/pip$suffix list --format legacy | sed "s/\(.*\)* (.*).*/\1/" | $logcattee | $logsuffix
                    echo >> $tmpfile ;;
                *)
                    # check if package installed
                    flag=`$prefix/pip$suffix list --format legacy | awk "/^$name$/"`
                    if [[ -nz $flag ]]; then
                        echo -e "++ pip$pprint show $name | grep \"Name: \" | sed \"s/Name: //\"" >> $tmpfile
                        $logprefix $prefix/pip$suffix show $name | grep "Name: " | sed "s/Name: //" | $logcattee | $logsuffix
                        echo >> $tmpfile

                        # if ignore-dependencies flag not set
                        if ( ! $arg_i ) ; then
                            echo -e "++ pip$pprint show $name | grep \"Requires: \" | sed \"s/Requires: //\" | sed \"s/,//g\"" >> $tmpfile
                            $logprefix $prefix/pip$suffix show $name | grep "Requires: " | sed "s/Requires: //" | sed "s/,//g" | $logcattee | $logsuffix
                            echo >> $tmpfile
                        fi
                    else
                        echo -e "Error: No pip$pprint package names $name installed.\n" >> $tmpfile
                    fi ;;
            esac
        done
    else
        echo -e "$prefix/pip$suffix: No such file or directory.\n" >> $tmpfile
    fi
}


# preset all mode bools
mode_pip_sys=false      # 2.* / system / cpython
mode_pip_sys3=false     # 3.* / system / cpython
mode_pip=false          # 2.* / cellar / cpython
mode_pip3=false         # 3.* / cellar / cpython
mode_pip_pypy=false     # 2.* / cellar / pypy
mode_pip_pypy3=false    # 3.* / cellar / pypy


# if system flag set
if ( $arg_s ) ; then
    case $arg_V in
        1)  mode_pip_sys=true
            mode_pip_sys3=true ;;
        2)  mode_pip_sys=true ;;
        3)  mode_pip_sys3=true ;;
    esac
fi


# if cellar flag set
if ( $arg_b ) ; then
    case $arg_V in
        1)  mode_pip=true
            mode_pip3=true
            mode_pip_pypy=true
            mode_pip_pypy3=true ;;
        2)  mode_pip=true
            mode_pip_pypy=true ;;
        3)  mode_pip3=true
            mode_pip_pypy3=true ;;
    esac
fi


# if cpython flag set
if ( $arg_c ) ; then
    case $arg_V in
        1)  mode_pip_sys=true
            mode_pip_sys3=true
            mode_pip=true
            mode_pip3=true ;;
        2)  mode_pip_sys=true
            mode_pip=true ;;
        3)  mode_pip_sys3=true
            mode_pip3=true ;;
    esac
fi


# if pypy flag set
if ( $arg_y ) ; then
    case $arg_V in
        1)  mode_pip_pypy=true
            mode_pip_pypy3=true ;;
        2)  mode_pip_pypy=true ;;
        3)  mode_pip_pypy3=true ;;
    esac
fi


# call piplogging function according to modes
list=( [1]=$mode_pip_sys $mode_pip_sys3 $mode_pip $mode_pip3 $mode_pip_pypy $mode_pip_pypy3 )
for index in ${!list[*]} ; do
    if ( ${list[$index]} ) ; then
        piplogging $index
    fi
done


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
