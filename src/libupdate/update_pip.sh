#!/bin/bash


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1


# terminal display
reset="\033[0m"         # reset
bold="\033[1m"          # bold
under="\033[4m"         # underline
red="\033[91m"          # bright red foreground
green="\033[92m"        # bright green foreground
yellow="\033[93m"       # bright yellow foreground


################################################################################
# Check Python site packages updates.
#
# Parameter list:
#   1. Encrypted Password
#   2. Log File
#   3. Temp File
#   4. System Flag
#   5. Cellar Flag
#   6. CPython Flag
#   7. PyPy Flag
#   8. Version
#       |-> 0  : None
#       |-> 1  : All
#       |-> 2  : Python 2.*
#       |-> 20 : Python 2.0.*
#       |-> 21 : Python 2.1.*
#       |-> 22 : Python 2.2.*
#       |-> 23 : Python 2.3.*
#       |-> 24 : Python 2.4.*
#       |-> 25 : Python 2.5.*
#       |-> 26 : Python 2.6.*
#       |-> 27 : Python 2.7.*
#       |-> 3  : Python 3.*
#       |-> 31 : Python 3.1.*
#       |-> 32 : Python 3.2.*
#       |-> 33 : Python 3.3.*
#       |-> 34 : Python 3.4.*
#       |-> 35 : Python 3.5.*
#       |-> 36 : Python 3.6.*
#       |-> 37 : Python 3.7.*
#   9. Yes Flag
#  10. Quiet Flag
#  11. Verbose Flag
#  12. Pre-release Flag
#  13. Package
#       ............
################################################################################


# parameter assignment
password=`python -c "print(__import__('base64').b64decode(__import__('sys').stdin.readline().strip()).decode())" <<< $1`
# echo $1 | cut -c2- | rev | cut -c2- | rev
logfile=`python -c "print(__import__('sys').stdin.readline().strip().strip('\''))" <<< $2`
tmpfile=`python -c "print(__import__('sys').stdin.readline().strip().strip('\''))" <<< $3`
arg_s=$4
arg_b=$5
arg_c=$6
arg_y=$7
arg_V=$8
arg_Y=$9
arg_q=${10}
arg_v=${11}
arg_P=${12}
arg_pkg=${*:13}


# remove /tmp/log/update.log
rm -f "$tmpfile"


# create /tmp/log/update.log & /Library/Logs/Scripts/update/logdate/logtime.log
touch "$logfile"
touch "$tmpfile"


# log current status
echo "- /bin/bash $0 $@" >> "$tmpfile"


# log commands
logprefix="script -aq "$tmpfile""
if ( $arg_q ) ; then
    logsuffix="grep ^$"
else
    logsuffix="grep ^.*$"
fi


# pip fix broken function usage
#   pip_fixbroken pip-prefix pip-suffix pip-pprint packages
function pip_fixbroken {
    # parameter assignment
    local prefix=$1
    local suffix=$2
    local pprint=$3
    local arg_pkg=${*:4}

    # log function call
    echo "+ pip_fixbroken $@" >> "$tmpfile"

    # reinstall broken dependencies
    for pkg in $arg_pkg ; do
        # ask for password up-front
        sudo --reset-timestamp
        sudo --stdin --validate <<< $password ; echo

        $logprefix printf "++ ${bold}pip$pprint reinstall --no-cache-dir --ignore-installed $pkg $pre $verbose $quiet${reset}\n" | $logsuffix
        if ( $arg_q ) ; then
            sudo --set-home $logprefix $prefix/$suffix -m pip uninstall --yes $pkg $verbose $quiet > /dev/null 2>&1
            sudo --set-home $logprefix $prefix/$suffix -m pip install --ignore-installed --no-cache-dir $pre $pkg $verbose $quiet > /dev/null 2>&1
        else
            sudo --set-home $logprefix $prefix/$suffix -m pip uninstall --yes $pkg $verbose $quiet
            sudo --set-home $logprefix $prefix/$suffix -m pip install --ignore-installed --no-cache-dir $pre $pkg $verbose $quiet
        fi
        $logprefix echo | $logsuffix
    done

    # recursively fix broken package dependencies
    tmparg=`$prefix/$suffix -m pip check 2>/dev/null | grep "has requirement" | sed "s/.* has requirement \(.*\)*, .*/\1/" | sort -u | xargs`
    if [[ ! -z $tmparg ]]; then
    	pip_fixbroken $prefix $suffix $pprint $tmparg
    fi
}


