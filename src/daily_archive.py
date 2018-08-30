# -*- coding: utf-8 -*-


from macdaily.daily_utility import *


# terminal display
reset  = '\033[0m'      # reset
under  = '\033[4m'      # underline
red    = '\033[91m'     # bright red foreground
green  = '\033[92m'     # bright green foreground


def main(config, *, logdate, today):
    filelist = list()
    for mode in {   'update', 'uninstall', 'reinstall', 'postinstall', 'dependency',
                    'logging/apm', 'logging/gem', 'logging/pip', 'logging/npm',
                    'logging/brew', 'logging/cask', 'logging/dotapp', 'logging/macapp', 'logging/appstore'  }:
        tmppath, logpath, arcpath, tarpath = make_path(config, mode=mode, logdate=logdate)
        filelist.extend(archive(config, logpath=logpath, arcpath=arcpath, tarpath=tarpath, logdate=logdate, today=today, mvflag=False))
    filelist.extend(storage(config, logdate=logdate, today=today))

    if filelist:
        files = f'{reset}, {under}'.join(filelist)
        print(f'macdaily: {green}archive{reset}: archived following old logs: {under}{files}{reset}')
    else:
        print(f'macdaily: {red}archive{reset}: no ancient logs archived')


if __name__ == '__main__':
    import datetime
    import sys

    from macdaily.daily_config import parse

    config = parse()
    argv = sys.argv[1:]
    today = datetime.datetime.today()
    logdate = datetime.date.strftime(today, '%y%m%d')
    sys.exit(main(argv, config, logdate=logdate, today=today))
