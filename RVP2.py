import PySimpleGUI as sg
from time import sleep
from sys import exit
from ping3 import ping
from json import load
from webbrowser import open as webopen
from os import system, rename, remove
from zipfile import ZipFile
from os.path import isfile, isdir
from urllib.request import urlretrieve
from lastversion import latest, has_update
# QuickInstall - pip install ping3 lastversion PySimpleGUI

# =====================< Downloader >=====================
def reporter(block_num, block_size, total_size):
    read_so_far = block_num * block_size
    if total_size > 0:
        percent = read_so_far * 1e2 / total_size
        print(
            f"\r{percent:5.1f}% {read_so_far:{len(str(total_size))}} out of {total_size}", end='')
        if read_so_far >= total_size:
            print()
    else:
        print(f"read {read_so_far}", end='')

def download(name, repname, link):
    print("Downloading " + name + " ...")
    print(link)
    urlretrieve(link, repname, reporter)
    print(name + ' Downloaded!')

def cleantemp():
    if KeepFiles == "False":
        if isfile("patches.jar") == True:
            remove("patches.jar")

        if isfile("integrations.apk") == True:
            remove("integrations.apk")

        if isfile("rvcli.jar") == True:
            remove("rvcli.jar")

        if isfile("revanced.keystore") == True:
            remove("revanced.keystore")

# =====================< Prep Phase >=====================

sg.theme("DarkGray15")
sg.set_options(font=("Consolas", 9), text_color='#FFFFFF')
if isfile("settings.RVP.json") == False:
    urlretrieve('https://raw.githubusercontent.com/xemulat/ReVancedPacker/main/settings.RVP', 'settings.RVP.json')
with open('settings.RVP.json') as c:
    v = load(c)
    KeepFiles = str(v["KeepFiles"])
if isfile("java.zip") == True and isdir("jv17" or "jdk-17.0.4.1+1") == False:
    if KeepFiles == "False":
        remove("java.zip")
if isdir("jv17") == False:
    if isfile("Java.zip") == False:
        download("Java 17", 'java.zip', 'https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.4.1%2B1/OpenJDK17U-jdk_x64_windows_hotspot_17.0.4.1_1.zip')
    print("Unzipping Java...")
    with ZipFile("Java.zip", "r") as fe:
        fe.extractall("")
    rename("jdk-17.0.4.1+1", "jv17")
    if KeepFiles == "False":
        remove("java.zip")
cleantemp()
javadir = "start jv17/bin/java.exe"

with open('settings.RVP.json') as f:
    d = load(f)
    KeepFiles = str(d["KeepFiles"])
    if str(d["IsDev"]) == "True":
        newver = "dev"
    else:
        newver = latest('xemulat/ReVancedPacker')
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

# =====================< Packer / Injector >=====================
def injects(file):
    isexperimental = 0
    custom = [[sg.Text('Enter integrations to add')],
              [sg.Text('*Press Enter to confirm*')],
              [sg.Text('for example "swipe-controls seekbar-tapping"\n'
                       'DON' + "'" + 'T ADD "microg-support", \nit' + "'" + 's added when you click the button(s) =>')],
              [sg.Input('', enable_events=True, key='-INTEGRATIONS-')],
              [sg.Text('')], 
              [sg.Text('')],
              [sg.Text('Coded by Xemulated')]]

    # it's really past my breaking point
    itsreallypastmybreakingpoint = [[sg.Text('Buttonz')],
                                    [sg.Text('click once')],
                                    [sg.Button('Help')],
                                    [sg.Button('Build!')],
                                    [sg.Button('Exit')],
                                    [sg.Text('')],
                                    [sg.Text('')],
                                    [sg.Text('')],
                                    [sg.Text('')]]

    custoz = [[sg.Text('Add Flags:')],
              [sg.Text('You can only click them once')],
              [sg.Button('Experimental'), sg.Button('MicroG')],
              [sg.Text('')],
              [sg.Text('')],
              [sg.Text('')],
              [sg.Text('')],
              [sg.Text('')],
              [sg.Text('')]]

    layout = [[sg.Column(custom),
               sg.VSeperator(),
               sg.Column(itsreallypastmybreakingpoint),
               sg.VSeperator(),
               sg.Column(custoz)]]

    window = sg.Window('RVP2', layout)
    down = True

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            exit()

        if event == "Help" or event == sg.WIN_CLOSED:
            webopen('https://github.com/revanced/revanced-patches#-patches')

        # it was 2AM 404Oops stop harassing me please
        if event == 'Experimental':
            isexperimental = 1

        if event == "Build!":
            if window['-INTEGRATIONS-'].get() == "":
                integrations = ""

            else:
                integrations = window['-INTEGRATIONS-'].get().replace(" ", " -i ")
                integrations = "-i " + integrations
            print("Updating Repos...")

            patchver = latest(repo='revanced/revanced-patches', output_format='version')
            cliver = latest(repo='revanced/revanced-cli', output_format='version')
            integrationsver = latest(repo='revanced/revanced-integrations', output_format='version')

            print("Repos Updated!")
            print("Downloading Required Files...")

            download("Patches", 'patches.jar', 'https://github.com/revanced/revanced-patches/releases/download/v' + str(patchver) + '/revanced-patches-' + str(patchver) + '.jar')
            download("Integrations", 'integrations.apk', 'https://github.com/revanced/revanced-integrations/releases/download/v' + str(integrationsver) + '/app-release-unsigned.apk')
            download("CLI", 'rvcli.jar', 'https://github.com/revanced/revanced-cli/releases/download/v' + str(cliver) + '/revanced-cli-' + str(cliver) + '-all.jar')

            print("Packing ReVanced...")
            addon = ""
            if isexperimental == 1:
                addon = addon + " --experimental"
            print(javadir + " -jar rvcli.jar -a " + file + " -c -o revanced.apk -b patches.jar -m integrations.apk --exclusive " + integrations)
            system(javadir + " -jar rvcli.jar -a " + file + " -c -o revanced.apk -b patches.jar -m integrations.apk --exclusive " + integrations)
            print("Done!")
            exit

def main():
    # =====================< Internet Chacker >=====================
    internet = ping("https://www.github.com/")
    if internet is None or False:
        internetac = "Unreachable"
        hcin = "#FF0000"
    else:
        internetac = "Reachable"
        hcin = "#00FF00"

    # =====================< Main Window >=====================
    custon = [[sg.Text("Version - " + vers, text_color=hcve)],
              [sg.Text("Network - " + internetac, text_color=hcin)],
              [sg.Text("")],
              [sg.Text('Enter your APK name')],
              [sg.Text('*Press Enter to confirm*')],
              [sg.Input('', enable_events=True, key='-INPUT-', ), sg.Button('Enter', visible=True, bind_return_key=True)],
              [sg.Button('Exit'), sg.Button('Help')],
              [sg.Text('')],
              [sg.Text('Coded by Xemulated')]]

    window = sg.Window('RVP2', custon)

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            exit()

        elif event == 'Enter':
            if newver == "dev":
                window.close()
                injects("youtube.apk")
            else:
                if window['-INPUT-'].get() == '':
                    pass
                elif isfile(window['-INPUT-'].get()) == False:
                    pass
                else:
                    if ".apk" in window['-INPUT-'].get():
                        window.close()
                        injects(window['-INPUT-'].get())
                    else:
                        pass

main()
