from urllib.request import urlretrieve
import sys
from time import sleep
from os import system, startfile, path, remove as rm
from socket import gethostbyname, create_connection
from colorama import Fore, init
init(autoreset=True)

#Optimized Custom Integrations
corn = ''
def linker(name, command):
    global corn
    print(" ")
    WPrint("Include " + name)
    rads = input("(y/n): ")
    if rads == 'n':
        corn = corn + ' -e ' + command
    else:
        test = 'test'

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
    
def LPrint(prentr):
    print(Fore.RED + "[S>] " + prentr)
    
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
    WPrint("You MUST have java 17")
    BPrint("1. Download And Pack The APK")
    BPrint("2. Download java")
    BPrint("99. Exit")
    gosever = input("(1/99): ")
    if gosever == '1':
        WPrint("Use All Integrations or EXCLUDE selected Integrations")
        BPrint("1. Use All")
        BPrint("2. EXCLUDE Selected")
        integrations = input("(1/2): ")
        if integrations == '1':
            print(" ")
        
        if integrations == '2':
            linker('Remove Ads', 'general-resource-ads -e general-ads -e video-ads')
            linker('Seekbar Tapping', 'seekbar-tapping')
            linker('Amoled Theme', 'amoled')
            linker('Premium Heading', 'premium-heading')
            linker('Custom Branding', 'custom-branding')
            linker('Hide Cast Button', 'hide-cast-button')
            linker('Disable Create Button', 'disable-create-button')
            linker('Minimized Playback', 'minimized-playback')
            linker('Old Quality Layout', 'old-quality-layout')
            linker('Hide Reels', 'hide-reels')
            linker('Disable Shorts Button', 'disable-shorts-button')
            linker('Locale Config Fix (Reccomended if compilation failed)', 'locale-config-fix')
            linker('Include MicroG Support (Reccomended on Non-Rooted Devices!)', 'microg-support')
            linker('resource-id-mapping-provider-resource-patch-dependency', 'Include Resource Provider For Resource Mapping (Unknown))')
                
        LPrint("Downloading Required Files...")
        powpow('ReVanced CLI', 'RVCli.jar', 'https://github.com/revanced/revanced-cli/releases/download/v1.11.0/revanced-cli-1.11.0-all.jar')
        powpow('ReVanced Patches', 'Patches.jar', 'https://github.com/revanced/revanced-patches/releases/download/v1.10.1/revanced-patches-1.10.1.jar')
        powpow('ReVanced Integrations', 'Integrations.apk', 'https://github.com/revanced/revanced-integrations/releases/download/v0.13.0/app-release-unsigned.apk')
        powpow('YouTube', 'youtube.apk', 'https://github.com/xemulat/MyFilesForDDL/releases/download/youtube/youtube.apk')
        LPrint("Required Files Downloaded!")
        print(" ")
        WPrint("This Setup Script Will Be Used: java -jar rvcli.jar -a youtube.apk -c -o revanced.apk -b patches.jar -m integrations.apk" + corn)
        input("If You Accept Press ENTER")
        LPrint("Packing The Apk, Please Wait...")
        system('java -jar rvcli.jar -a youtube.apk -c -o revanced.apk -b patches.jar -m integrations.apk' + corn)
        LPrint("Apk Created, Done!")
        print(" ")
        LPrint("Cleaning Temp Files...")
        rm('Patches.jar')
        rm('youtube.apk')
        rm('RVCli.jar')
        rm('Integrations.apk')
        if path.exists('revanced_signed.keystore') == True:
            rm('revanced_signed.keystore')
        elif path.exists('revanced.keystore') == True:
            rm('revanced.keystore')
        LPrint("Temp Files Cleaned")
        RPrint("Output File Saved As revanced.apk")
        LPrint("All Actions Are Done")
        exit(sleep(4))
        
    if gosever == '2':
        powpow('Java 17', 'Java.msi', 'https://github.com/xemulat/MyFilesForDDL/releases/download/jdk/java.msi')
        system('Java.msi /passive')
        WPrint("Installing Java 17...")
        rm("Java.msi")
        exit(sleep(4))

    if gosever == '99':
        exit(sleep(2))
