from urllib.request import urlretrieve
import sys
from time import sleep
from webbrowser import open as webopen
from os import system, startfile, remove as rm
from socket import gethostbyname, create_connection
from colorama import Fore, init
init(autoreset=True)

#Progress Bar And Size Reporter
def reporter(blocknum, blocksize, totalsize):
    readsofar = blocknum * blocksize
    if totalsize > 0:
        percent = readsofar * 1e2 / totalsize
        s = "\r%5.1f%% %*d out of %d" % (
            percent, len(str(totalsize)), readsofar, totalsize)
        sys.stderr.write(s)
        if readsofar >= totalsize:
            sys.stderr.write("\n")
    else:
        sys.stderr.write("read %d\n" % (readsofar,))

#TESTING! Optimized print function
def BPrint(prent):
    print(Fore.BLUE + prent)

def RPrint(prentr):
    print(Fore.RED + prentr)

def WPrint(prentw):
    print(Fore.WHITE + prentw)

#UrlRetriever
def powpow(name, repname, replink):
    print(" ")
    RPrint("Downloading " + name + "...")
    urlretrieve(replink, repname, reporter)
    RPrint(name + " Downloaded!")

#Check Is Internet Connection
def is_connected():
  try:
    host = gethostbyname("github.com")
    s = create_connection((host, 80), 2)
    return 'Yes'
  except:
     pass
  return 'No'

#Main
system('cls')
RPrint("[S>] Testing Internet...")
if is_connected() == 'Yes':
    system('cls')
    RPrint("[S>] Internet is connected")
    print(" ")
    WPrint("Welcome, This small Python script will Download ReVanced for you!")
    WPrint("All credits to ReVanced")
    WPrint("You MUST Have Java 17!!! Download it from adoptium.net/download")
    BPrint("1. Download And Pack The APK")
    BPrint("99. Exit")
    gosever = input("(1/99): ")
    if gosever == '1':
        RPrint("Downloading Required Files...")
        powpow('ReVanced CLI', 'RVCli.jar', 'https://github.com/revanced/revanced-cli/releases/download/v1.7.0/revanced-cli-1.7.0-all.jar')
        powpow('ReVanced Patches', 'Patches.jar', 'https://github.com/revanced/revanced-patches/releases/download/v1.9.1/revanced-patches-1.9.1.jar')
        powpow('ReVanced Integrations', 'Integrations.apk', 'https://github.com/revanced/revanced-integrations/releases/download/v0.11.0/app-release-unsigned.apk')
        powpow('YouTube', 'youtube.apk', 'https://github.com/xemulat/MyFilesForDDL/releases/download/youtube/youtube.apk')
        RPrint("Required Files Downloaded!")
        RPrint("Packing The Apk, Please Wait...")
        system('java -jar RVCli.jar -a youtube.apk -c -o revanced.apk -b Patches.jar -m Integrations.apk')
        RPrint("Apk Created, Done!")
        print(" ")
        RPrint("Cleaning temp files...")
        rm('Patches.jar')
        rm('youtube.apk')
        rm('RVCli.jar')
        rm('Integrations.apk')
        rm('revanced_signed.keystore')
        exit(sleep(4))
    if gosever == '99':
        exit(sleep(2))