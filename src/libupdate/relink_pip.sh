#!/bin/bash


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1


################################################################################
# Relink Python executives.
################################################################################


# relink brewed pythons
brew link python@2 --force --overwrite
brew link python --overwrite
brew link pypy --overwrite
brew link pypy3 --overwrite


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1
