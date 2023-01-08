from os import system, startfile, remove
from requests import get
from platform import system as platform
from os.path import isfile, isdir
from sys import exit
from time import sleep
try:
    from tqdm import tqdm
    from XeLib import cls, printer, download
    from lastversion import latest
    from ping3 import ping
    from colorama import init, Fore
except:
    print("Installing packages...")
    system("python -m pip install XeLib lastversion ping3 tqdm wget")

init(autoreset=True)

def achooser(choose, option):
    if option == choose or option.upper() == choose or option.capitalize() == choose or option.title() == choose or option.lower() == choose: return True

def rm(file):
    if not isfile('norm.cnf'):
        if isfile(file) == True:
            remove(file)

def removetmp():
    rm('cli.jar')
    rm('patches.jar')
    rm('integrations.apk')

def update():
    print('Update?')
    doupdate = input("("+Fore.GREEN+"Y"+Fore.WHITE+"/"+Fore.RED+"n"+Fore.WHITE + "): ")
    if achooser(doupdate, "n"):
        print("Okey.")
        sleep(2)
        pass
    elif achooser(doupdate, "y"):
        printer.lprint("Updating...")
        try:
            download("https://github.com/xemulat/ReVancedPacker/releases/latest/download/RVP.exe", "RVP."+str(latest("xemulat/ReVancedPacker"))+".exe", 'RVP Update')
            startfile("RVP."+str(latest("xemulat/ReVancedPacker"))+".exe")
            exit()
        except:
            printer.lprint("Can't complete updates, aborting...") ; sleep(4) ; exit()

# Prep
cls()
printer.lprint('Removing TEMP files...')
removetmp()

# Get links
api_url = 'https://releases.revanced.app/tools'
resp = get(api_url).json()
printer.lprint("Setting up...")

h = (((resp['tools'])[0])['browser_download_url'])

if isfile("Integrations.apk") == False:
    download((((resp['tools'])[4])['browser_download_url']), "integrations.apk", "ReVanced Integrations")

if isfile("Patches.jar") == False:
    download((((resp['tools'])[3])['browser_download_url']), "patches.jar", "ReVanced Patches")

if isfile("cli.jar") == False:
    download((((resp['tools'])[6])['browser_download_url']), "cli.jar", "ReVanced CLI")

# Get patches
api_url = 'https://releases.revanced.app/patches'
resp = get(api_url).json()
version = 2.5
init(autoreset=True)

newver = latest("xemulat/ReVancedPacker")
if str(version) == str(newver):
    state = 'Up-To-Date'

elif str(newver) > str(version):
    # Triggers the update after outdated version is detected
    state = 'Outdated'
    update()

else:
    state = 'cant'