# pip update function usage:
#   pipupdate mode
function pipupdate {
    # parameter assignment
    mode=$1

    # log function call
    echo "+ pipupdate $@" >> "$tmpfile"

    # make prefix & suffix of pip
    case $mode in
        1)  # pip2.0
            prefix="/Library/Frameworks/Python.framework/Versions/2.0/bin"
            suffix="python2.0"
            pprint="2.0" ;;
        2)  # pip2.1
            prefix="/Library/Frameworks/Python.framework/Versions/2.1/bin"
            suffix="python2.1"
            pprint="2.1" ;;
        3)  # pip2.2
            prefix="/Library/Frameworks/Python.framework/Versions/2.2/bin"
            suffix="python2.2"
            pprint="2.2" ;;
        4)  # pip2.3
            prefix="/Library/Frameworks/Python.framework/Versions/2.3/bin"
            suffix="python2.3"
            pprint="2.3" ;;
        5)  # pip2.4
            prefix="/Library/Frameworks/Python.framework/Versions/2.4/bin"
            suffix="python2.4"
            pprint="2.4" ;;
        6)  # pip2.5
            prefix="/Library/Frameworks/Python.framework/Versions/2.5/bin"
            suffix="python2.5"
            pprint="2.5" ;;
        7)  # pip2.6
            prefix="/Library/Frameworks/Python.framework/Versions/2.6/bin"
            suffix="python2.6"
            pprint="2.6" ;;
        8)  # pip2.7
            prefix="/Library/Frameworks/Python.framework/Versions/2.7/bin"
            suffix="python2.7"
            pprint="2.7" ;;
        9)  # pip3.0
            prefix="/Library/Frameworks/Python.framework/Versions/3.0/bin"
            suffix="python3.0"
            pprint="3.0" ;;
        10)  # pip3.1
            prefix="/Library/Frameworks/Python.framework/Versions/3.1/bin"
            suffix="python3.1"
            pprint="3.1" ;;
        11)  # pip3.2
            prefix="/Library/Frameworks/Python.framework/Versions/3.2/bin"
            suffix="python3.2"
            pprint="3.2" ;;
        12)  # pip3.3
            prefix="/Library/Frameworks/Python.framework/Versions/3.3/bin"
            suffix="python3.3"
            pprint="3.3" ;;
        13)  # pip3.4
            prefix="/Library/Frameworks/Python.framework/Versions/3.4/bin"
            suffix="python3.4"
            pprint="3.4" ;;
        14)  # pip3.5
            prefix="/Library/Frameworks/Python.framework/Versions/3.5/bin"
            suffix="python3.5"
            pprint="3.5" ;;
        15)  # pip3.6
            prefix="/Library/Frameworks/Python.framework/Versions/3.6/bin"
            suffix="python3.6"
            pprint="3.6" ;;
        16)  # pip3.7
            prefix="/Library/Frameworks/Python.framework/Versions/3.7/bin"
            suffix="python3.7"
            pprint="3.7" ;;
        17)  # pip2
            prefix="/usr/local/opt/python@2/bin"
            suffix="python2"
            pprint="2" ;;
        18)  # pip3
            prefix="/usr/local/opt/python@3/bin"
            suffix="python3"
            pprint="3" ;;
        19)  # pip_pypy
            prefix="/usr/local/opt/pypy/bin"
            suffix="pypy"
            pprint="_pypy" ;;
        20)  # pip_pypy3
            prefix="/usr/local/opt/pypy3/bin"
            suffix="pypy3"
            pprint="_pypy3" ;;
    esac

    # if executive exits
    if [ -e $prefix/$suffix ] ; then
        updated=true
        for name in $arg_pkg ; do
            # All or Specified Packages
            case $name in
                all)
                    # list=`pipdeptree$pprint | grep -e "==" | grep -v "required"`
                    list=`$prefix/$suffix -m pip list --no-cache-dir --format freeze --outdated $pre 2>/dev/null | grep "==" | sed "s/\(.*\)*==.*/\1/"`
                    if [[ ! -z $list ]] ; then
                        for pkg in $list ; do
                            case $pkg in
                                macdaily )
                                    $logprefix printf "update: ${yellow}pip${reset}: pip$pprint package \`${bold}${under}macdaily${reset}\` is to update after\n\n" | $logsuffix ;;
                                * )
                                    # ask for password up-front
                                    sudo --reset-timestamp
                                    sudo --stdin --validate <<< $password ; echo

                                    $logprefix printf "++ ${bold}pip$pprint install --upgrade --no-cache-dir $pkg $pre $verbose $quiet${reset}\n" | $logsuffix
                                    if ( $arg_q ) ; then
                                        sudo --set-home $logprefix $prefix/$suffix -m pip install --upgrade --no-cache-dir $pkg $pre $verbose $quiet > /dev/null 2>&1
                                    else
                                        sudo --set-home $logprefix $prefix/$suffix -m pip install --upgrade --no-cache-dir $pkg $pre $verbose $quiet
                                    fi
                                    $logprefix echo | $logsuffix ;;
                            esac
                        done
                    else
                        $logprefix printf "update: ${green}pip${reset}: all ${bold}pip$pprint packages${reset} have been up-to-date\n\n" | $logsuffix
                    fi ;;
                *)
                    flag=`$prefix/$suffix -m pip list --no-cache-dir --format freeze 2>/dev/null | grep "==" | sed "s/\(.*\)*==.*/\1/" | awk "/^$name$/"`
                    if [[ ! -z $flag ]]; then
                        # ask for password up-front
                        sudo --reset-timestamp
                        sudo --stdin --validate <<< $password ; echo

                        $logprefix printf "++ ${bold}pip$pprint install --upgrade --no-cache-dir $name $pre $verbose $quiet${reset}\n" | $logsuffix
                        if ( $arg_q ) ; then
                            sudo --set-home $logprefix $prefix/$suffix -m pip install --upgrade --no-cache-dir $name $pre $verbose $quiet > /dev/null 2>&1
                        else
                            sudo --set-home $logprefix $prefix/$suffix -m pip install --upgrade --no-cache-dir $name $pre $verbose $quiet
                        fi
                        $logprefix echo | $logsuffix
                    else
                        $logprefix printf "update: ${yellow}pip${reset}: no pip$pprint package names ${red}$name${reset} installed\n" | $logsuffix

                        # did you mean
                        tmp=`$prefix/$suffix -m pip list --no-cache-dir --format freeze 2>/dev/null | grep "==" | sed "s/\(.*\)*==.*/\1/" | grep $name | xargs`
                        if [[ ! -z $tmp ]] ; then
                            dym=`python -c "print('${red}' + '${reset}, ${red}'.join(__import__('sys').stdin.read().strip().split()) + '${reset}')" <<< $tmp`
                            $logprefix printf "update: ${yellow}pip${reset}: did you mean any of the following packages: $dym?\n" | $logsuffix
                        fi
                        $logprefix echo | $logsuffix
                    fi ;;
            esac
        done

        # fix broken package dependencies
        tmparg=`$prefix/$suffix -m pip check 2>/dev/null | grep "has requirement" | sed "s/.* has requirement \(.*\)*, .*/\1/" | sort -u | xargs`
        if [[ ! -z $tmparg ]]; then
            broken=`python -c "print('${red}' + '${reset}, ${red}'.join([ __import__('re').split('[>=<]', item)[0] for item in __import__('sys').stdin.read().strip().split() ]) + '${reset}')" <<< $tmparg`
            $logprefix printf "update: ${red}pip${reset}: dependency ${bold}pip$pprint packages${reset} found broken: $broken\n" | $logsuffix
            if ( $arg_Y || $arg_q ) ; then
                $logprefix echo | $logsuffix
                pip_fixbroken $prefix $suffix $pprint $tmparg
                $logprefix printf "update: ${green}pip${reset}: all broken ${bold}pip$pprint${reset} dependencies fixed\n" | $logsuffix
            else
                while true ; do
                    read -p "Would you like to reinstall? (y/N)" yn
                    case $yn in
                        [Yy]* )
                            $logprefix echo | $logsuffix
                            pip_fixbroken $prefix $suffix $pprint $tmparg
						    $logprefix printf "update: ${green}pip${reset}: all broken ${bold}pip$pprint${reset} dependencies fixed\n" | $logsuffix
                            break ;;
                        [Nn]* )
                            $logprefix printf "update: ${red}pip${reset}: broken dependencies remain\n" | $logsuffix
                            break ;;
                        * )
                            printf "update: ${red}pip${reset}: invalid choice\n" ;;
                    esac
                done
            fi
            $logprefix echo | $logsuffix
        fi
    else
        printf "update: pip: pip$pprint not installed.\n\n" >> "$tmpfile"
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


