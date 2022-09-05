import PySimpleGUI as sg
from time import sleep
from sys import exit
from ping3 import ping
from json import load
from os import system
from os.path import isfile
from urllib.request import urlretrieve
from lastversion import latest, has_update
# QuickInstall - pip install ping3 lastversion PySimpleGUI

# ===============< Prep Phase >===============
sg.theme("DarkGray15")
sg.set_options(font=("Consolas", 9), text_color='#FFFFFF')
if isfile("settings.RVP") == False:
    urlretrieve('PLECEHOLDER GO BRRRRR', 'settings.RVP')
