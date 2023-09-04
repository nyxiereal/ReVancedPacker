from os import system
from requests import get, head
from rich.progress import Progress
from re import match as rematch
from subprocess import run, PIPE

# replace the ` ` with an `-` in url encoding, shit just fucking works
def caseConverter(inp):
    return(inp.replace(' ', '-').lower())

# `cls` shortcut
def cls():
    system('cls')

# Y/n quick question shortcut
def yn():
    inp = input('(N/y) ')
    if inp.lower() == 'y':
        return(True)
    else:
        return(False)

# Downloads the file from any source
# Uses rich's progress bar tracking
def download(url, fnam, name):
    headers = {'Accept-Encoding': 'gzip, deflate',
                'User-Agent': 'Mozilla/5.0',
                'cache_control': 'max-age=600',
                'connection': 'keep-alive'}

    response = head(url, headers=headers)
    total_size = int(response.headers.get("content-length", 0))

    with Progress() as progress:
        task = progress.add_task(f"[blue]:: Downloading {name}", total=total_size)

        with open(fnam, "wb") as file:

            response = get(url, stream=True)
            chunk_size = 1024  # You can adjust this value as needed

            # the shits that writes the data and updates the progress bar every 1kib
            for data in response.iter_content(chunk_size=chunk_size):
                file.write(data)
                progress.update(task, completed=file.tell())
                
# Shortens the file names so they are shorter ¯\_(ツ)_/¯
def convertFilename(inp):
    if 'revanced-cli' in inp:
        return('cli.jar')
    elif 'revanced-integrations' in inp:
        return('integrations.apk')
    elif 'revanced-patches' in inp:
        return('patches.jar')
    
# this fucking shit converts ex. patches.jar to ReVanced Patches
# Used in the downloader
def fuckingConverter(inp):
    return(f"ReVanced {inp.split('.')[0].capitalize()}")

def javaCheck():
    try:
        result = run(['java', '-version'], stdout=PIPE, stderr=PIPE, text=True)
        if result.returncode == 0:
            if '17.' in result.stderr:
                return True
        else:
            return False
    except:
        return False
