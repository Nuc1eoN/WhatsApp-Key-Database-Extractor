# Auto Requirements installer.
import os
try:
    import packaging
    import termcolor
    import wget
except ImportError:
    print('First run : Auto installing requirements.')
    try:
        # Trying both methods of installations
        os.system('pip install --upgrade termcolor wget packaging')
    except:
        os.system('python -m pip install --upgrade termcolor wget packaging')

import helpers.ADBDeviceSerialId as deviceId
import subprocess
from helpers.CustomCI import CustomInput, CustomPrint
from view_extract import ExtractAB
from helpers.Termux import TermuxMode
import re

appURLWhatsAppCDN = 'https://www.cdn.whatsapp.net/android/2.11.431/WhatsApp.apk'
appURLWhatsCryptCDN = 'https://whatcrypt.com/WhatsApp-2.11.431.apk'
isJAVAInstalled = False


def main():
    os.system('clear')
    CheckBin()
    ShowBanner()
    global isJAVAInstalled
    #isJAVAInstalled = CheckJAVA()
    CustomPrint('Temporarily continuing without Java.')
    USBMode()


def BackupWhatsAppApk(SDKVersion, versionName, WhatsAppapkPath):
    os.system(adb + ' shell am force-stop com.whatsapp') if(SDKVersion >
                                                            11) else os.system(adb + ' shell am kill com.whatsapp')
    CustomPrint('Backing up WhatsApp ' + versionName +
                ' apk, the one installed on device to ' + tmp + 'WhatsAppbackup.apk')
    os.system(adb + ' pull ' + WhatsAppapkPath +
              ' ' + tmp + 'WhatsAppbackup.apk')
    CustomPrint('Apk backup complete.')


def BackupWhatsAppDataasAb(SDKVersion):
    CustomPrint('Backing up WhatsApp data as ' + tmp +
                'whatsapp.ab. May take time, don\'t panic.')
    try:
        os.system(adb + ' backup -f ' + tmp + 'whatsapp.ab com.whatsapp') if(SDKVersion >=
                                                                             23) else os.system(adb + ' backup -f ' + tmp + 'whatsapp.ab -noapk com.whatsapp')
    except Exception as e:
        CustomPrint(e)
    CustomPrint('Done backing up data.')


def CheckBin():
    if (not os.path.isdir('bin')):
        CustomPrint('I can not find bin folder, check again...', 'green')
        Exit()
    pass


def CheckJAVA():
    JAVAVersion = re.search('(?<=version ")(.*)(?=")', str(subprocess.check_output(
        'java -version'.split(), stderr=subprocess.STDOUT))).group(1)
    isJAVAInstalled = True if(JAVAVersion) else False
    if (isJAVAInstalled):
        CustomPrint('Found Java installed on system. Continuing...')
        return isJAVAInstalled
    else:
        noJAVAContinue = CustomInput(
            'It looks like you don\'t have JAVA installed on your system. Would you like to (C)ontinue with the process and \'view extract\' later? or (S)top? : ', 'green') or 'c'
        if(noJAVAContinue == 'c'):
            CustomPrint(
                'Continuing without JAVA, once JAVA is installed on system run \'view_extract.py\'', 'green')
            return isJAVAInstalled
        else:
            Exit()


def Exit():
    CustomPrint('\nExiting...', 'green')
    os.system('adb kill-server')
    quit()


def InstallLegacy(SDKVersion):
    CustomPrint("installing Legacy WhatsApp V2.11.431, hold tight now.")
    if(SDKVersion >= 17):
        os.system(adb + ' install -r -d ' + helpers + 'LegacyWhatsApp.apk')
    else:
        os.system(adb + ' install -r ' + helpers + 'LegacyWhatsApp.apk')
    CustomPrint('Installation Complete.')


def RealDeal(SDKVersion, WhatsAppapkPath, versionName):
    BackupWhatsAppApk(SDKVersion, versionName, WhatsAppapkPath)
    UninstallWhatsApp(SDKVersion)
    InstallLegacy(SDKVersion)
    BackupWhatsAppDataasAb(SDKVersion)
    ReinstallWhatsApp()
    CustomPrint('Our work with device has finished.')
    # ExtractAB(isJAVAInstalled)
    CustomPrint(
        'Extraction is not possible on termux as of now. I have to back \'whatsapp.ab\' up in \'extracted\' folder.')
    userName = CustomInput(
        'Enter a reference name for this user (Remeber this name for later). : ') or 'user'
    os.mkdir(extracted + userName) if not (os.path.isdir(extracted +
                                                         userName)) else CustomPrint('Folder already exists.')
    # copy from to here.
    os.system('mv ' + tmp + 'whatsapp.ab ' +
              extracted + userName + '/whatsapp.ab')
    CustomPrint(
        'Done copying, deleting from \'tmp\' folder. Now run \'view_extract.py\' from computer.')
    os.system('rm -rf ' + tmp + 'whatsapp.ab')


def ReinstallWhatsApp():
    CustomPrint('Reinstallting original WhatsApp.')
    try:
        os.system(adb + ' install -r -d ' + tmp + 'WhatsAppbackup.apk')
    except Exception as e:
        print(e)
        CustomPrint('Could not install WhatsApp, install by running \'restore_whatsapp.py\' or manually installing from Play Store.\nHowever if it crashes then you have to clear storage/clear data from settings => app settings => WhatsApp.')


def ShowBanner():
    banner_path = 'non_essentials/banner.txt'
    try:
        banner = open(banner_path, 'r')
        banner_content = banner.read()
        CustomPrint(banner_content, 'green', ['bold'])
        banner.close()
    except Exception as e:
        CustomPrint(e)
    CustomPrint('WhatsApp Key/DB Extrator on non-rooted Android\n',
                'green', ['bold'])
    intro_path = 'non_essentials/intro.txt'
    try:
        intro = open(intro_path, 'r')
        intro_content = intro.read()
        CustomPrint(intro_content, 'green', ['bold'])
        intro.close()
    except Exception as e:
        CustomPrint(e)


def UninstallWhatsApp(SDKVersion):
    if(SDKVersion >= 23):
        try:
            CustomPrint('Uninstalling WhatsApp, skipping data.')
            os.system(adb + ' shell pm uninstall -k com.whatsapp')
            CustomPrint('Uninstalled.')
        except Exception as e:
            CustomPrint('Could not uninstall WhatsApp.')
            CustomPrint(e)
            Exit()


def USBMode():
    ACReturnCode, SDKVersion, WhatsAppapkPath, versionName, sdPath = TermuxMode(
        adb)
    RealDeal(SDKVersion, WhatsAppapkPath,
             versionName) if ACReturnCode == 1 else Exit()


if __name__ == "__main__":

    ADBSerialId = deviceId.init()

    # Global command line helpers
    adb = 'adb -s ' + ADBSerialId
    delete = 'rm -rf'
    tmp = 'tmp/'
    confirmDelete = ''
    grep = 'grep'
    curl = 'curl'
    helpers = 'helpers/'
    extracted = 'extracted/'

    main()
