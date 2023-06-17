# Imported (PyQt5)
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget, QCheckBox, QLineEdit, QPushButton, QListWidgetItem, QProgressDialog, QInputDialog
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtGui import QPalette, QColor

# Imported (site-packages)
from glob import glob
from json import loads, dump
from zipfile import ZipFile
from sys import argv, exit
from os import remove, rmdir
from os.path import isdir, isfile
from subprocess import check_output, CREATE_NO_WINDOW, Popen, CREATE_NEW_CONSOLE
from re import findall, MULTILINE
from shutil import move
from time import sleep

# Imported (Selenium WebDriver)
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Imported (PYPI)
from psutil import process_iter
from requests import Session, get
from requests.adapters import HTTPAdapter

# Imported (Xem's libraries)
from XeLib import cls

cls()

def gettools():
    data = (loads((get('https://releases.revanced.app/tools').content).decode('utf-8')))['tools']

    tools = []
    for i in data:
        iurl = i['browser_download_url']
        if ('/revanced/revanced-patches' in iurl and '.jar' in iurl) or ('/revanced/revanced-cli' in iurl and '.jar' in iurl) or ('/revanced/revanced-integrations' in iurl and '.apk' in iurl) :
            tools.append([i['browser_download_url'], i['name']])
    return(tools)

def getdeviceid():
    output = check_output('cd platform-tools && .\\adb.exe devices', shell=True, creationflags=CREATE_NO_WINDOW).decode('utf-8')
    authorized = findall(r'(\w+)\tdevice', output, MULTILINE)
    unauthorized = findall(r'(\w+)\tunauthorized', output, MULTILINE)

    if authorized:
        return [authorized[0]]
    elif unauthorized:
        return [unauthorized[0], 'ACCEPT THE DEBUGGING PROMPT', 'AND RELAUNCH THIS WIDGET']
    else:
        return ['NO DEVICE FOUND', 'ENABLE USB DEBUGGING', 'AND USB INSTALLATION', 'IN DEVELOPER SETTINGS', 'AFTER RECONNECTING', 'RELAUNCH THIS WIDGET']

def getpatches(app: str = 'com.google.android.youtube'):
    r = loads(((get('https://releases.revanced.app/patches')).content).decode('utf-8'))
    patches = []

    for item in r:
        compatible_packages = item['compatiblePackages']
        for package in compatible_packages:
            if package['name'] == app:
                name = item['name']
                patches.append(name)
    return patches

def getversion(app: str = 'com.google.android.youtube'):
    r = loads(((get('https://releases.revanced.app/patches')).content).decode('utf-8'))

    for item in r:
        compatible_packages = item['compatiblePackages']
        for package in compatible_packages:
            if package['name'] == app:
                return(max(package['versions'], key=lambda x: tuple(map(int, x.split('.')))))

def getpackage(app: str = 'com.google.android.youtube'):
    r = loads(((get('https://releases.revanced.app/patches')).content).decode('utf-8'))
    patches = []

    for item in r:
        compatible_packages = item['compatiblePackages']
        for package in compatible_packages:
            if package['name'] == app:
                patches.append(item)
    return patches

