#!/usr/bin/env osascript

-- script based on https://github.com/theseal/ssh-askpass

on run argv
    set args to argv as text
    if args starts with "--help" or args starts with "-h" then
        return "macdaily-askpass [-p PASS] [prompt]"
    else if args starts with "--password" or args starts with "-p" then
        return text item 2 of argv
    end if
    display dialog args with icon caution default button "OK" default answer "" with hidden answer
    return result's text returned
end run