# if pre-release flag set
if ( $arg_P ) ; then
    pre="--pre"
else
    pre=""
fi


# updated flag
updated=false


# preset all mode bools
mode_pip_sys20=false    # 2.0.* / system / cpython
mode_pip_sys21=false    # 2.1.* / system / cpython
mode_pip_sys22=false    # 2.2.* / system / cpython
mode_pip_sys23=false    # 2.3.* / system / cpython
mode_pip_sys24=false    # 2.4.* / system / cpython
mode_pip_sys25=false    # 2.5.* / system / cpython
mode_pip_sys26=false    # 2.6.* / system / cpython
mode_pip_sys27=false    # 2.7.* / system / cpython
mode_pip_sys30=false    # 3.0.* / system / cpython
mode_pip_sys31=false    # 3.1.* / system / cpython
mode_pip_sys32=false    # 3.2.* / system / cpython
mode_pip_sys33=false    # 3.3.* / system / cpython
mode_pip_sys34=false    # 3.4.* / system / cpython
mode_pip_sys35=false    # 3.5.* / system / cpython
mode_pip_sys36=false    # 3.6.* / system / cpython
mode_pip_sys37=false    # 3.7.* / system / cpython
mode_pip_brew2=false    # 2.* / cellar / cpython
mode_pip_brew3=false    # 3.* / cellar / cpython
mode_pip_pypy2=false    # 2.* / cellar / pypy
mode_pip_pypy3=false    # 3.* / cellar / pypy


