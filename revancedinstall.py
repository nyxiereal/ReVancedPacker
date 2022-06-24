from os import system, path, remove as rm
from socket import create_connection, gethostbyname, gaierror
from time import sleep
from urllib.request import urlretrieve
from sys import exit
from colorama import Fore, init
init(autoreset=True)

class Printer:
    @staticmethod
    def clr_print(color: str, text: str, end: str = Fore.WHITE):
        print(color + text + end)

    def blue(self, text: str):
        self.clr_print(Fore.BLUE, text)

    def red(self, text: str):
        self.clr_print(Fore.RED, text)

    def lprint(self, text: str):
        self.clr_print(Fore.RED, f'[S>] {text}')


printer = Printer()

# Optimized Custom Integrations
corn = []

def linker(name, command):
    global corn
    rads = input(f"Include {name} [Y/n]: ")
    if rads == 'n':
        corn.append(command)


# Progress Bar And Size Reporter
def reporter(block_num, block_size, total_size):
    read_so_far = block_num * block_size
    if total_size > 0:
        percent = read_so_far * 1e2 / total_size
        print(f"\r{percent:5.1f}% {read_so_far:{len(str(total_size))}} out of {total_size}", end='')
        if read_so_far >= total_size:
            print()
    else:
        print(f"read {read_so_far}", end='')


# UrlRetriever
def powpow(name, rep_name, rep_link):
    printer.red(f"Downloading {name}...")
    urlretrieve(rep_link, rep_name, reporter)
    printer.red(f'{name} Downloaded!')


# Check Is Internet Connection
def is_connected():
    try:
        return create_connection((gethostbyname('github.com'), 80), 2)
    except gaierror:
        return False


# Main
def main():
    printer.lprint("Testing Internet...")
    if not is_connected():
        printer.red("You MUST Have internet connection to use this app!")
        exit(sleep(6))

    yourversion = '1.3'
    
    system('cls')
    printer.lprint("Internet is connected")
    urlretrieve('https://raw.githubusercontent.com/xemulat/ReVancedPacker/main/newestversion.txt', 'temp.txt')
    with open('temp.txt', 'r') as line:
        newver = line.read(3)
    rm('temp.txt')
    if newver == yourversion:
        printer.lprint("Your version is up-to-date!")
        print(" ")
    elif newver > yourversion:
        printer.lprint("Your version is outdated :(")
        print(" ")

    print("Welcome, This small Python script will Download ReVanced for you!\n"
          "All credits to ReVanced\n"
          "You MUST have java 17")

    printer.blue("1. Download And Pack The APK\n"
                 "2. Download java\n"
                 "99. Exit")

    gosever = input("(1/99): ")
    if gosever == '1':
        system('cls')
        print("Use All Integrations or EXCLUDE selected Integrations")
        printer.blue("1. Use All")
        printer.blue("2. EXCLUDE Selected")
        integrations = input("(1/2): ")

        if integrations == '2':
            system('cls')
            linker('Remove Ads', '-e general-resource-ads -e general-ads -e video-ads ')
            linker('Seekbar Tapping', '-e seekbar-tapping ')
            linker('Amoled Theme', '-e amoled ')
            linker('Premium Heading', '-e premium-heading ')
            linker('Custom Branding', '-e custom-branding ')
            linker('Hide Cast Button', '-e hide-cast-button ')
            linker('Disable Create Button', '-e disable-create-button ')
            linker('Minimized Playback', '-e minimized-playback ')
            linker('Old Quality Layout', '-e old-quality-layout ')
            linker('Hide Reels', '-e hide-reels ')
            linker('Disable Shorts Button', '-e disable-shorts-button ')
            linker('Locale Config Fix (Recommended if compilation failed)', '-e locale-config-fix ')
            linker('Include MicroG Support (Recommended on Non-Rooted Devices!)', '-e microg-support ')
            linker('Include Resource Provider For Resource Mapping (Unknown)', '-e resource-id-mapping-provider-resource-patch-dependency')

        printer.lprint("Downloading Required Files...")
        powpow('ReVanced CLI', 'RVCli.jar',
               'https://github.com/revanced/revanced-cli/releases/download/v1.11.0/revanced-cli-1.11.0-all.jar')
        powpow('ReVanced Patches', 'Patches.jar',
               'https://github.com/revanced/revanced-patches/releases/download/v1.10.1/revanced-patches-1.10.1.jar')
        powpow('ReVanced Integrations', 'Integrations.apk',
               'https://github.com/revanced/revanced-integrations/releases/download/v0.13.0/app-release-unsigned.apk')
        powpow('YouTube', 'youtube.apk',
               'https://github.com/xemulat/MyFilesForDDL/releases/download/youtube/youtube.apk')
        printer.lprint("Required Files Downloaded!")
        print(f"This Setup Script Will Be Used: java -jar rvcli.jar -a youtube.apk -c -o revanced.apk -b patches.jar -m integrations.apk {''.join(corn)}")
        input("If You Accept Press ENTER")
        printer.lprint("Packing The Apk, Please Wait...")
        system(f'java -jar rvcli.jar -a youtube.apk -c -o revanced.apk -b patches.jar -m integrations.apk {"".join(corn)}')
        printer.lprint("Apk Created, Done!")
        printer.lprint("Cleaning Temp Files...")
        rm('Patches.jar')
        rm('youtube.apk')
        rm('RVCli.jar')
        rm('Integrations.apk')
        if path.exists('revanced_signed.keystore'):
            rm('revanced_signed.keystore')
        elif path.exists('revanced.keystore'):
            rm('revanced.keystore')
        printer.lprint("Temp Files Cleaned")
        printer.red("Output File Saved As revanced.apk")
        printer.lprint("All Actions Are Done")
        exit(sleep(4))

    if gosever == '2':
        powpow('Java 17', 'Java.msi', 'https://github.com/xemulat/MyFilesForDDL/releases/download/jdk/java.msi')
        system('Java.msi /passive')
        print("Installing Java 17...")
        rm("Java.msi")
        exit(sleep(4))

    if gosever == '99':
        exit(sleep(2))


if __name__ == '__main__':
    main()

    
