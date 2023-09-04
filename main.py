# Imported (site-packages)
from sys import exit
from zipfile import ZipFile
from os import system
from time import sleep

# Imported (PYPI)
from rich.progress import Progress
from orjson import loads
from bs4 import BeautifulSoup
from requests import get, head

from tools import caseConverter, cls, yn, download, convertFilename, fuckingConverter, javaCheck

def getpatches(app: str = 'com.google.android.youtube'):
    # Get, decode, parse the API
    r = ((get('https://api.revanced.app/v2/patches/latest').content).decode('utf-8'))

    # Load the response into memory
    r = loads(r)
    r = r['patches']

    # Set a blank list, then populate it
    patches = []

    # Create a Progress object
    with Progress() as progress:
        task = progress.add_task("[blue]:: Fetching Patches", total=len(r))
        
        for item in r:
            compatible_packages = item['compatiblePackages']
            for package in compatible_packages:
                if package['name'] == app:
                    name = item['name']
                    patches.append(caseConverter(name))
            progress.advance(task, 1)  # Update the progress bar
    
    return patches

def gettools():
    data = (loads((get('https://api.revanced.app/tools').content).decode('utf-8')))['tools']

    tools = []
    for i in data:
        iurl = i['browser_download_url']
        iname = i['name']
        if not ('.json' in iurl or 'manager' in iurl or 'tarball' in iurl):
            tools.append([iurl, iname])
    return(tools)

def getCompatibleVersion(app: str = 'com.google.android.youtube'):
    # Get, decode, parse the API
    r = ((get('https://api.revanced.app/v2/patches/latest').content).decode('utf-8'))

    # Load the response into the memory
    r = loads(r)
    r = r['patches']

    # Get the version from the API
    for item in r:
        compatible_packages = item['compatiblePackages']
        for package in compatible_packages:
            if package['name'] == app:
                return(max(package['versions'], key=lambda x: tuple(map(int, x.split('.')))))

def getYouTubeAPKUrl():
    with Progress() as progress:
        task = progress.add_task(f"[blue]:: Fetching the YouTube APK", total=100)
        # Get the version from the function above, replace `.` with `-` for the url
        version_itemized = str(getCompatibleVersion()).replace('.', '-')
        progress.advance(task, 10)
        
        # Set the headers for web scraping (ddos protection/robots.txt)
        headers = {'Accept-Encoding': 'gzip, deflate',
                'User-Agent': 'Mozilla/5.0',
                'cache_control': 'max-age=600',
                'connection': 'keep-alive'}

        # Scrape the url of the YouTube APK
        r = get(f'https://www.apkmirror.com/apk/google-inc/youtube/youtube-{version_itemized}-release/youtube-{version_itemized}-android-apk-download/', headers=headers)
        progress.advance(task, 10)
        soup = BeautifulSoup(r.content, 'html.parser')
        progress.advance(task, 10)

        # Find the download button
        element = soup.find("a", {"class": "downloadButton"})
        progress.advance(task, 10)
        url1 = f"https://www.apkmirror.com/{element['href']}"
        progress.advance(task, 10)
        
        # Fetch the direct download URL for the APK
        r = get(url1, headers=headers)
        progress.advance(task, 10)
        soup = BeautifulSoup(r.content, 'html.parser')
        progress.advance(task, 10)
        
        # Get the download button position and send a head request to it
        url2 = soup.find('a', {'rel': 'nofollow', 'data-google-vignette': 'false'})
        progress.advance(task, 10)
        h = (f"https://www.apkmirror.com{url2['href']}")
        progress.advance(task, 10)
        
        response = head(h, allow_redirects=True, headers=headers)
        progress.advance(task, 10)

        return(response.url)

def main():
    v = ''
    while v != '1':
        cls()
        # TODO: updater and version display
        print(f'ReVancedPacker \n\n'
            '1. Compile ReVanced\n'
            '99. Exit\n')
        v = input('> ')
        if v == '1':
            cls()
            # Root check
            print('Is your device rooted?')
            isRooted = yn()
            
            # Download files
            cls()
            download(getYouTubeAPKUrl(), 'youtube.apk', 'YouTube')
            for i in gettools():
                download(i[0], convertFilename(i[1]), fuckingConverter(convertFilename(i[1])))

            # Prep env, check if java 17 is in path
            if javaCheck() == False:
                download('https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.8.1%2B1/OpenJDK17U-jre_x86-32_windows_hotspot_17.0.8.1_1.zip', 'java.zip', 'Java 17')
                with ZipFile('java.zip', 'r') as z:
                    z.extractall('java')
                    z.close()
                javaPath = './java/jdk-17.0.8.1+1-jre/bin/java.exe'

            else:
                javaPath = 'java'

            # Prep patches for compilation
            patches = getpatches()
            
            patchesFinal = ''
            for i in patches:
                if isRooted == True:
                    if 'microg' in i:
                        pass
                    else:
                        patchesFinal = patchesFinal + f' -i {i}'
                else:
                    patchesFinal = patchesFinal + f' -i {i}'
                    
            # Patch the app
            
            
            cmd = f'{javaPath} -jar cli.jar patch -b patches.jar -o output.apk -m integrations.apk --exclusive {patchesFinal} youtube.apk'
            system(cmd)
        elif v == '99':
            exit()
        elif v == '69':
            print('balsl')
            sleep(2)
            exit()
        else:
            pass

# big balls
main()
