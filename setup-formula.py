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

DEVEL_URL = f'https://codeload.github.com/JarryShaw/MacDaily/tar.gz/v{VERSION}'
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
  head "https://github.com/JarryShaw/MacDaily.git", :branch => "release"

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
  depends_on "theseal/ssh-askpass/ssh-askpass" => :optional

  {CONFIGUPDATER}

  {DICTDUMPER}

  {PTYNG}

  {PSUTIL}

  {PATHLIB2}

  {SUBPROCESS32}

  def install
    virtualenv_install_with_resources
    man_path = Pathname.glob(libexec/"lib/python?.?/site-packages/macdaily/man/*.1")
    man_path.each do |f|
      man1.install f
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

with open(os.path.join(os.path.dirname(__file__), 'Formula/macdaily.rb'), 'w') as file:
    file.write(FORMULA)
