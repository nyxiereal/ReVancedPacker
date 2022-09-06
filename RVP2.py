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
    urlretrieve('https://raw.githubusercontent.com/xemulat/ReVancedPacker/main/settings.RVP', 'settings.RVP')
with open('settings.RVP') as f:
        d = load(f)
        print(str(d["KeepFiles"]))
        if str(d["IsDev"]) == "True":
            newver = "dev"
        else:
            newver = latest('xemulat/VirusVideoMaker')
        if "1.2" == str(newver):
            vers = "Up-To-Date"
            hcve = "#00FF00"
        elif str(newver) == "dev":
            vers = "Dev build, not checking for updates"
            hcve = "#74D962"
        elif str(newver) > "1.2":
            vers = "Outdated, download it from my github"
            hcve = "#FF0000"
        else:
            vers = "error checking updates :("
            hcve = "#FFFF00"
        print("Build: " + str(newver))

# ===============< Packer / Injector >===============
def injects(file):

def main():
    # ===============< Internet Chacker >===============
    internet = ping("https://www.github.com/")
    if internet is None or False:
        internetac = "Unreachable"
        hcin = "#FF0000"
    else:
        internetac = "Reachable"
        hcin = "#00FF00"

    # ===============< Main Window >===============
    custom = [[sg.Text("Version - " + vers, text_color=hcve)],
              [sg.Text("Network - " + internetac, text_color=hcin)],
              [sg.Text("")],
              [sg.Text('Enter your APK name')],
              [sg.Text('*Press Enter to confirm*')],
              [sg.Input('', enable_events=True, key='-INPUT-', ), sg.Button('Enter', visible=True, bind_return_key=True)],
              [sg.Button('Exit'), sg.Button('Enter')],
              [sg.Text('')],
              [sg.Text('Coded by Xemulated')]]

    window = sg.Window('RVP2', custom)

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            exit()

        elif event == 'Enter':
            if window['-INPUT-'].get() == '':
                pass
            elif isfile(window['-INPUT-'].get()) == False:
                pass
            else:
                window.close()
                injects(window['-INPUT-'].get())
main()
