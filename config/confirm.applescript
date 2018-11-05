#!/usr/bin/env osascript

on run argv
    set args to argv as text
    if args starts with "--help" or args starts with "-h" then
        return "macdaily-confirm [-h|--help] [prompt]"
    end if
    display dialog args with icon note default button "Cancel"
    return result's button returned
end run