# if system flag set
if ( $arg_s ) ; then
    case $arg_V in
        1)  mode_pip_sys20=true
            mode_pip_sys21=true
            mode_pip_sys22=true
            mode_pip_sys23=true
            mode_pip_sys24=true
            mode_pip_sys25=true
            mode_pip_sys26=true
            mode_pip_sys27=true
            mode_pip_sys30=true
            mode_pip_sys31=true
            mode_pip_sys32=true
            mode_pip_sys33=true
            mode_pip_sys34=true
            mode_pip_sys35=true
            mode_pip_sys36=true
            mode_pip_sys37=true ;;
        2)  mode_pip_sys20=true
            mode_pip_sys21=true
            mode_pip_sys22=true
            mode_pip_sys23=true
            mode_pip_sys24=true
            mode_pip_sys25=true
            mode_pip_sys26=true
            mode_pip_sys27=true ;;
        20) mode_pip_sys20=true ;;
        21) mode_pip_sys21=true ;;
        22) mode_pip_sys22=true ;;
        23) mode_pip_sys23=true ;;
        24) mode_pip_sys24=true ;;
        25) mode_pip_sys25=true ;;
        26) mode_pip_sys26=true ;;
        27) mode_pip_sys27=true ;;
        3)  mode_pip_sys30=true
            mode_pip_sys31=true
            mode_pip_sys32=true
            mode_pip_sys33=true
            mode_pip_sys34=true
            mode_pip_sys35=true
            mode_pip_sys36=true
            mode_pip_sys37=true ;;
        30) mode_pip_sys30=true ;;
        31) mode_pip_sys31=true ;;
        32) mode_pip_sys32=true ;;
        33) mode_pip_sys33=true ;;
        34) mode_pip_sys34=true ;;
        35) mode_pip_sys35=true ;;
        36) mode_pip_sys36=true ;;
        37) mode_pip_sys37=true ;;
    esac
