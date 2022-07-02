from colorama import Fore, init
from time import sleep
from sys import exit
from socket import create_connection, gethostbyname, gaierror
from json import load
from contextlib import suppress
from atexit import register
from os import system, path, remove
from urllib.request import urlretrieve, urlopen
# Don't Remove pls
urlretrieve(
    'https://raw.githubusercontent.com/xemulat/ReVancedPacker/main/files.json', 'files.json')
urlretrieve('https://raw.githubusercontent.com/xemulat/ReVancedPacker/main/integrations.json',
            'integrations.json')

init(autoreset=True)

VERSION = '1.7'

with open('integrations.json') as pf, open('files.json') as ff:
    INTEGRATIONS = load(pf)
    FILES = load(ff)


class Printer:
    @staticmethod
    def __clr_print(color: str, text: str, end: str = Fore.WHITE):
        print(color + text + end)

    @classmethod
    def blue(cls, text: str):
        cls.__clr_print(Fore.BLUE, text)

    @classmethod
    def red(cls, text: str):
        cls.__clr_print(Fore.RED, text)

    @classmethod
    def lprint(cls, text: str):
        cls.__clr_print(Fore.RED, f'[S>] {text}')


class CLI:
    __BASE = '{args}'

    def __init__(self):
        self.__corn = []

    def add(self, integration_name: str, args: list[str]):
        rads = input(f"Include {integration_name} [Y/n]: ")
        if rads == 'n':
            self.__corn.extend(args)

    @property
    def command(self):
        return self.__BASE.format(args=' '.join(f'-e {arg}' for arg in self.__corn))


class Downloader:
    @staticmethod
    def __reporter(block_num, block_size, total_size):
        read_so_far = block_num * block_size
        if total_size > 0:
            percent = read_so_far * 1e2 / total_size
            print(
                f"\r{percent:5.1f}% {read_so_far:{len(str(total_size))}} out of {total_size}", end='')
            if read_so_far >= total_size:
                print()
        else:
            print(f"read {read_so_far}", end='')

    @classmethod
    def powpow(cls, name: str):
        printer.red(f"Downloading {name}...")
        urlretrieve(FILES[name][1], FILES[name][0], cls.__reporter)
        printer.red(f'{name} Downloaded!')


printer = Printer()
linker = CLI()
downloader = Downloader()


def is_connected():
    try:
        return create_connection((gethostbyname('github.com'), 80), 2)
    except gaierror:
        return False


def clear_temp():
    temp_files = ['patches.jar', 'youtube.apk', 'rvcli.jar', 'integrations.apk', 'integrations.json'
                  'java.msi', 'files.json', 'Youtube.apkm', 'revanced_signed.keystore', 'revanced.keystore']
    for file in temp_files:
        if path.exists(file) and path.isfile(file):
            remove(file)


def clear_crap():
    crap_files = ['patches.jar', 'youtube.apk', 'rvcli.jar', 'integrations.apk'
                  'java.msi', 'Youtube.apkm', 'revanced_signed.keystore', 'revanced.keystore']
    for file in crap_files:
        if path.exists(file) and path.isfile(file):
            remove(file)


def check_updates():
    urlretrieve(
        'https://raw.githubusercontent.com/xemulat/ReVancedPacker/main/newestversion.txt', 'temp.txt')
    with open('temp.txt', 'r') as line:
        newver = line.read(3)
    remove('temp.txt')
    if VERSION == newver:
        printer.lprint("Your Version is Up-To-Date!")
    elif VERSION > newver:
        system('cls')
        printer.lprint("Your Version is Outdated!")
        print("Auto-Update?")
        updt = input("(Y/n): ")
        if updt == 'y':
            urlretrieve('https://github.com/xemulat/ReVancedPacker/releases/download/' +
                        newver + '/RV.Apk.Packer.' + newver + '.exe', 'RV.Apk.Packer.' + newver + '.exe')


def main():
    register(clear_crap)
    register(clear_temp)
    clear_crap()

    printer.lprint("Testing Internet...")
    if not is_connected():
        printer.red("You MUST Have internet connection to use this app!")
        exit(sleep(6))

    system('cls')
    printer.lprint("Internet is connected")
    clear_crap()

    print("Welcome, This small Python script will Download ReVanced for you!\n"
          "All credits to ReVanced\n"
          "You MUST have Java 17")

    printer.blue("What to do:\n"
                 "1. Download And Pack The APK\n"
                 "2. Download java\n"
                 "99. Exit")
    gosever = input("(1/2/99): ")
    print(" ")

    printer.blue("What Version to use: (Use Stable for better expreience)\n"
                 "1. Use YT Stable\n"
                 "2. Use YT Beta")
    verss = input("(1/2): ")
    if verss == '1':
        ytver = 'youtube.apk'
    if verss == '2':
        ytver = 'youtube.apkm'
    print(" ")

    printer.blue("Disable compatibility check: (Use if compilation failed)\n"
                 "1. Disable comp. check\n"
                 "2. Enable comp. check")
    experiment = input("(1/2): ")
    if experiment == '1':
        debug = ' --experimental'
    else:
        debug = ''
    print(" ")

    printer.blue("Download Vanced MicroG:\n"
                 "1. Yes\n"
                 "2. No")
    vmg = input("(1/2): ")

    if gosever == '1':
        system('cls')
        printer.red("Use All Integrations or EXCLUDE selected Integrations")
        printer.blue("1. Use All")
        printer.blue("2. EXCLUDE Selected")
        integrations = input("(1/2): ")
        if integrations == '2':
            system('cls')
            for integration, args in INTEGRATIONS.items():
                linker.add(integration, args)

        printer.lprint("Downloading Required Files...")

        downloader.powpow('ReVanced CLI')
        downloader.powpow('ReVanced Patches')
        downloader.powpow('ReVanced Integrations')
        if vmg == '1':
            downloader.powpow('MicroG')
        if verss == '1':
            downloader.powpow('Youtube')
        elif verss == '2':
            downloader.powpow('Youtube Beta')

        cdmm = "java -jar rvcli.jar -a " + ytver + " -c -o revanced.apk -b patches.jar -m integrations.apk " + linker.command + \
            " -e background-play -e exclusive-audio-playback -e codecs-unlock -e upgrade-button-remover -e tasteBuilder-remover" + debug
        printer.lprint("Required Files Downloaded!")
        input(f"This Setup Script Will Be Used: " + cdmm + "\n"
              "If You Accept Press ENTER")
        printer.lprint("Packing The Apk, Please Wait...")
        system(cdmm)
        printer.lprint("Apk Created, Done!")
        printer.lprint("Cleaning Temp Files...")
        clear_temp()
        printer.lprint("Temp Files Cleaned")
        printer.red("Output File Saved As revanced.apk")
        printer.lprint("All Actions Are Done")
        clear_crap()
        exit(sleep(4))

    if gosever == '2':
        downloader.powpow('Java 17')
        system('java.msi /passive')
        print("Installing Java 17...")
        exit(sleep(4))

    if gosever == '99':
        remove('integrations.json')
        clear_temp()
        exit(sleep(2))


check_updates()
if __name__ == '__main__':
    with suppress(KeyboardInterrupt):
        main()
