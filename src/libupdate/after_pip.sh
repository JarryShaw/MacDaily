#!/bin/bash


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1


################################################################################
# Aftermath.
################################################################################


# relink brewed pythons
brew unlink python@2 > /dev/null 2>&1
brew unlink python > /dev/null 2>&1
brew unlink pypy > /dev/null 2>&1
brew unlink pypy3 > /dev/null 2>&1
brew link python@2 --force --overwrite > /dev/null 2>&1
brew link python --force --overwrite > /dev/null 2>&1
brew link pypy --force --overwrite > /dev/null 2>&1
brew link pypy3 --force --overwrite > /dev/null 2>&1


# clear potential terminal buffer
sript -q /dev/null tput clear > /dev/null 2>&1
