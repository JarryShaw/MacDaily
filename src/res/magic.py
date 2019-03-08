# -*- coding: utf-8 -*-

import os
import random
import shutil

from macdaily.util.compat import subprocess

# useful programmes
BREW = shutil.which('brew')
FORTUNE = shutil.which('fortune')
COWSAY = shutil.which('cowsay')
LOLCAT = shutil.which('lolcat')

# my own quotes
DB = {
    ("N avpur bs gur ynzo vf gur tenivgnf bs n snepr.\n"
     "\n"
     "-- Wneel Funj --"),
    ("Oyrffrq ner gur zrrx.\n"
     "\n"
     "Naq oyrffrq ner gubfr jub fhssre sbe gur pnhfr bs\n"
     "evtugrbhfarff sbe gurvef vf gur xvatqbz bs urnira."),
    ("Punbf vfa'g n cvg.\n"
     "Punbf vf gur ynqqre.\n"
     "\n"
     "-- Crgle Ornyvfu --"),
    ("Gul xvatqbz pbzr.\n"
     "Gul jvyy or qbar...\n"
     "\n"
     "-- Fureybpx --"),
}


def decode():
    d = {}
    for c in (65, 97):
        for i in range(26):
            d[chr(i+c)] = chr((i+13) % 26 + c)
    return [f'echo "{"".join([d.get(c, c) for c in s])}"' for s in DB]


def install(formula):
    if BREW is None:
        return False
    try:
        subprocess.check_call([BREW, 'install', formula],
                              stdout=subprocess.DEVNULL,
                              stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        return False
    return True


def whoop_de_doo():
    s = decode()
    if FORTUNE is None:
        if install('fortune'):
            s.extend(['/usr/local/opt/fortune/bin/fortune' for _ in DB])
    else:
        s.extend([FORTUNE for _ in DB])
    fortune = random.choice(s)

    if COWSAY is None:
        if install('cowsay'):
            cowsay = '/usr/local/opt/cowsay/bin/cowsay'
        else:
            cowsay = 'cat'
    else:
        cowsay = 'cowsay'

    if LOLCAT is None:
        if install('lolcat'):
            lolcat = '/usr/local/opt/lolcat/bin/lolcat'
        else:
            lolcat = 'cat'
    else:
        lolcat = 'lolcat'

    os.system(f'{fortune} | {cowsay} | {lolcat}')


if __name__ == '__main__':
    whoop_de_doo()
