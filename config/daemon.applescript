#!/usr/bin/env osascript

-- show notification
display notification "Running scheduled {mode} scripts..." with title "MacDaily"

-- run script
do shell script "{sys.executable} -m macdaily {mode} {argv}"
