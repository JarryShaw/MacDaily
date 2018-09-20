# -*- coding: utf-8 -*-


import datetime
import sys

from macdaily.daily_config import parse
from macdaily.daily_utility import *


# terminal display
reset  = '\033[0m'      # reset
under  = '\033[4m'      # underline
red    = '\033[91m'     # bright red foreground
green  = '\033[92m'     # bright green foreground


def archive_(config, *, logdate, today):
    filelist = list()
    for mode in {'update', 'uninstall', 'reinstall', 'postinstall', 'dependency',
                 'logging/apm', 'logging/gem', 'logging/pip', 'logging/npm',
                 'logging/brew', 'logging/cask', 'logging/dotapp', 'logging/macapp', 'logging/appstore'}:
        tmppath, logpath, arcpath, tarpath = make_path(config, mode=mode, logdate=logdate)
        filelist.extend(archive(config, logpath=logpath, arcpath=arcpath, tarpath=tarpath, logdate=logdate, today=today, mvflag=False))
    filelist.extend(storage(config, logdate=logdate, today=today))

    if filelist:
        files = '{}, {}'.format(reset, under).join(filelist)
        print('macdaily: {}archive{}: archived following old logs: {}{}{}'.format(green, reset, under, files, reset))
    else:
        print('macdaily: {}archive{}: no ancient logs archived'.format(red, reset))


@beholder
def main():
    config = parse()
    argv = sys.argv[1:]
    today = datetime.datetime.today()
    logdate = datetime.date.strftime(today, '%y%m%d')

    archive_(argv, config, logdate=logdate, today=today)


if __name__ == '__main__':
    sys.exit(main())
