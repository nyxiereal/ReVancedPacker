from os import system, path, remove as rm
from socket import create_connection, gethostbyname, gaierror
from time import sleep
from urllib.request import urlretrieve

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
        exit()

    system('cls')
    printer.lprint("Internet is connected")

    print("Welcome, This small Python script will Download ReVanced for you!\n"
          "All credits to ReVanced\n"
          "You MUST have java 17")

    printer.blue("1. Download And Pack The APK\n"
                 "2. Download java\n"
                 "99. Exit")

    gosever = input("(1/99): ")
    if gosever == '1':
        print("Use All Integrations or EXCLUDE selected Integrations")
        printer.blue("1. Use All")
        printer.blue("2. EXCLUDE Selected")
        integrations = input("(1/2): ")

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
            linker('Locale Config Fix (Recommended if compilation failed)', 'locale-config-fix')
            linker('Include MicroG Support (Recommended on Non-Rooted Devices!)', 'microg-support')
            linker('resource-id-mapping-provider-resource-patch-dependency',
                   'Include Resource Provider For Resource Mapping (Unknown))')

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
        print(f"This Setup Script Will Be Used: java -jar rvcli.jar -a youtube.apk -c -o revanced.apk -b patches.jar -m integrations.apk {' -e '.join(corn)}")
        input("If You Accept Press ENTER")
        printer.lprint("Packing The Apk, Please Wait...")
        system(f'java -jar rvcli.jar -a youtube.apk -c -o revanced.apk -b patches.jar -m integrations.apk {" -e ".join(corn)}')
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

    
