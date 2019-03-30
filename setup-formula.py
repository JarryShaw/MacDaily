# -*- coding: utf-8 -*-

import distutils.util  # pylint: disable=no-name-in-module,import-error
import hashlib
import os
import re
import subprocess
import sys
import tempfile

import bs4
import requests

with open(os.path.join(os.path.dirname(__file__), 'macdaily/util/const/macro.py')) as file:
    for line in file:
        match = re.match(r"VERSION = '(.*)'", line)
        if match is None:
            continue
        VERSION = match.groups()[0]
        break
# print(VERSION)

url = f'https://pypi.org/project/macdaily/{VERSION}/#files'
page = requests.get(url)
soup = bs4.BeautifulSoup(page.text, 'html5lib')
table = soup.find_all('table', class_='table--downloads')[0]

for line in filter(lambda item: isinstance(item, bs4.element.Tag), table.tbody):
    item = line.find_all('td')[0]
    link = item.a.get('href') or ''
    # print(link)
    if link.endswith('.tar.gz'):
        MACDAILY_URL = link
        MACDAILY_SHA = hashlib.sha256(requests.get(MACDAILY_URL).content).hexdigest()
        break
# print(MACDAILY_URL)
# print(MACDAILY_SHA)

with tempfile.TemporaryDirectory() as tempdir:
    platform = distutils.util.get_platform().replace('-', '_').replace('.', '_')  # pylint: disable=no-member
    python_version = '%s%s' % sys.version_info[:2]
    implementation = sys.implementation.name[:2]
    subprocess.check_call([sys.executable, '-m', 'pip', 'download', 'macdaily',
                           f"--platform={platform}",
                           f"--python-version={python_version}",
                           f'--implementation={implementation}',
                           f'--dest={tempdir}',
                           '--no-deps'], stdout=subprocess.DEVNULL)
    archive = f'{tempdir}/macdaily-{VERSION}-{implementation}{python_version}-none-{platform}.whl'
    with open(archive, 'rb') as file:
        content = file.read()
    DEVEL_SUFFIX = hashlib.sha256(content).hexdigest()[:6]

DEVEL_URL = f'https://github.com/JarryShaw/MacDaily/archive/v{VERSION}.{DEVEL_SUFFIX}-devel.tar.gz'
DEVEL_SHA = hashlib.sha256(requests.get(DEVEL_URL).content).hexdigest()
# print(DEVEL_URL)
# print(DEVEL_SHA)

CONFIGUPDATER = subprocess.check_output(['poet', 'configupdater']).decode().strip()
DICTDUMPER = subprocess.check_output(['poet', 'dictdumper']).decode().strip()
PSUTIL = subprocess.check_output(['poet', 'psutil']).decode().strip()
PTYNG = subprocess.check_output(['poet', 'ptyng']).decode().strip()
PATHLIB2 = subprocess.check_output(['poet', 'pathlib2']).decode().strip()
SUBPROCESS32 = subprocess.check_output(['poet', 'subprocess32']).decode().strip()
TBTRIM = subprocess.check_output(['poet', 'tbtrim']).decode().strip()
# print(CONFIGUPDATER)
# print(DICTDUMPER)
# print(PSUTIL)
# print(PTYNG)
# print(PATHLIB2)
# print(SUBPROCESS32)
# print(TBTRIM)

match = re.match(r'([0-9.]+)\.post([0-9])', VERSION)
if match is None:
    MACDAILY = (f'url "{MACDAILY_URL}"\n'
                f'  sha256 "{MACDAILY_SHA}"')
    DEVEL = (f'url "{DEVEL_URL}"\n'
             f'    version "{VERSION}.{DEVEL_SUFFIX}"\n'
             f'    sha256 "{DEVEL_SHA}"')
