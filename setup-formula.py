# -*- coding: utf-8 -*-

import hashlib
import os
import re
import subprocess

import bs4
import requests

with open(os.path.join(os.path.dirname(__file__), 'macdaily/util/const.py')) as file:
    for line in file:
        match = re.match(r"__version__ = '(.*)'", line)
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

DEVEL_URL = f'https://codeload.github.com/JarryShaw/MacDaily/tar.gz/v{VERSION}.devel'
DEVEL_SHA = hashlib.sha256(requests.get(DEVEL_URL).content).hexdigest()
# print(DEVEL_URL)
# print(DEVEL_SHA)

CONFIGUPDATER = subprocess.check_output(['poet', 'configupdater']).decode().strip()
DICTDUMPER = subprocess.check_output(['poet', 'dictdumper']).decode().strip()
PSUTIL = subprocess.check_output(['poet', 'psutil']).decode().strip()
PTYNG = subprocess.check_output(['poet', 'ptyng']).decode().strip()
PATHLIB2 = subprocess.check_output(['poet', 'pathlib2']).decode().strip()
SUBPROCESS32 = subprocess.check_output(['poet', 'subprocess32']).decode().strip()
# print(CONFIGUPDATER)
# print(DICTDUMPER)
# print(PSUTIL)
# print(PTYNG)
# print(PATHLIB2)
# print(SUBPROCESS32)

FORMULA = f'''\
class Macdaily < Formula
  include Language::Python::Virtualenv

  version "{VERSION}"
  desc "macOS Automated Package Manager"
  homepage "https://github.com/JarryShaw/MacDaily#macdaily"
  url "{MACDAILY_URL}"
  sha256 "{MACDAILY_SHA}"
  head "https://github.com/JarryShaw/MacDaily.git", :branch => "master"

  bottle :unneeded

  # bottle do
  #   cellar :any_skip_relocation
  #   sha256 "" => :mojave
  #   sha256 "" => :high_sierra
  #   sha256 "" => :sierra
  # end

  devel do
    url "{DEVEL_URL}"
    sha256 "{DEVEL_SHA}"
  end

  depends_on "python"
  depends_on "expect" => :recommended
  depends_on "jarryshaw/tap/askpass" => :optional
  depends_on "jarryshaw/tap/confirm" => :optional
  depends_on "theseal/ssh-askpass/ssh-askpass" => :optional

  option "without-config", "build without config modification support"
  option "without-tree", "build without tree format support"
  option "without-ptyng", "build without alternative PTY support"

  {CONFIGUPDATER}

  {DICTDUMPER}

  {PTYNG}

  {PSUTIL}

  {PATHLIB2}

  {SUBPROCESS32}

  def install
    # virtualenv_install_with_resources
    venv = virtualenv_create(libexec, "python3")
    if build.with?("config")
      venv.pip_install resource("configupdater")
    end

    if build.with?("tree")
      venv.pip_install resource("dictdumper")
    end

    if build.with?("ptyng")
      venv.pip_install resource("ptyng")

      exitcode = `#{{libexec}}/"bin/python" -c "print(__import__('os').system('ps axo pid=,stat= > /dev/null 2>&1'))"`
      if !( exitcode =~ /0/ )
        venv.pip_install resource("psutil")
      end
    end

    version = `#{{libexec}}/"bin/python" -c "print('%s.%s' % __import__('sys').version_info[:2])"`
    if ( version =~ /3.4/ )
      %w[pathlib2 six subprocess32].each do |r|
        venv.pip_install resource(r)
      end
    end
    venv.pip_install_and_link buildpath

    man_path = Pathname.glob(libexec/"lib/python?.?/site-packages/macdaily/man/*.1")
    dir_name = File.dirname man_path[0]
    dest = File.join(dir_name, "temp.1")

    man_path.each do |f|
      FileUtils.cp f, dest
      man1.install f
      FileUtils.mv dest, f
    end
  end

  # def post_install
  #   text = <<~EOS
  #     To run postinstall process, please directly call
  #       `macdaily launch askpass confirm`
  #   EOS
  #   puts text
  # end

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

      For more information, check out `macdaily help` command. Online
      documentations available at GitHub repository.

      To run postinstall process, please directly call
        `macdaily launch askpass confirm`

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
