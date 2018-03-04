#!/bin/bash


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1


# preset terminal output colours
blush="tput setaf 1"    # blush / red
green="tput setaf 2"    # green
reset="tput sgr0"       # reset


################################################################################
# Log Python site packages uninstallation.
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
#   7. Quiet Flag
#   8. Verbose Flag
#   9. Yes Flag
#  10. Ignore-Dependencies Flag
#  11. Package
#       ............
################################################################################


# parameter assignment
logdate=$1
arg_s=$2
arg_b=$3
arg_c=$4
arg_y=$5
arg_V=$6
arg_q=$7
arg_v=$8
arg_Y=$9
arg_i=$10
arg_pkg=${*:11}


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


# pip uninstall function usage
#   pipuninstall package pip-suffix pip-suffix pip-pprint
function pipuninstall {
    # parameter assignment
    local arg_pkg=$1
    local prefix=$2
    local suffix=$3
    local pprint=$4

    # log function call
    echo "+ pipuninstall $@" >> $tmpfile

    # uninstall procedure
    $logprefix echo "++ pip$pprint uninstall $arg_pkg --yes $verbose $quiet" | $logcattee | $logsuffix
    $logprefix $prefix/pip$suffix uninstall $arg_pkg --yes $verbose $quiet | $logcattee | $logsuffix
    $logprefix echo | $logcattee | $logsuffix

    # if ignore-dependencies flag not set
    if ( ! $arg_i ) ; then
        list=`$prefix/pip$suffix show $arg_pkg | grep "Requires: " | sed "s/Requires: //" | sed "s/,//g"`
        for name in $arg_pkg ; do
            # check if package installed
            flag=`$prefix/pip$suffix list --format legacy | awk "/^$name$/"`
            if [[ -nz $flag ]]; then
                $logprefix echo "++ pip$pprint uninstall $name --yes $verbose $quiet" | $logcattee | $logsuffix
                $logprefix $prefix/pip$suffix uninstall $name --yes $verbose $quiet | $logcattee | $logsuffix
                $logprefix echo | $logcattee | $logsuffix
            fi
        done
    fi
}


# pip fix missing function usage
#   pip_fixmissing pip-prefix pip-suffix pip-pprint packages
function pip_fixmissing {
    # parameter assignment
    local prefix=$1
    local suffix=$2
    local pprint=$3
    local arg_pkg=${*:4}

    # log function call
    echo "+ pip_fixmissing $@" >> $tmpfile

    # reinstall missing packages
    for $name in $arg_pkg ; do
        $logprefix echo "++ pip$pprint install $name --no-cache-dir $verbose $quiet" | $logcattee | $logsuffix
        $logprefix $prefix/pip$suffix install $name --no-cache-dir $verbose $quiet | $logcattee | $logsuffix
        $logprefix echo | $logcattee | $logsuffix
    done

    # inform if missing packages fixed
    $green
    $logprefix echo "All missing pip$pprint packages installed." | $logcattee | $logsuffix
    $reset
    $logprefix echo | $logcattee | $logsuffix
}


# pip logging function usage:
#   piplogging mode
function piplogging {
    # parameter assignment
    mode=$1

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
        for name in $arg_pkg ; do
            # All or Specified Packages
            case $name in
                all)
                    # list=`pipdeptree$pprint | grep -e "==" | grep -v "required"`
                    list=`$prefix/pip$suffix list --format legacy | sed "s/\(.*\)* (.*).*/\1/"`
                    for pkg in $list ; do
                        case $pkg in
                            # keep fundamental packages
                            pip|setuptools|wheel)
                                : ;;
                            *)
                                if ( $arg_Y ) ; then
                                    $logprefix echo "++ pip$pprint uninstall $pkg --yes $verbose $quiet" | $logcattee | $logsuffix
                                    $logprefix $prefix/pip$suffix uninstall $pkg --yes $verbose $quiet | $logcattee | $logsuffix
                                    $logprefix echo | $logcattee | $logsuffix
                                else
                                    while true ; do
                                        # ask for confirmation
                                        read -p "Would you like to uninstall $pkg? (y/N)" yn
                                        case $yn in
                                            [Yy]*)
                                                $logprefix echo "++ pip$pprint uninstall $pkg --yes $verbose $quiet" | $logcattee | $logsuffix
                                                $logprefix $prefix/pip$suffix uninstall $pkg --yes $verbose $quiet | $logcattee | $logsuffix
                                                $logprefix echo | $logcattee | $logsuffix
                                                break ;;
                                            [Nn]*)
                                                $blush
                                                $logprefix echo "Uninstall procedure for $pkg declined." | $logcattee | $logsuffix
                                                $reset
                                                break ;;
                                            * )
                                                echo "Invalid choice." ;;
                                        esac
                                    done
                                fi ;;
                        esac
                    done ;;
                # keep fundamental packages
                pip|setuptools|wheel)
                    : ;;
                *)
                    # check if package installed
                    flag=`$prefix/pip$suffix list --format legacy | awk "/^$name$/"`
                    if [[ -nz $flag ]]; then
                        if ( $arg_Y ) ; then
                            pipuninstall $name $prefix $suffix $pprint
                        else
                            while true ; do
                                # ask for confirmation
                                read -p "Would you like to uninstall $name? (y/N)" yn
                                case $yn in
                                    [Yy]*)
                                        pipuninstall $name $prefix $suffix $pprint
                                        break ;;
                                    [Nn]*)
                                        $blush
                                        $logprefix echo "Uninstall procedure for $name declined." | $logcattee | $logsuffix
                                        $reset
                                        break ;;
                                    * )
                                        echo "Invalid choice." ;;
                                esac
                            done
                        fi
                    else
                        $blush
                        $logprefix echo "Error: No pip$pprint package names $name installed." | $logcattee | $logsuffix
                        $reset

                        # did you mean
                        dym=`$prefix/pip$suffix list --format legacy | sed "s/\(.*\)* (.*).*/\1/" | grep $name | xargs | sed "s/ /, /g"`
                        if [[ -nz $dym ]] ; then
                            $logprefix echo "Did you mean any of the following packages: $dym?" | $logcattee | $logsuffix
                        fi
                        $logprefix echo | $logcattee | $logsuffix
                    fi ;;
            esac
        done

        # fix missing package dependencies
        miss=`$prefix/pip$suffix check | grep "requires" | sed "s/.* requires \(.*\)*, .*/\1/" | sort -u | xargs`
        if [[ -nz $miss ]] ; then
            $blush
            $logprefix echo "Required pip$pprint packages found missing: $miss" | $logcattee | $logsuffix
            $reset
            if ( $arg_Y ) ; then
                pip_fixmissing $prefix $suffix $pprint $miss
            else
                while true ; do
                    read -p "Would you like to reinstall? (y/N)" yn
                    case $yn in
                        [Yy]* )
                            pip_fixmissing $prefix $suffix $pprint $miss
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
            $logprefix echo | $logcattee | $logsuffix
        fi
    else
        echo -e "$prefix/pip$suffix: No such file or directory.\n" >> $tmpfile
    fi
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