else:
    version, revision = match.groups()
    MACDAILY = (f'url "{MACDAILY_URL}"\n'
                f'  version "{version}"\n'
                f'  sha256 "{MACDAILY_SHA}"\n'
                f'  revision {revision}')
    DEVEL = (f'url "{DEVEL_URL}"\n'
             f'    version "{version}_{revision}.{DEVEL_SUFFIX}"\n'
             f'    sha256 "{DEVEL_SHA}"')

FORMULA = f'''\
class Macdaily < Formula
  include Language::Python::Virtualenv

  desc "macOS Automated Package Manager"
  homepage "https://github.com/JarryShaw/MacDaily#macdaily"
  {MACDAILY}

  head "https://github.com/JarryShaw/MacDaily.git", :branch => "master"

  devel do
    {DEVEL}
  end

  option "without-config", "Build without config modification support"
  option "without-tree", "Build without tree format support"
  option "without-ptyng", "Build without alternative PTY support"

  depends_on "python"
  depends_on "expect" => :recommended
  depends_on "cowsay" => :optional
  depends_on "fortune" => :optional
  depends_on "lolcat" => :optional

  {CONFIGUPDATER}

  {DICTDUMPER}

  {PSUTIL}

  {PTYNG}

  {PATHLIB2}

  {SUBPROCESS32}

  {TBTRIM}

  def install
    venv = virtualenv_create(libexec, "python3")
    venv.pip_install resource("tbtrim")

    if build.with?("config")
      venv.pip_install resource("configupdater")
    end

    if build.with?("tree")
      venv.pip_install resource("dictdumper")
    end

    if build.with?("ptyng")
      venv.pip_install resource("ptyng")

      exitcode = `#{{libexec}}/"bin/python" -c "print(__import__('os').system('ps axo pid=,stat= > /dev/null 2>&1'))"`
      if exitcode !~ /0/
        venv.pip_install resource("psutil")
      end
    end

    version = Language::Python.major_minor_version "python3"
    if version =~ /3.4/
      %w[pathlib2 six subprocess32].each do |r|
        venv.pip_install resource(r)
      end
    end
    venv.pip_install_and_link buildpath

    comp_path = Pathname.new(buildpath/"macdaily/comp/macdaily.bash-completion")
    comp_base = File.dirname comp_path
    bash_comp = File.join(comp_base, "macdaily")

    cp comp_path, bash_comp
    bash_completion.install bash_comp

    man_path = Pathname.glob(libexec/"lib/python#{{version}}/site-packages/macdaily/man/*.1")
    dir_name = File.dirname man_path[0]
    dest = File.join(dir_name, "temp.1")

    man_path.each do |f|
      cp f, dest
      man1.install f
      mv dest, f
    end
  end

  def post_install
    # set environment variables
    ENV["NULL_PASSWORD"] = "true"
    ENV["MACDAILY_LOGDIR"] = "/tmp"
    ENV["MACDAILY_NO_CONFIG"] = "true"

    # relaunch askpass & confirm utilities
    system bin/"macdaily", "launch", "askpass", "confirm"
  end

  def caveats
    text = <<~EOS
      MacDaily has been installed as
        #{{HOMEBREW_PREFIX}}/bin/macdaily

      Alias executables `md-update`, `md-uninstall`, etc. equal to
      `macdaily update`, `macdaily uninstall`, etc., respectively,
      have been also installed into #{{HOMEBREW_PREFIX}}/bin/

      Configuration file locates at ~/.dailyrc, please directly run
      `macdaily config --interactive` command to set up your runtime
      specifications.

      Due to restrictions of Homebrew, please manually run
      `macdaily launch daemons` command to relaunch your scheduled
      tasks of MacDaily.

      For more information, check out `macdaily help` command. Online
      documentations available at GitHub repository.

      See: https://github.com/JarryShaw/MacDaily#generals
    EOS
    text
  end

  test do
    system bin/"macdaily", "--help"
  end
end
'''

with open(os.path.join(os.path.dirname(__file__), 'Tap/Formula/macdaily.rb'), 'w') as file:
    file.write(FORMULA)
