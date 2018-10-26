# -*- coding: utf-8 -*-

import abc
import collections
import datetime
import glob
import json
import os
import re
import shlex
import shutil
import signal
import sys

from macdaily.daily_utility import (blush, bold, Command, flash, make_mode,
                                    purple, red, reset, under)

try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess

__all__ = [
    'update_all', 'update_apm', 'update_mas', 'update_npm', 'update_gem',
    'update_pip', 'update_brew', 'update_cask', 'update_cleanup', 'update_system'
]

# root path
ROOT = os.path.dirname(os.path.abspath(__file__))

# brew renewed time
BREW_RENEW = None


class UpdateCommand(Command):
    @property
    def failed(self):
        return set(self._fail)

    def _run_proc(self):
        self._pkgs = list()
        self._fail = list()
        for path in self._exec:
            self._proc_logging(path)
            self._proc_update(path)

    def _proc_logging(self, path):
        if self._packages:
            self._check_pkgs(path)
        else:
            self._check_list(path)

    @abc.abstractmethod
    def _check_pkgs(self, path):
        self.__temp_pkgs = self._packages

    @abc.abstractmethod
    def _check_list(self, path):
        self.__temp_pkgs = set()

    @abc.abstractmethod
    def _proc_update(self, path):
        pass


class PipUpdate(UpdateCommand):
    @property
    def mode(self):
        return 'pip'

    def _pkg_args(self, args):
        super()._pkg_args(args)

        def match(version):
            return re.fullmatch(r'\d(\.\d)?', version)

        temp_ver = list()
        args_ver = getattr(args, 'version', list())
        for item in args_ver:
            temp_ver.extend(filter(match, item.split(',')))
        self._version = set(temp_ver)

    def _parse_args(self, namespace):
        self._brew = namespace.pop('brew', False)
        self._cpython = namespace.pop('cpython', False)
        self._pre = namespace.pop('pre', False)
        self._pypy = namespace.pop('pypy', False)
        self._quiet = namespace.pop('quiet', False)
        self._show_log = namespace.pop('show_log', False)
        self._system = namespace.pop('system', False)
        self._verbose = namespace.pop('verbose', False)
        self._yes = namespace.pop('yes', False)

        self._logging_opts = namespace.pop('logging', str()).split()
        self._update_opts = namespace.pop('update', str()).split()

    def _loc_exec(self):
        EXEC_PATH = dict(
            source=dict(
                brew=collections.defaultdict(list),
                system=collections.defaultdict(list),
            ),
            version=collections.defaultdict(list),
            combination={
                (True, True): collections.defaultdict(list),
                (True, False): collections.defaultdict(list),
                (False, True): collections.defaultdict(list),
                (False, False): collections.defaultdict(list),
            },
            implementation=dict(
                cpython=collections.defaultdict(list),
                pypy=collections.defaultdict(list),
            ),
        )

        def _sort_glob(path, *, flag):
            implementation = 'cpython' if flag else 'pypy'
            glob_path = glob.glob(path)
            if not glob_path:
                return
            glob_path.sort()
            path = glob_path[-1]

            try:
                ver_proc = subprocess.check_output(
                    [path, '--version'], stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError:
                return
            if re.match(rb"^Python \d\.\d", ver_proc, flags=(re.I | re.M)) is None:
                return
            ver_text = ver_proc.decode().split()[1]

            def _append_path(exec_path):
                exec_path[ver_text[:3]].append(path)
                exec_path[ver_text[0]].append(path)
                exec_path['main'].append(path)

            _append_path(EXEC_PATH['implementation'][implementation])
            _append_path(EXEC_PATH['combination'][(True, flag)])
            _append_path(EXEC_PATH['source']['brew'])
            _append_path(EXEC_PATH['version'])

        _sort_glob('/usr/local/Cellar/pypy/*/bin/pypy', flag=False)
        _sort_glob('/usr/local/Cellar/pypy3/*/bin/pypy3', flag=False)
        _sort_glob('/usr/local/Cellar/python@2/*/bin/python2.?', flag=True)
        _sort_glob('/usr/local/Cellar/python/*/bin/python3.?', flag=True)

        def _append_path(exec_path):
            exec_path[version[0]].append(path)
            exec_path[version].append(path)
            exec_path['main'].append(path)

        for path in glob.glob('/Library/Frameworks/Python.framework/Versions/?.?/bin/python?.?'):
            version = path[-3:]
            _append_path(EXEC_PATH['combination'][(False, True)])
            _append_path(EXEC_PATH['implementation']['cpython'])
            _append_path(EXEC_PATH['source']['system'])
            _append_path(EXEC_PATH['version'])

        def _extend_version(exec_path):
            if self._version:
                for version in self._version:
                    temp_exec.extend(exec_path[version])
            else:
                temp_exec.extend(exec_path['main'])

        temp_exec = list()
        if not any([self._brew, self._cpython, self._pypy, self._system]):
            _extend_version(EXEC_PATH['version'])
        elif (any([self._brew, self._system]) and not any([self._cpython, self._pypy])):
            if self._brew:
                _extend_version(EXEC_PATH['source']['brew'])
            if self._system:
                _extend_version(EXEC_PATH['source']['system'])
        elif (any([self._cpython, self._pypy]) and not any([self._brew, self._system])):
            if self._cpython:
                _extend_version(EXEC_PATH['implementation']['cpython'])
            if self._pypy:
                _extend_version(EXEC_PATH['implementation']['pypy'])
        else:
            if self._brew and self._cpython:
                _extend_version(EXEC_PATH['combination'][(True, True)])
            if self._brew and self._pypy:
                _extend_version(EXEC_PATH['combination'][(True, False)])
            if self._system and self._cpython:
                _extend_version(EXEC_PATH['combination'][(False, True)])
            if self._system and self._pypy:
                _extend_version(EXEC_PATH['combination'][(False, False)])
        self._exec = set(temp_exec)

        import pprint
        pprint.pprint(self._exec)

    def _check_pkgs(self, path):
        temp_pkgs = list()
        for package in self._packages:
            try:
                subprocess.check_call(
                    [path, 'show', package], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except subprocess.CalledProcessError:
                continue
            temp_pkgs.append(package)
        self.__temp_pkgs = set(package)

    def _check_list(self, path):
        args = [path, '-m', 'pip', 'list', '--format=freeze', '--outdated']
        if self._pre:
            args.append('--pre')
        args.extend(self._logging_opts)

        try:
            proc = subprocess.check_output(args, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            self.__temp_pkgs = set()
        else:
            self.__temp_pkgs = set(
                map(lambda pkg: pkg.split('==')[0], proc.decode().split()))

    def _proc_update(self, path):
        args = ['sudo', '--set-home', path,
                '-m', 'pip', 'install', '--upgrade']
        if self._pre:
            args.append('--pre')
        if self._quiet:
            args.append('--quiet')
        if self._verbose:
            args.append('--verbose')
        args.extend(self._update_opts)

        for package in self.__temp_pkgs:
            args.append(package)
            try:
                subprocess.check_call(args)
            except subprocess.CalledProcessError:
                self._fail.append(package)
            else:
                self._pkgs.append(package)
        del self.__temp_pkgs


def _merge_packages(args):
    packages = list()
    if 'package' in args and args.package:
        for pkg in map(lambda s: re.split(r'\W*,\W*', s), args.package):
            if 'all' in pkg:
                setattr(args, 'all', True)
                packages = {'all'}
                break
            packages.extend(pkg)
    elif 'all' in args.mode or args.all:
        packages = {'all'}
    return set(packages)


def update_all(args, file, temp, disk, password, bash_timeout, sudo_timeout):
    glb = globals()
    log = collections.defaultdict(set)
    for mode in {'apm', 'gem', 'mas', 'npm', 'pip', 'brew', 'cask', 'system'}:
        glb[mode] = False
        if not getattr(args, f'no_{mode}'):
            glb[mode] = True
            log[mode] = eval(f'update_{mode}')(args, file=file, temp=temp, disk=disk, retset=True,
                                               password=password, bash_timeout=bash_timeout, sudo_timeout=sudo_timeout)

    if not args.no_cleanup:
        update_cleanup(args, file=file, temp=temp, disk=disk, retset=True,
                       gem=gem, npm=npm, pip=pip, brew=brew, cask=cask,  # pylint: disable=E0602
                       password=password, bash_timeout=bash_timeout, sudo_timeout=sudo_timeout)
    return log


def update_apm(args, file, temp, disk, password, bash_timeout, sudo_timeout, retset=False):
    if shutil.which('apm') is None:
        print(f'update: {blush}{flash}apm{reset}: command not found\n'
              f'update: {red}apm{reset}: you may download Atom from {purple}{under}https://atom.io{reset}\n',
              file=sys.stderr)
        return set() if retset else dict(apm=set())

    logname = shlex.quote(file)
    tmpname = shlex.quote(temp)
    quiet = str(args.quiet).lower()
    verbose = str(args.verbose).lower()
    yes = str(args.yes).lower()
    packages = _merge_packages(args)

    make_mode(args, file, 'Atom')
    if 'all' in packages or args.all:
        logging = subprocess.run(['bash', os.path.join(ROOT, 'logging_apm.sh'), logname, tmpname],
                                 stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=bash_timeout)
        log = set(re.sub(r'\^D\x08\x08', '', logging.stdout.decode().strip(), flags=re.IGNORECASE).split())
        outdated = 'true' if log and all(log) else 'false'
    else:
        log = packages
        outdated = 'true'

    subprocess.run(['bash', os.path.join(ROOT, 'update_apm.sh'),
                   logname, tmpname, quiet, verbose, outdated, yes] + list(log), timeout=bash_timeout)

    print()
    return log if retset else dict(apm=log)


def update_gem(args, file, temp, disk, password, bash_timeout, sudo_timeout, cleanup=True, retset=False):
    if shutil.which('gem') is None:
        print(f'update: {blush}{flash}gem{reset}: command not found\n'
              f'update: {red}gem{reset}: you may download Ruby from '
              f'{purple}{under}https://www.ruby-lang.org/{reset}\n', file=sys.stderr)
        return set() if retset else dict(gem=set())

    logname = shlex.quote(file)
    tmpname = shlex.quote(temp)
    quiet = str(args.quiet).lower()
    verbose = str(args.verbose).lower()
    yes = str(args.yes).lower()
    packages = _merge_packages(args)

    make_mode(args, file, 'Ruby')
    if 'all' in packages or args.all:
        logging = subprocess.run(['bash', os.path.join(ROOT, 'logging_gem.sh'), logname, tmpname],
                                 stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=bash_timeout)
        log = set(re.sub(r'\^D\x08\x08', '', logging.stdout.decode().strip(), flags=re.IGNORECASE).split())
        outdated = 'true' if log and all(log) else 'false'
    else:
        log = packages
        outdated = 'true'

    subprocess.run(['bash', os.path.join(ROOT, 'update_gem.sh'), password, sudo_timeout,
                   logname, tmpname, quiet, verbose, yes, outdated] + list(log), timeout=bash_timeout)

    print()
    if not (retset or args.no_cleanup):
        update_cleanup(args, file=file, temp=temp, disk=disk, gem=True,
                       password=password, bash_timeout=bash_timeout, sudo_timeout=sudo_timeout)
    return log if retset else dict(gem=log)


def update_mas(args, file, temp, disk, password, bash_timeout, sudo_timeout, retset=False):
    if shutil.which('mas') is None:
        print(f'update: {blush}{flash}mas{reset}: command not found\n'
              f'update: {red}cask{reset}: you may download MAS through following command -- '
              f'`{bold}brew install mas{reset}`\n', file=sys.stderr)
        return set() if retset else dict(mas=set())

    logname = shlex.quote(file)
    tmpname = shlex.quote(temp)
    quiet = str(args.quiet).lower()
    verbose = str(args.verbose).lower()
    packages = _merge_packages(args)

    make_mode(args, file, 'Mac App Store')
    logging = subprocess.run(['bash', os.path.join(ROOT, 'logging_mas.sh'), logname, tmpname],
                             stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=bash_timeout)
    if 'all' in packages or args.all:
        log = set(re.split(r'[\r\n]', re.sub(r'\^D\x08\x08', '', logging.stdout.decode().strip(), flags=re.IGNORECASE)))
        outdated = 'true' if log and all(log) else 'false'
    else:
        log = packages
        outdated = 'true'

    subprocess.run(['bash', os.path.join(ROOT, 'update_mas.sh'), password, sudo_timeout,
                   logname, tmpname, quiet, verbose, outdated] + list(packages), timeout=bash_timeout)

    print()
    return log if retset else dict(mas=log)


def update_npm(args, file, temp, disk, password, bash_timeout, sudo_timeout, cleanup=True, retset=False):
    if shutil.which('npm') is None:
        print(f'update: {blush}{flash}npm{reset}: command not found\n'
              f'update: {red}npm{reset}: you may download Node.js from '
              f'{purple}{under}https://nodejs.org/{reset}\n', file=sys.stderr)
        return set() if retset else dict(npm=set())

    logname = shlex.quote(file)
    tmpname = shlex.quote(temp)
    quiet = str(args.quiet).lower()
    verbose = str(args.verbose).lower()
    packages = _merge_packages(args)

    make_mode(args, file, 'Node.js')
    if 'all' in packages or args.all:
        allflag = 'true'
        logging = subprocess.run(['bash', os.path.join(ROOT, 'logging_npm.sh'), logname, tmpname],
                                 stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=bash_timeout)
        stdout = logging.stdout.decode().strip()
        start = stdout.find('{')
        end = stdout.rfind('}')
        if start == -1 or end == -1:
            stdict = dict()
        else:
            stdict = json.loads(re.sub(r'\^D\x08\x08', '', stdout[start:end+1], flags=re.I))
        log = set(stdict.keys())
        pkg = {f'{name}@{value["wanted"]}' for name, value in stdict.items()}
        outdated = 'true' if log and all(log) else 'false'
    else:
        allflag = 'false'
        log = pkg = packages
        outdated = 'true'

    subprocess.run(['bash', os.path.join(ROOT, 'update_npm.sh'), password, sudo_timeout,
                   logname, tmpname, allflag, quiet, verbose, outdated] + list(pkg), timeout=bash_timeout)

    print()
    if not retset and not args.no_cleanup:
        update_cleanup(args, file=file, temp=temp, disk=disk, npm=True,
                       password=password, bash_timeout=bash_timeout, sudo_timeout=sudo_timeout)
    return log if retset else dict(npm=log)


def update_pip(args, file, temp, disk, password, bash_timeout, sudo_timeout, cleanup=True, retset=False):
    logname = shlex.quote(file)
    tmpname = shlex.quote(temp)
    quiet = str(args.quiet).lower()
    verbose = str(args.verbose).lower()
    yes = str(args.yes).lower()
    pre = str(args.pre).lower()
    packages = _merge_packages(args)

    make_mode(args, file, 'Python')
    flag = not ('pip' in args.mode and any((args.version, args.system, args.brew, args.cpython, args.pypy)))
    if flag and packages:
        system, brew, cpython, pypy, version = 'true', 'true', 'true', 'true', '1'
    else:
        system, brew, cpython, pypy, version = \
            str(args.system).lower(), str(args.brew).lower(), \
            str(args.cpython).lower(), str(args.pypy).lower(), str(args.version)

    logging = subprocess.run(['bash', os.path.join(ROOT, 'logging_pip.sh'), logname, tmpname,
                              system, brew, cpython, pypy, version, pre] + list(packages),
                             stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=bash_timeout)
    log = set(re.sub(r'\^D\x08\x08', '', logging.stdout.decode().strip(), flags=re.IGNORECASE).split())
    if 'macdaily' in log:
        os.kill(os.getpid(), signal.SIGUSR1)

    subprocess.run(['bash', os.path.join(ROOT, 'update_pip.sh'), password, sudo_timeout,
                    logname, tmpname, system, brew, cpython, pypy, version,
                    yes, quiet, verbose, pre] + list(packages), timeout=bash_timeout)
    subprocess.run(['bash', os.path.join(ROOT, 'relink_pip.sh')],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=bash_timeout)

    print()
    if not retset and not args.no_cleanup:
        update_cleanup(args, file=file, temp=temp, disk=disk, pip=True,
                       password=password, bash_timeout=bash_timeout, sudo_timeout=sudo_timeout)
    return log if retset else dict(pip=log)


def update_brew(args, file, temp, disk, password, bash_timeout, sudo_timeout, cleanup=True, retset=False):
    if shutil.which('brew') is None:
        print(f'update: {blush}{flash}brew{reset}: command not found\n'
              f'update: {red}brew{reset}: you may find Homebrew on {purple}{under}https://brew.sh{reset}, '
              f'or install Homebrew through following command -- `{bold}/usr/bin/ruby -e '
              f'"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"{reset}`\n',
              file=sys.stderr)
        return set() if retset else dict(brew=set())

    logname = shlex.quote(file)
    tmpname = shlex.quote(temp)
    quiet = str(args.quiet).lower()
    verbose = str(args.verbose).lower()
    force = str(args.force).lower()
    merge = str(args.merge).lower()
    packages = _merge_packages(args)

    make_mode(args, file, 'Homebrew')
    global BREW_RENEW
    if BREW_RENEW is None or (datetime.datetime.now() - BREW_RENEW).total_seconds() > 300:
        subprocess.run(['bash', os.path.join(ROOT, 'renew_brew.sh'), logname, tmpname,
                        quiet, verbose, force, merge], timeout=bash_timeout)
        BREW_RENEW = datetime.datetime.now()

    if 'all' in packages or args.all:
        logging = subprocess.run(['bash', os.path.join(ROOT, 'logging_brew.sh'), logname, tmpname],
                                 stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=bash_timeout)
        log = set(re.sub(r'\^D\x08\x08', '', logging.stdout.decode().strip(), flags=re.IGNORECASE).split())
        outdated = 'true' if log and all(log) else 'false'
    else:
        log = packages
        outdated = 'true'

    subprocess.run(['bash', os.path.join(ROOT, 'update_brew.sh'), password, sudo_timeout,
                   logname, tmpname, quiet, verbose, outdated] + list(log), timeout=bash_timeout)

    print()
    if not retset and not args.no_cleanup:
        update_cleanup(args, file=file, temp=temp, disk=disk, brew=True,
                       password=password, bash_timeout=bash_timeout, sudo_timeout=sudo_timeout)
    return log if retset else dict(brew=log)


def update_cask(args, file, temp, disk, password, bash_timeout, sudo_timeout, cleanup=True, retset=False):
    try:
        subprocess.check_call(['brew', 'command', 'cask'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print(f'update: {blush}{flash}cask{reset}: command not found\n'
              f'update: {red}cask{reset}: you may find Caskroom on '
              f'{purple}{under}https://caskroom.github.io{reset}, '
              f'or install Caskroom through following command -- '
              f'`{bold}brew tap homebrew/cask{reset}`\n', file=sys.stderr)
        return set() if retset else dict(cask=set())

    logname = shlex.quote(file)
    tmpname = shlex.quote(temp)
    quiet = str(args.quiet).lower()
    verbose = str(args.verbose).lower()
    force = str(args.force).lower()
    merge = str(args.merge).lower()
    greedy = str(args.greedy).lower()
    packages = _merge_packages(args)

    make_mode(args, file, 'Caskroom')
    global BREW_RENEW
    if BREW_RENEW is None or (datetime.datetime.now() - BREW_RENEW).total_seconds() > 300:
        subprocess.run(['bash', os.path.join(ROOT, 'renew_brew.sh'), logname, tmpname,
                        quiet, verbose, force, merge], timeout=bash_timeout)
        BREW_RENEW = datetime.datetime.now()

    if 'all' in packages or args.all:
        logging = subprocess.run(['bash', os.path.join(ROOT, 'logging_cask.sh'), logname, tmpname, greedy, force],
                                 stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=bash_timeout)
        log = set(re.sub(r'\^D\x08\x08', '', logging.stdout.decode().strip(), flags=re.IGNORECASE).split())
        outdated = 'true' if log and all(log) else 'false'
    else:
        log = packages
        outdated = 'true'

    subprocess.run(['bash', os.path.join(ROOT, 'update_cask.sh'), password, sudo_timeout,
                   logname, tmpname, quiet, verbose, force, greedy, outdated] + list(log), timeout=bash_timeout)

    print()
    if not retset and not args.no_cleanup:
        update_cleanup(args, file=file, temp=temp, disk=disk, cask=True,
                       password=password, bash_timeout=bash_timeout, sudo_timeout=sudo_timeout)
    return log if retset else dict(cask=log)


def update_system(args, file, temp, disk, password, bash_timeout, sudo_timeout, retset=False):
    if shutil.which('softwareupdate') is None:
        print(f'update: {blush}{flash}system{reset}: command not found\n'
              f"update: {red}system{reset}: you may add `softwareupdate' to $PATH through the following command -- "
              f"`{bold}echo export PATH='/usr/sbin:$PATH' >> ~/.bash_profile{reset}'\n", file=sys.stderr)
        return set() if retset else dict(system=set())

    logname = shlex.quote(file)
    tmpname = shlex.quote(temp)
    quiet = str(args.quiet).lower()
    verbose = str(args.verbose).lower()
    restart = str(args.restart).lower()
    packages = _merge_packages(args)

    make_mode(args, file, 'System')
    logging = subprocess.run(['bash', os.path.join(ROOT, 'logging_system.sh'), logname, tmpname],
                             stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=bash_timeout)
    if 'all' in packages or args.all:
        log = set(re.split(r'[\n\r]', re.sub(r'\^D\x08\x08', '', logging.stdout.decode().strip(), flags=re.IGNORECASE)))
        outdated = 'true' if log and all(log) else 'false'
    else:
        log = packages
        outdated = 'true'

    subprocess.run(['bash', os.path.join(ROOT, 'update_system.sh'), password, sudo_timeout,
                   logname, tmpname, quiet, verbose, restart, outdated] + list(packages), timeout=bash_timeout)

    print()
    return log if retset else dict(system=log)


def update_cleanup(args, file, temp, disk, password, bash_timeout, sudo_timeout,
                   gem=False, npm=False, pip=False, brew=False, cask=False, retset=False):
    logname = shlex.quote(file)
    tmpname = shlex.quote(temp)
    dskname = shlex.quote(disk)

    gem = str(args.gem if 'cleanup' in args.mode else gem).lower()
    npm = str(args.npm if 'cleanup' in args.mode else npm).lower()
    pip = str(args.pip if 'cleanup' in args.mode else pip).lower()
    brew = str(args.brew if 'cleanup' in args.mode else brew).lower()
    cask = str(args.cask if 'cleanup' in args.mode else cask).lower()
    quiet = str(args.quiet).lower()

    make_mode(args, file, 'Cleanup', flag=any((gem, npm, pip, brew, cask)))
    subprocess.run(['bash', os.path.join(ROOT, 'cleanup.sh'), password, sudo_timeout,
                   logname, tmpname, dskname, gem, npm, pip, brew, cask, quiet], timeout=bash_timeout)

    print()
    return set() if retset else dict(cleanup=set())
