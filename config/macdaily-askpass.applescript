#!/usr/bin/env osascript

-- script based on https://github.com/theseal/ssh-askpass

on run argv
    set args to argv as text
    display dialog args with icon caution default button "OK" default answer "" with hidden answer
    return result's text returned
end run