def main():
    cls()
    javapath = 'java'
    print(f"Welcome to RVP v{version}!\n"
          f"RVP is {state}\n"
          f"Internet: {str(round(ping('github.com', unit='ms'), 2))}ms\n"
          f"")

    print("[1] Pack ReVanced\n"
          "[2] Show Integrations\n"
          "[3] Download Java\n"
          "[99] Exit")
    choose = input("> ")

    if choose == "1":
        cls()
        print("Choose what app to pack:")
        print("[1] YouTube\n"
              "[2] YouTube Music\n"
              "[3] TikTok\n"
              "[4] Reddit\n"
              "[5] Spotify\n"
              "[6] Twitter\n"
              "[7] Crunchyroll\n"
              "[8] Twitch")

        choosee = input("> ")
        if   choosee == "1": integration = 'com.google.android.youtube'
        elif choosee == "2": integration = 'com.google.android.apps.youtube.music'
        elif choosee == "3": integration = 'com.ss.android.ugc.trill'
        elif choosee == "4": integration = 'com.reddit.frontpage'
        elif choosee == "5": integration = 'com.spotify.music'
        elif choosee == "6": integration = 'com.twitter.android'
        elif choosee == "7": integration = 'com.crunchyroll.crunchyroid'
        elif choosee == "8": integration = 'tv.twitch.android.app'
        else: print(f"No item named {choose}...") ; sleep(6) ; main()

        print('Disable patch version compatibility?')
        chooosee = input('(Y/n): ')
        if chooosee == achooser(chooosee, 'y'):
            patches = '--experimental'
        else:
            patches = ""

        z = True
        x = 0
        print("Select patches to add to your app:\n"
              "[1] All Integrations\n"
              "[2] Only Selected Integration")
        pacches = input("> ")

        if pacches == '1':
            while z == True:
                if integration == 'com.ss.android.ugc.trill':
                    try:
                        if (((resp[x])['compatiblePackages'])[0])['name'] == integration:
                            patches = patches + " -i " + str((resp[x])['name'])
                        x = x + 1
                    except: z = False

                else:
                    try:
                        if (((resp[x])['compatiblePackages'])[0])['name'] == integration:
                            patches = patches + " -i " + str((resp[x])['name'])
                        x = x + 1
                    except: z = False

        elif pacches == '2':
            while z == True:
                if integration == 'com.ss.android.ugc.trill':
                    try:
                        if (((resp[x])['compatiblePackages'])[0])['name'] == integration:
                            choose = input(str((resp[x])['name']) + " > ")
                            if achooser(choose, 'y'):
                                patches = patches + " -i " + str((resp[x])['name'])
                            else:
                                patches = patches + " -e " + str((resp[x])['name'])
                        x = x + 1
                    except: z = False

                else:
                    try:
                        if (((resp[x])['compatiblePackages'])[0])['name'] == integration:
                            choose = input(str((resp[x])['name']) + " > ")
                            if achooser(choose, 'y'):
                                patches = patches + " -i " + str((resp[x])['name'])
                            else:
                                patches = patches + " -e " + str((resp[x])['name'])
                        x = x + 1
                    except: z = False

        c = True

        if achooser(choosee, '1' or '2'):
            print("Do you want to download MicroG? It's required for YouTube ReVanced and YouTube Music ReVanced.")
            choosemicrog = input('(Y/n): ')
            if achooser(choosemicrog, 'y'):
                while c:
                    print('What MicroG to download?\n'
                        '[1] Vanced MicroG (oldest)\n'
                        "[2] Inotia's MicroG (latest)")

                    secondmicrogchoose = input('> ')
                    if achooser(secondmicrogchoose, '1'):
                        download(str(h), 'MicroG.apk', 'Vanced MicroG')
                        c = False

                    elif achooser(secondmicrogchoose, '2'):
                        download('https://github.com/inotia00/VancedMicroG/releases/latest/download/microg.apk', 'InoMicroG.apk', "Inotia's MicroG")
                        c = False

                    else: print(f"No item named {choose}...") ; sleep(2)
        
        if   achooser(choosee, "1"): download("https://d.apkpure.com/b/APK/com.google.android.youtube?version=latest", "YouTube.apk", "youtube") ; inputapk = "YouTube.apk" ; patches = patches + ' -i settings'
        elif achooser(choosee, "2"): download("https://d.apkpure.com/b/APK/com.google.android.apps.youtube.music?version=latest", "YouTubeMusic.apk", "YouTubeMusic") ; inputapk = "YouTubeMusic.apk" ; patches = patches + ' -i settings'
        elif achooser(choosee, "3"): download("https://d.apkpure.com/b/APK/com.zhiliaoapp.musically?version=latest", "TikTok.apk", "TikTok") ; inputapk = "TikTok.apk"
        elif achooser(choosee, "4"): download("https://d.apkpure.com/b/APK/com.reddit.frontpage?version=latest", "Reddit.apk", "Reddit") ; inputapk = "Reddit.apk"
        elif achooser(choosee, "5"): download("https://d.apkpure.com/b/APK/com.spotify.music?versionCode=94112650", "Spotify.apk", "Spotify") ; inputapk = "Spotify.apk"
        elif achooser(choosee, "6"): download("https://d.apkpure.com/b/APK/com.twitter.android?version=latest", "Twitter.apk", "Twitter") ; inputapk = "Twitter.apk"
        elif achooser(choosee, "7"): download("https://d.apkpure.com/b/APK/com.crunchyroll.crunchyroid?version=latest", "Crunchyroll.apk", "Crunchyroll") ; inputapk = "Crunchyroll.apk"
        elif achooser(choosee, "8"): download("https://d.apkpure.com/b/APK/tv.twitch.android.app?version=latest", "Twitch.apk", "Twitch") ; inputapk = "Twitch.apk"
        else: print(f"No item named {choose}...") ; sleep(6) ; main()

        cli = javapath + f" -jar cli.jar -a {inputapk} -b patches.jar -m integrations.apk --experimental --clean -o revanced.apk" + patches

        print(f'Are you sure you want to run:\n{cli}')
        finalchoose = input('(Y/n): ')
        if not achooser(finalchoose, 'y'):
            print('Exiting...')
            exit(sleep(3))

        system(cli)
        print('Cleaning TEMP files...')
        removetmp()
        exit()

    elif choose == "2":
        cls()
        while True:
            print("Show Integrations from:\n"
                "[1] YouTube\n"
                "[2] YouTube Music\n"
                "[3] TikTok\n"
                "[4] Reddit\n"
                "[5] Spotify\n"
                "[6] Twitter\n"
                "[7] Crunchyroll\n"
                "[8] Twitch")

            choose = input("> ")
            if   choose == "1": integration = 'com.google.android.youtube'
            elif choose == "2": integration = 'com.google.android.apps.youtube.music'
            elif choose == "3": integration = 'com.ss.android.ugc.trill'
            elif choose == "4": integration = 'com.reddit.frontpage'
            elif choose == "5": integration = 'com.spotify.music'
            elif choose == "6": integration = 'com.twitter.android'
            elif choose == "7": integration = 'com.crunchyroll.crunchyroid'
            elif choose == "8": integration = 'tv.twitch.android.app'
            else: print(f"No item named {choose}...") ; sleep(6) ; main()
            x = 0
            z = True

            while z == True:
                if integration == 'com.ss.android.ugc.trill':
                    try:
                        if (((resp[x])['compatiblePackages'])[0])['name'] == integration:
                            printer.red("┌────────────────────────────────────────────────────")
                            print(Fore.RED+"│ "+Fore.RESET + str((resp[x])['name']))
                            print(Fore.RED+"│ "+Fore.RESET + str((resp[x])['description']))
                        x = x + 1
                    except: z = False

                else:
                    try:
                        if (((resp[x])['compatiblePackages'])[0])['name'] == integration:
                            printer.red("┌────────────────────────────────────────────────────")
                            print(Fore.RED+"│ "+Fore.RESET + str((resp[x])['name']))
                            print(Fore.RED+"│ "+Fore.RESET + str((resp[x])['description']))
                        x = x + 1
                    except: z = False
            print("\nGo Back")
            choose = input("> ")
            main()
    elif choose == "3": download("https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.5%2B8/OpenJDK17U-jdk_x64_windows_hotspot_17.0.5_8.msi", "java17.msi", "Java 17") ; startfile("java17.msi")
    elif choose == '99': exit()
    else: print(f"No item named {choose}...") ; sleep(6) ; main()

main()