fi


# if cellar flag set
if ( $arg_b ) ; then
    case $arg_V in
        1)  mode_pip_brew2=true
            mode_pip_brew3=true
            mode_pip_pypy2=true
            mode_pip_pypy3=true ;;
        2)  mode_pip_brew2=true
            mode_pip_pypy2=true ;;
        3)  mode_pip_brew3=true
            mode_pip_pypy3=true ;;
    esac
fi


# if cpython flag set
if ( $arg_c ) ; then
    case $arg_V in
        1)  mode_pip_sys20=true
            mode_pip_sys21=true
            mode_pip_sys22=true
            mode_pip_sys23=true
            mode_pip_sys24=true
            mode_pip_sys25=true
            mode_pip_sys26=true
            mode_pip_sys27=true
            mode_pip_sys30=true
            mode_pip_sys31=true
            mode_pip_sys32=true
            mode_pip_sys33=true
            mode_pip_sys34=true
            mode_pip_sys35=true
            mode_pip_sys36=true
            mode_pip_sys37=true
            mode_pip_brew2=true
            mode_pip_brew3=true ;;
        2)  mode_pip_sys20=true
            mode_pip_sys21=true
            mode_pip_sys22=true
            mode_pip_sys23=true
            mode_pip_sys24=true
            mode_pip_sys25=true
            mode_pip_sys26=true
            mode_pip_sys27=true
            mode_pip_brew2=true ;;
        3)  mode_pip_sys30=true
            mode_pip_sys31=true
            mode_pip_sys32=true
            mode_pip_sys33=true
            mode_pip_sys34=true
            mode_pip_sys35=true
            mode_pip_sys36=true
            mode_pip_sys37=true
            mode_pip_brew3=true ;;
    esac
fi


# if pypy flag set
if ( $arg_y ) ; then
    case $arg_V in
        1)  mode_pip_pypy2=true
            mode_pip_pypy3=true ;;
        2)  mode_pip_pypy2=true ;;
        3)  mode_pip_pypy3=true ;;
    esac
fi


# call piplogging function according to modes
list=( \
    [1]=$mode_pip_sys20 $mode_pip_sys21 $mode_pip_sys22 $mode_pip_sys23 $mode_pip_sys24 $mode_pip_sys25 $mode_pip_sys26 $mode_pip_sys27 \
        $mode_pip_sys30 $mode_pip_sys31 $mode_pip_sys32 $mode_pip_sys33 $mode_pip_sys34 $mode_pip_sys35 $mode_pip_sys36 $mode_pip_sys37 \
        $mode_pip_brew2 $mode_pip_brew3 $mode_pip_pypy2 $mode_pip_pypy3 \
)
for index in ${!list[*]} ; do
    if ( ${list[$index]} ) ; then
        pipupdate $index
    fi
done


# if no pip updated
if ( ! $( \
    $mode_pip_sys20 || $mode_pip_sys21 || $mode_pip_sys22 || $mode_pip_sys23 || $mode_pip_sys24 || $mode_pip_sys25 || $mode_pip_sys26 || $mode_pip_sys27 || \
    $mode_pip_sys30 || $mode_pip_sys31 || $mode_pip_sys32 || $mode_pip_sys33 || $mode_pip_sys34 || $mode_pip_sys35 || $mode_pip_sys36 || $mode_pip_sys37 || \
    $mode_pip_brew2 || $mode_pip_brew3 || $mode_pip_pypy2 || $mode_pip_pypy3 || $updated \
    ) ) ; then
    $logprefix printf "update: ${green}pip${reset}: no ${bold}packages${reset} updated in Python\n\n" | $logsuffix
fi


# aftermath works
aftermath=`python -c "import os; print(os.path.join(os.path.dirname(os.path.abspath('$0')), 'aftermath.sh'))"`
bash $aftermath "$logfile" "$tmpfile"


# remove /tmp/log/update.log
rm -f "$tmpfile"


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1