# Does it only once, minimize excessive API usage.
patches = getpatches()
package_patches = getpackage()
tools = gettools()

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.device_id = ''
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Create the QListWidget
        self.list_widget = QListWidget()
        for element in patches:
            item = QListWidgetItem(element)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.list_widget.addItem(item)
        layout.addWidget(self.list_widget)

        # Automatically check patches with excluded set to false
        for index in range(self.list_widget.count()):
            item = self.list_widget.item(index)
            if package_patches[index]['excluded'] == False:
                item.setCheckState(Qt.Checked)

        # Create the "Deploy" button
        self.deploy_button = QPushButton("Deploy")
        self.deploy_button.clicked.connect(self.handle_deploy_button)
        layout.addWidget(self.deploy_button)

        # Create the "Disable version check" checkbox
        self.version_check_checkbox = QCheckBox("Disable version check")
        layout.addWidget(self.version_check_checkbox)

        # Create the "Build" button
        self.build_button = QPushButton("Build")
        self.build_button.clicked.connect(self.handle_build_button)
        layout.addWidget(self.build_button)

        self.setLayout(layout)
        self.setWindowTitle("RVP RELOADED v1.0-EA")
        self.show()


    def download(self, url, filename, name):
        progress_callback=None
        self.progress_dialog = QProgressDialog(f"Downloading {name}...", "Cancel", 0, 100)
        self.progress_dialog.setWindowTitle(f"Downloading {name}...")
        self.progress_dialog.setWindowModality(Qt.WindowModal)
        self.progress_dialog.setAutoClose(True)
        self.progress_dialog.setAutoReset(True)
        self.progress_dialog.setMinimumDuration(0)
        self.progress_dialog.show()
        self.progress_dialog.setValue(0)
        # Set HTTPAdapter options.
        adapter = HTTPAdapter(max_retries=3,
                              pool_connections=20,
                              pool_maxsize=10)
        # Fake the User-Agent so ApkMirror lets us download files without a headless browser.
        headers = {'Accept-Encoding': 'gzip, deflate',
                   'User-Agent': 'Mozilla/5.0',
                   'cache_control': 'max-age=600',
                   'connection': 'keep-alive'}
        # Session so it's possible to use the same session for multiple downloads.
        session = Session()
        # Mount the adapter to the request.
        session.mount('https://', adapter)
        # Get the file with predefined headers and stream=True to get the file size.
        response = session.get(url,
                            allow_redirects=True,
                            stream=True,
                            headers=headers)

        total_size = int(response.headers.get('content-length', 0))

        with open(filename, 'wb') as file:
            downloaded_size = 0
            chunk_size = 256
            for data in response.iter_content(chunk_size=chunk_size):
                file.write(data)
                downloaded_size += len(data)
                percent = int(downloaded_size * 100 / total_size)
                if progress_callback:
                    progress_callback(downloaded_size, chunk_size, total_size)
                if self.progress_dialog:
                    self.progress_dialog.setValue(percent)
                    QCoreApplication.processEvents()  # Update the GUI
        self.progress_dialog.close()

    def download_progress(self, block_num, block_size, total_size):
        percent = int(block_num * block_size * 100 / total_size)
        self.progress_dialog.setValue(percent)
        QCoreApplication.processEvents()  # Update the GUI

    def handle_deploy_button(self):
        # Open another window to display the list
        self.deploy_window = QWidget()
        deploy_layout = QVBoxLayout()

        # Create the QListWidget
        self.deploy_list_widget = QListWidget()
        deploy_layout.addWidget(self.deploy_list_widget)

        # Check if the platform-tools exists. If not, download it.
        if not isdir('platform-tools'):
            # Start the download
            self.download('https://dl.google.com/android/repository/platform-tools_r34.0.3-windows.zip', 'ADB-r34.zip', "ADB")

            # Begin the extraction process
            with ZipFile('ADB-r34.zip', 'r') as zip_ref:
                zip_ref.extractall('')
            remove('ADB-r34.zip')

        self.deploy_list_widget.addItems(getdeviceid())

        # Create the "Choose" button
        choose_button = QPushButton("Choose")
        choose_button.clicked.connect(lambda: self.handle_choose_button(self.deploy_list_widget))
        deploy_layout.addWidget(choose_button)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(lambda: self.deploy_window.close())
        deploy_layout.addWidget(cancel_button)

        self.deploy_window.setLayout(deploy_layout)
        self.deploy_window.setWindowTitle("Deployment")
        self.deploy_window.show()

    def handle_choose_button(self, deploy_list_widget):
        selected_items = [deploy_list_widget.item(index).text()
                          for index in range(deploy_list_widget.count())
                          if deploy_list_widget.item(index).isSelected()]
        if selected_items:
            self.device_id = selected_items[0]  # Set the selected device ID
        print("DEBUG: Selected device ID:", self.device_id)

        # Close the deployment window
        self.deploy_window.close()

    def handle_build_button(self):
        self.hide()

        # Prompt the user to choose the output APK name
        output_apk_name, ok = QInputDialog.getText(self, 'APK Name', 'Enter the output APK name:')
        package_name, ok = QInputDialog.getText(self, 'Change the app name', 'YouTube app package name\nleave for default:')
        
        if output_apk_name == '':
            output_apk_name = 'revanced.apk'
        if ok:
            # Continue with the build process
            if not isfile('prepatched.apk'):
                # Try and check if Chromium's ChromeDriver is downloaded.
                # If it's not, download it and set up WebDriver.
                if isfile('chromedriver.exe') == False:
                    self.download(r'https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Win%2F722276%2Fchromedriver_win32.zip?generation=1575590357764683&alt=media', 'chromedriver.zip', "Chromium ChromeDriver")
                    with ZipFile('chromedriver.zip', 'r') as zip_ref:
                        zip_ref.extractall('')
                    remove('chromedriver.zip')
                    move('chromedriver_win32\chromedriver.exe', 'chromedriver.exe')
                    rmdir('chromedriver_win32')
                
                # Try and check if Chromium 80 (2nd browser with devtools and DAWN API) is downloaded.
                if not isdir('chrome-win'):
                    if not isfile('chrome-win.zip'):
                        self.download(r'https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Win%2F722276%2Fchrome-win.zip?generation=1575590351685488&alt=media', 'chrome-win.zip', 'Chromium Browser')
                    with ZipFile('chrome-win.zip', 'r') as zip_ref:
                        zip_ref.extractall('')
                    remove('chrome-win.zip')
                opts = Options()
                opts.binary_location = 'chrome-win/chrome.exe'
                browser = webdriver.Chrome(service=Service("chromedriver.exe"), options=opts)

                # Fetch and download the YouTube APK.
                version_itemized = str(getversion()).replace('.', '-')
                browser.get(f'https://www.apkmirror.com/apk/google-inc/youtube/youtube-{version_itemized}-release/youtube-{version_itemized}-android-apk-download/')
                sleep(2)
                browser.find_element(By.CLASS_NAME, 'fc-button-label').click()
                dlurl = (browser.find_element(By.CLASS_NAME, 'downloadButton').get_attribute("href"))
                browser.get(dlurl)
                ytdlurl = ((browser.find_element(By.XPATH, '//a[contains(@href, "/wp-content/themes/APKMirror")]')).get_attribute('href'))
                browser.quit()
            
                self.download(ytdlurl, 'prepatched.apk', 'YouTube APK')

            # Download CLI, Integrations, Patches.
            tools = gettools()
            for i in tools:
                if isfile(i[1]) == False:
                    if 'revanced-cli-' in i[1]:
                        try:
                            if str((glob('revanced-cli-*.jar'))[0]) != i[1]:
                                remove(str((glob('revanced-cli-*.jar'))[0]))
                        except IndexError:
                            pass

                    if 'revanced-patches-' in i[1]:
                        try:
                            if str((glob('revanced-patches-*.jar'))[0]) != i[1]:
                                remove(str((glob('revanced-patches-*.jar'))[0]))
                        except IndexError:
                            pass
                        
                    if 'revanced-integrations-' in i[1]:
                        try:
                            if str((glob('revanced-integrations-*.apk'))[0]) != i[1]:
                                remove(str((glob('revanced-integrations-*.apk'))[0]))
                        except IndexError:
                            pass

                    self.download(i[0], i[1], i[1])

            selected_items = [self.list_widget.item(index).text()
                            for index in range(self.list_widget.count())
                            if self.list_widget.item(index).checkState() == Qt.Checked]
            excluded_items = []
            for item in patches:
                if item not in selected_items:
                    excluded_items.append(item)

            data = [
    {
        "patchName": "custom-branding",
        "options": [
            {
                "key": "appName",
                "value": "YouTube ReVanced"
            },
            {
                "key": "iconPath",
                "value": None
            }
        ]
    },
]

            # Modify the values
            if package_name != '':
                data[0]["options"][0]["value"] = package_name

            # Write the modified JSON to a file
            with open("options.json", "w") as file:
                dump(data, file, indent=4)
            def expcheck():
                if self.version_check_checkbox.checkState() == Qt.Checked:
                    return(' --experimental')
            cmd = f'java -jar {str((glob("revanced-cli-*.jar"))[0])} --exclusive -a prepatched.apk -b {str((glob("revanced-patches-*.jar"))[0])} -m {str((glob("revanced-integrations-*.apk"))[0])} -o {output_apk_name}{expcheck()}'

            for i in selected_items:
                cmd = cmd + f' -i {i}'

            if self.device_id != '':
                cmd = cmd + f' -d {self.device_id}'

            print(cmd)
            z = Popen(["cmd", "/c", cmd], creationflags=CREATE_NEW_CONSOLE)
            
            while True:
                for process in process_iter(['name']):
                    if process.info['name'] == process_name:
                        return True
                return False

if __name__ == '__main__':
    try:
        app = QApplication(argv)
        window = MyApp()
        exit(app.exec_())
    except KeyboardInterrupt:
        exit()
