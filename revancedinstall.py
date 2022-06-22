from urllib.request import urlretrieve
import sys
from time import sleep
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

corn = ''

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
            WPrint("Include Remove Ads?")
            rads = input("(y/n): ")
            if rads == 'n':
                corn = corn + ' -e general-resource-ads -e general-ads -e video-ads'
            else:
                test = 'test'
            
            print(" ")
            WPrint("Include Seekbar Tapping?")
            rads = input("(y/n): ")
            if rads == 'n':
                corn = corn + ' -e seekbar-tapping'
            else:
                test = 'test'

            print(" ")
            WPrint("Include Amoled Theme?")
            rads = input("(y/n): ")
            if rads == 'n':
                corn = corn + ' -e amoled'
            else:
                test = 'test'

            print(" ")
            WPrint("Include Premium Heading?")
            rads = input("(y/n): ")
            if rads == 'n':
                corn = corn + ' -e premium-heading'
            else:
                test = 'test'

            print(" ")
            WPrint("Include Custom Branding?")
            rads = input("(y/n): ")
            if rads == 'n':
                corn = corn + ' -e custom-branding'
            else:
                test = 'test'

            print(" ")
            WPrint("Include Hide Cast Button?")
            rads = input("(y/n): ")
            if rads == 'n':
                corn = corn + ' -e hide-cast-button'
            else:
                test = 'test'

            print(" ")
            WPrint("Include Disable Create Button?")
            rads = input("(y/n): ")
            if rads == 'n':
                corn = corn + ' -e disable-create-button'
            else:
                test = 'test'

            print(" ")
            WPrint("Include Minimized Playback?")
            rads = input("(y/n): ")
            if rads == 'n':
                corn = corn + ' -e minimized-playback'
            else:
                test = 'test'
        
            print(" ")
            WPrint("Include Old Quality Layout")
            rads = input("(y/n): ")
            if rads == 'n':
                corn = corn + ' -e old-quality-layout'
            else:
                test = 'test'
        
            print(" ")
            WPrint("Include Hide Reels")
            rads = input("(y/n): ")
            if rads == 'n':
                corn = corn + ' -e hide-reels'
            else:
                test = 'test'
        
            print(" ")
            WPrint("Include Disable Shorts Button")
            rads = input("(y/n): ")
            if rads == 'n':
                corn = corn + ' -e disable-shorts-button'
            else:
                test = 'test'
        
            print(" ")
            WPrint("Include Locale Config Fix")
            rads = input("(y/n): ")
            if rads == 'n':
                corn = corn + ' -e locale-config-fix'
            else:
                test = 'test'
        
            print(" ")
            WPrint("Include MicroG Support (Reccomended on Non-Rooted Devices!)")
            rads = input("(y/n): ")
            if rads == 'n':
                corn = corn + ' -e microg-support'
            else:
                test = 'test'
        
            print(" ")
            WPrint("Include Resource Provider For Resource Mapping (Not Reccomended)")
            rads = input("(y/n): ")
            if rads == 'n':
                corn = corn + ' -e resource-id-mapping-provider-resource-patch-dependency'
            else:
                test = 'test'
                
        LPrint("Downloading Required Files...")
        powpow('ReVanced CLI', 'RVCli.jar', 'https://github.com/revanced/revanced-cli/releases/download/v1.7.0/revanced-cli-1.7.0-all.jar')
        powpow('ReVanced Patches', 'Patches.jar', 'https://github.com/revanced/revanced-patches/releases/download/v1.9.1/revanced-patches-1.9.1.jar')
        powpow('ReVanced Integrations', 'Integrations.apk', 'https://github.com/revanced/revanced-integrations/releases/download/v0.11.0/app-release-unsigned.apk')
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
        rm('revanced_signed.keystore')
        LPrint("Temp Files Cleaned...")
        exit(sleep(4))

    if gosever == '2':
        powpow('Java 17', 'Java.msi', 'https://github.com/xemulat/MyFilesForDDL/releases/download/jdk/java.msi')
        startfile('Java.msi')
        exit(sleep(3))

    if gosever == '99':
        exit(sleep(2))
