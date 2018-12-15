# -*- coding: utf-8 -*-

import datetime
import os
import pprint
import re
import sys

from macdaily.cli.config import get_config_parser, parse_args
from macdaily.cmd.config import make_config, parse_config
from macdaily.util.const import (__version__, bold, green, length, red, reset,
                                 yellow)
from macdaily.util.misc import beholder, print_term, record


@beholder
def config(argv=None):
    # parse args & set context redirection flags
    args = parse_args(argv)
    quiet = args.quiet
    verbose = (args.quiet or not args.verbose)

    # enter interactive setup process
    if args.interactive:
        # record program status
        text = f'{bold}{green}|🚨|{reset} {bold}Running MacDaily version {__version__}{reset}'
        print_term(text, os.devnull, redirect=quiet)
        record(os.devnull, args, datetime.datetime.today(), redirect=verbose)

        # make config
        make_config(quiet, verbose)
        text = (f'{bold}{green}|🍺|{reset} {bold}MacDaily successfully performed config process')
        print_term(text, os.devnull, redirect=quiet)
        return

    # parse config & change environ
    config = parse_config(quiet, verbose)
    os.environ['SUDO_ASKPASS'] = config['Miscellaneous']['askpass']
    os.environ['TIMEOUT'] = config['Miscellaneous']['retry']

    # list existing config
    if args.list:
        for key, value in config.items():
            for k, v, in value.items():
                print(f'{key}.{k}={v}')
        return

    # then key is mandatory
    if args.key is None:
        parser = get_config_parser()
        parser.error('the following arguments are required: key')

    # validate given key
    match = re.match(r'(\w+)\.(\w+)', args.key.strip())
    if match is None:
        parser = get_config_parser()
        parser.error(f"argument KEY: invalid value: {args.key!r}")
    section, option = match.groups()

    # fetch value of a given key
    if args.get:
        return pprint.pprint(config[section].get(option), indent=2, width=length)

    try:
        import configupdater
    except ImportError:
        print_term(f'macdaily-config: {yellow}error{reset}: {bold}ConfigUpdater{reset} not installed, '
                   f"which is mandatory for modification of configuration",
                   os.devnull, redirect=verbose)
        print(f'macdaily-config: {red}error{reset}: broken dependency', file=sys.stderr)
        raise

    # make ConfigUpdater
    updater = configupdater.ConfigUpdater(allow_no_value=True,
                                          inline_comment_prefixes=';')
    with open(os.path.expanduser('~/.dailyrc')) as file:
        updater.read_file(file)

    # then value is also mandatory
    check_value = sum((args.true, args.false, (args.value is not None)))
    if check_value > 1:
        parser = get_config_parser()
        parser.error(f"conflicting option(s): '--true', '--false' and {args.value!r}")
    elif check_value == 0:
        parser = get_config_parser()
        parser.error("the following arguments are required: '--true', '--false', or value")
    elif args.false:
        value = 'false'
    elif args.true:
        value = 'true'
    else:
        value = args.value
    formatted_value = value.ljust(56 - len(option))

    # fetch comment
    origin = updater[section].get(option)
    if origin is None:
        comment = str()
    else:
        comment = ''.join(origin.value.split(maxsplit=1)[1:])

    # modify value for a given key
    if args.add and args.unset:
        parser = get_config_parser()
        parser.error("conflicting option(s): '--all' and '--unset'")
    elif args.unset:
        updater[section][option] = comment
    elif args.add:
        if origin is None:
            updater[section][option] = f'{formatted_value} {comment}'
        else:
            updater[section][option] = f'{origin}{os.linesep}    {value}'
    else:
        updater[section][option] = f'{formatted_value} {comment}'

    # update config file
    updater.update_file()


if __name__ == '__main__':
    sys.exit(config())
