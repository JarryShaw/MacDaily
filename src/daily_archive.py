# -*- coding: utf-8 -*-

import datetime
import sys

from macdaily.daily_config import parse
from macdaily.daily_utility import archive, green, red, reset, storage, under, make_path, beholder


def archive_(config, logdate, today):
    filelist = list()
    for mode in {'update', 'uninstall', 'reinstall', 'postinstall', 'dependency',
                 'logging/apm', 'logging/gem', 'logging/pip', 'logging/npm', 'logging/brew',
                 'logging/cask', 'logging/dotapp', 'logging/macapp', 'logging/appstore'}:
        _, logpath, arcpath, tarpath = make_path(config, mode, logdate)
        filelist.extend(archive(config, logpath, arcpath, tarpath, logdate, today, mvflag=False))
    filelist.extend(storage(config, logdate, today))

    if filelist:
        files = '{}, {}'.format(reset, under).join(filelist)
        print('macdaily: {}archive{}: archived following old logs: {}{}{}'.format(green, reset, under, files, reset))
    else:
        print('macdaily: {}archive{}: no ancient logs archived'.format(red, reset))


@beholder
def main():
    config = parse()
    today = datetime.datetime.today()
    logdate = datetime.date.strftime(today, r'%y%m%d')
    archive_(config, logdate, today)


if __name__ == '__main__':
    sys.tracebacklimit = 0
    sys.exit(main())
