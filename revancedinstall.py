from os import system, path, remove
from urllib.request import urlretrieve, urlopen
# Don't Remove pls
urlretrieve('https://raw.githubusercontent.com/xemulat/ReVancedPacker/main/files.json', 'files.json')
urlretrieve('https://raw.githubusercontent.com/xemulat/ReVancedPacker/main/integrations.json', 'integrations.json')

from atexit import register
from contextlib import suppress
from json import load
from socket import create_connection, gethostbyname, gaierror
from sys import exit
from time import sleep
from colorama import Fore, init

init(autoreset=True)

VERSION = '1.5'

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
    __BASE = 'java -jar rvcli.jar -a youtube.apk -c -o revanced.apk -b patches.jar -m integrations.apk {args}'

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
            print(f"\r{percent:5.1f}% {read_so_far:{len(str(total_size))}} out of {total_size}", end='')
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


def check_updates():
    with urlopen('https://raw.githubusercontent.com/xemulat/ReVancedPacker/main/newestversion.txt') as resp:
        current_version = resp.read(3).decode()

    if VERSION == current_version:
        printer.lprint('You are up-to-date.')
    else:
        printer.lprint('Script is being updated.')
        with urlopen('https://raw.githubusercontent.com/xemulat/ReVancedPacker/main/revancedinstall.py') as resp:
            content = resp.read()
        with open(__file__, 'wb') as f:
            f.write(content)
        printer.lprint('Script has been updated please restart the script.')
        exit(sleep(6))


def clear_temp():
    temp_files = ['patches.jar', 'youtube.apk', 'rvcli.jar', 'integrations.apk',
                  'revanced_signed.keystore' or 'revanced.keystore', 'java.msi']
    for file in temp_files:
        if path.exists(file) and path.isfile(file):
            remove(file)


def main():
    register(clear_temp)

    printer.lprint("Testing Internet...")
    if not is_connected():
        printer.red("You MUST Have internet connection to use this app!")
        exit(sleep(6))

    system('cls')
    printer.lprint("Internet is connected")

    check_updates()

    print("Welcome, This small Python script will Download ReVanced for you!\n"
          "All credits to ReVanced\n"
          "You MUST have Java 17")

    printer.blue("1. Download And Pack The APK\n"
                 "2. Download java\n"
                 "99. Exit")

    gosever = input("(1/99): ")
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

        for file in list(FILES)[:-1]:
            downloader.powpow(file)

        printer.lprint("Required Files Downloaded!")

        input(f"This Setup Script Will Be Used: {linker.command}\nIf You Accept Press ENTER")
        printer.lprint("Packing The Apk, Please Wait...")
        system(linker.command)

        printer.lprint("Apk Created, Done!")
        printer.lprint("Cleaning Temp Files...")
        clear_temp()
        printer.lprint("Temp Files Cleaned")
        printer.red("Output File Saved As revanced.apk")
        printer.lprint("All Actions Are Done")
        exit(sleep(4))

    if gosever == '2':
        downloader.powpow('Java 17')
        system('java.msi /passive')
        print("Installing Java 17...")
        exit(sleep(4))

    if gosever == '99':
        exit(sleep(2))


if __name__ == '__main__':
    with suppress(KeyboardInterrupt):
        main()
