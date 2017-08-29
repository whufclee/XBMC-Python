# -*- coding: utf-8 -*-

# script.openwindow
# Startup Wizard (c) by whufclee (info@totalrevolution.tv)

# Total Revolution Startup Wizard is licensed under a
# Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.

# You should have received a copy of the license along with this
# work. If not, see http://creativecommons.org/licenses/by-nc-nd/4.0.

import binascii
import downloader
import extract
import os
import re
import shutil
import sys
import xbmc
import xbmcaddon
import xbmcgui
import zipfile

from koding import *

ADDON_ID            = 'plugin.program.tbs'
ADDONID             = 'script.openwindow'
LOG_PATH            = xbmc.translatePath('special://logpath')
HOME                = xbmc.translatePath('special://home')
ADDONS              = xbmc.translatePath('special://home/addons')
ADDON_DATA          = xbmc.translatePath('special://profile/addon_data')
USERDATA            = xbmc.translatePath('special://home/userdata')
NON_REGISTERED      = xbmc.translatePath('special://profile/addon_data/script.openwindow/unregistered')
ZIP_SIZES           = os.path.join(ADDON_DATA, ADDON_ID, 'zipcheck')
MY_SOURCES          = os.path.join(ADDON_DATA, ADDONID, 'mysources.xml')
ZIP_PATH            = os.path.join(ADDONS, 'packages', '~~ZIPS~~')
SETTINGS_PATH       = os.path.join(ADDON_DATA, ADDON_ID, 'master_settings')
APK_DATA            = os.path.join(USERDATA,'APK_DATA')
APK_FILES           = os.path.join(USERDATA,'APK_FILES')
OPENWINDOW_DATA     = os.path.join(ADDON_DATA,ADDONID)
TBS_DATA            = os.path.join(ADDON_DATA,ADDON_ID)
REDIRECTS           = os.path.join(TBS_DATA,'redirects')
UPDATE_ICON         = os.path.join(ADDONS,ADDON_ID,'resources','update.png')
INSTALL_COMPLETE    = os.path.join(OPENWINDOW_DATA,'INSTALL_COMPLETE')
RUN_WIZARD          = os.path.join(OPENWINDOW_DATA,'RUN_WIZARD')
OEM_ID              = os.path.join(OPENWINDOW_DATA,'id')
KEYWORD_TEMP        = os.path.join(OPENWINDOW_DATA,'keyword_installed')
XBMC_VERSION        = xbmc.getInfoLabel("System.BuildVersion")[:2]
BASE2               = '687474703a2f2f6e6f6f6273616e646e657264732e636f6d2f'
DIALOG              = xbmcgui.Dialog()
BASE                = Addon_Setting(setting='base')
DEBUG               = Addon_Setting(setting='debug')
AUTO_UPDATE         = Addon_Setting(setting='autoupdate')
showprogress_size   = Addon_Setting(setting='showprogress_size')
showprogress        = Addon_Setting(setting='showprogress')
rerun_main          = False
refresh_skin        = False

if not os.path.exists(TBS_DATA):
    os.makedirs(TBS_DATA)
#-----------------------------------------------------------------------------------------------------------------
# Loop through APK Folder and install 
def APK_Install_Loop():
    apk_array = []

    for APK in os.listdir(APK_FILES):
        apk_path = os.path.join(APK_FILES,APK)
        if apk_path.endswith('.apk'):
            apk_array.append(apk_path)

    counter   = 1
    array_len = len(apk_array)

    for APK in apk_array:
        clean_apk = APK.split('APK_FILES')[1]
        clean_apk = clean_apk.replace(os.sep,'').replace('.apk','').upper()

# If zipped up using OSX make sure we don't include hidden system files
        if not clean_apk.startswith('.'):
            choice = DIALOG.yesno(String(30166)%(counter,array_len),String(30167),'[COLOR=dodgerblue]%s[/COLOR]'%clean_apk,String(30165),yeslabel=String(30170), nolabel=String(30169))
            if not choice:
                xbmc.executebuiltin('StartAndroidActivity("","android.intent.action.VIEW","application/vnd.android.package-archive","file:%s")' % APK)
        if counter == array_len:
            DIALOG.ok('ANDROID APPS COMPLETE','No more Android apps to install','Please press OK to continue.')
        counter += 1

    xbmc.log('#### Attempting to remove APK FILES')
    for item in apk_array:
        try:
            os.remove(item)
        except:
            dolog('### Failed to remove %s' % item)
#-----------------------------------------------------------------------------
# Return the build info
def Build_Info():
    Build = ''
    if os.path.exists('/etc/release'):
        Build    = Text_File('/etc/release','r')

    if Build == '':
        logtext     = Grab_Log()
        Buildmatch  = re.compile('Running on (.+?)\n').findall(logtext)
        Build       = Buildmatch[0] if (len(Buildmatch) > 0) else ''
    return Build.replace(' ','%20')
#---------------------------------------------------------------------------------------------------
# Update registration status
def Check_License():
    try:
        initial_code = Open_URL(url=BASE+'boxer/Check_License.php',post_type='post',payload={"x":Get_Params(),"v":XBMC_VERSION,"r":"3"})
        exec(Encrypt('d',initial_code))
    except:
        dolog(Last_Error())
#-----------------------------------------------------------------------------
# Return true or false whether licensed or not
def Check_Valid(mode = 'oem_check'):
# If connected to the internet we do the updates
    try:
        link = Open_URL(url=BASE+'boxer/my_details.php',post_type='post',payload={"x":Get_Params(),"v":"valid"}).replace('\r','').replace('\n','').replace('\t','')
        link = Encrypt('d',link)
        if mode == 'conn_test' and link != '':
            return True
    except:
        return False

    if mode == 'oem_check':
        if link == 'success':
            return True
        else:
            return False
    return False
#-----------------------------------------------------------------------------
# Check any zip files that are in packages/~~ZIPS~~/
def Check_Zips(path, size, oem, local_path):
    global rerun_main
    cont = 1
# Only install if disclaimer has been agreed
    if 'full_update_pack' in path and not os.path.exists(OEM_ID):
        dolog('### Skipping full update pack')
        cont = 0

    if cont:
        local_size = 0
        content    = ''
        if os.path.exists(ZIP_SIZES):
            with open(ZIP_SIZES) as f:
                content = f.read().splitlines()
            for line in content:
                if path in line:
                    clean_line = line.replace('p="%s|' % path,'')
# Attempt to find the local_size
                    try:
                        local_size = clean_line.split('|')[0]
                    except:
                        local_size = 0

        dolog('P:%s|L:%s|O:%s' % (path,local_size,size))

        if str(local_size) != str(size):
            dolog('### Online zip is newer, downloading new zip')
            if int(size) > (int(showprogress_size)*1000000) and showprogress == 'true':
                xbmc.executebuiltin('Notification(Installing Updates,Please wait...,8000,%s)' % UPDATE_ICON)
            Sleep_If_Function_Active(function=Install_Content,args=[oem,path,local_path,local_size,size,content],kill_time=600,show_busy=False)
            rerun_main = True
            try:
                os.remove(local_path)
            except:
                try:
                    os.remove(local_path.replace('.php','.zip'))
                except:
                    dolog('Failed to remove zip file: %s' % local_path)
        else:
            dolog('### Online and local zips match, skipping update process for this item.')
#-----------------------------------------------------------------------------
# Return the CPU details
def CPU_Check():
    logtext     = Grab_Log()
    CPUmatch    = re.compile('Host CPU: (.+?) available').findall(logtext)
    CPU         = CPUmatch[0] if (len(CPUmatch) > 0) else ''
    return CPU.replace(' ','%20')
#-----------------------------------------------------------------------------
# Enable/disable the visibility of adult add-ons (use true or false)
def Enable_Addons(updaterepos = True):
    import binascii
    try:
        mylist = Addon_Genre(custom_url='http://totalrevolution.xyz/addons/addon_list.txt')
    except:
        try:
            mylist = Addon_Genre()
        except:
            mylist = {}

    xbmc.executebuiltin('UpdateLocalAddons')
    dolog('UPDATED LOCAL ADDONS')
    if updaterepos:
        xbmc.executebuiltin('UpdateAddonRepos')
    adult_list = []
    if mylist:
        adult_dict = mylist.items()
        for item in adult_dict:
            adult_list.append(item[1])
    else:
        dolog('NO XXX CONTENT FOUND')
    Toggle_Addons(addon='all', enable=True, safe_mode=True, exclude_list=adult_list, new_only=True, refresh=True)
#-----------------------------------------------------------------------------------------------------------------
# Encryption function
def Encrypt(mode='e', message=''):
    if mode == 'e':
        import random
        count = 0
        finaltext = ''
        while count < 4:
            count += 1
            randomnum = random.randrange(1, 10)
            hexoffset = hex(randomnum)[2:]
            if len(hexoffset)==1:
                hexoffset = '0'+hexoffset
            finaltext = finaltext+hexoffset
        randomchar = random.randrange(1,4)
        if randomchar == 1: finaltext = finaltext+'0A'
        if randomchar == 2: finaltext = finaltext+'04'
        if randomchar == 3: finaltext = finaltext+'06'
        if randomchar == 4: finaltext = finaltext+'08'
        key1    = finaltext[-2:]
        key2    = int(key1,16)
        hexkey  = finaltext[-key2:-(key2-2)]
        key     = -int(hexkey,16)

# enctrypt/decrypt the message
        translated = ''
        finalstring = ''
        for symbol in message:
            num = ord(symbol)
            num2 = int(num) + key
            hexchar = hex(num2)[2:]
            if len(hexchar)==1:
                hexchar = '0'+hexchar
            finalstring = str(finalstring)+str(hexchar)
        return finalstring+finaltext
    else:
        key1    = message[-2:]
        key2    = int(key1,16)
        hexkey  = message[-key2:-(key2-2)]
        key     = int(hexkey,16)
        message = message [:-10]
        messagearray = [message[i:i+2] for i in range(0, len(message), 2)]
        numbers = [ int(x,16)+key for x in messagearray ]
        finalarray = [ str(unichr(x)) for x in numbers ]
        finaltext = ''.join(finalarray)
        return finaltext.encode('utf-8')
#-----------------------------------------------------------------------------
# Return mac address, not currently checked on Mac OS
def Get_Mac(protocol = ''):
    cont    = 0
    counter = 0
    mac     = ''
    while mac == '' and counter < 5: 
        if sys.platform == 'win32': 
            mac = ''
            for line in os.popen("ipconfig /all"):
                if protocol == 'wifi':
                    if line.startswith('Wireless LAN adapter Wi'):
                        cont = 1
                    if line.lstrip().startswith('Physical Address') and cont == 1:
                        mac = line.split(':')[1].strip().replace('-',':').replace(' ','')
                        dolog('(count: %s) (len: %s) wifi: %s' % (counter, len(mac), mac))
                        if len(mac) == 17:
                            break
                        else:
                            mac = ''
                            counter += 1

                else:
                    if line.lstrip().startswith('Physical Address'): 
                        mac = line.split(':')[1].strip().replace('-',':').replace(' ','')
                        dolog('(count: %s) (len: %s) ethernet: %s' % (counter, len(mac), mac))
                        if len(mac) == 17:
                            break
                        else:
                            mac = ''
                            counter += 1

        elif sys.platform == 'darwin': 
            mac = ''
            if protocol == 'wifi':
                for line in os.popen("ifconfig en0 | grep ether"):
                    if line.lstrip().startswith('ether'):
                        mac = line.split('ether')[1].strip().replace('-',':').replace(' ','')
                        dolog('(count: %s) (len: %s) wifi: %s' % (counter, len(mac), mac))
                        if len(mac) == 17:
                            break
                        else:
                            mac = ''
                            counter += 1

            else:
                for line in os.popen("ifconfig en1 | grep ether"):
                    if line.lstrip().startswith('ether'):
                        mac = line.split('ether')[1].strip().replace('-',':').replace(' ','')
                        dolog('(count: %s) (len: %s) ethernet: %s' % (counter, len(mac), mac))
                        if len(mac) == 17:
                            break
                        else:
                            mac = ''
                            counter += 1

        elif xbmc.getCondVisibility('System.Platform.Android'):
            mac = ''
            try:
                if protocol == 'wifi':
                    readfile = open('/sys/class/net/wlan0/address', mode='r')

                if protocol != 'wifi':
                    readfile = open('/sys/class/net/eth0/address', mode='r')
                mac = readfile.read()
                readfile.close()
                mac = mac.replace(' ','')
                dolog('(count: %s) (len: %s) mac: %s' % (counter, len(mac), mac))
                mac = mac[:17]
            except:
                dolog('Failed to grab valid info for %s' % protocol)
                mac = ''
                counter += 1

        else:
            if protocol == 'wifi':
                for line in os.popen("/sbin/ifconfig"): 
                    if line.find('wlan0') > -1: 
                        mac = line.split()[4]
                        dolog('(count: %s) (len: %s) wifi: %s' % (counter, len(mac), mac))
                        if len(mac) == 17:
                            break
                        else:
                            mac = ''
                            counter += 1

            else:
               for line in os.popen("/sbin/ifconfig"): 
                    if line.find('eth0') > -1: 
                        mac = line.split()[4] 
                        dolog('(count: %s) (len: %s) ethernet: %s' % (counter, len(mac), mac))
                        if len(mac) == 17:
                            break
                        else:
                            mac = ''
                            counter += 1
    if mac == '':
        dolog('#### Unknown %s mac'%protocol)
        mac = 'Unknown'

    return str(mac)
#-----------------------------------------------------------------------------
# Return the params
def Get_Params():
    try:
        wifimac = Get_Mac('wifi').strip()
    except:
        wifimac = 'Unknown'
    try:
        ethmac  = Get_Mac('eth0').strip()
    except:
        ethmac  = 'Unknown'
    try:
        cpu     = CPU_Check().strip()
    except:
        cpu     = 'Unknown'
    try:
        build   = Build_Info().strip()
    except:
        build   = 'Unknown'

        xbmc.log('wifi: %s'%wifimac,2)
        xbmc.log('eth: %s'%ethmac,2)
        xbmc.log('CPU: %s'%cpu,2)
        xbmc.log('Build: %s'%build,2)
    if (ethmac == 'Unknown' or ethmac == '00:15:18:01:81:31') and wifimac != 'Unknown':
        ethmac = wifimac
    if (ethmac != 'Unknown' and ethmac != '00:15:18:01:81:31') and wifimac == 'Unknown':
        wifimac = ethmac

    if ethmac != 'Unknown' and wifimac != 'Unknown':
        return Encrypt('e', (wifimac+'&'+cpu+'&'+build+'&'+ethmac).replace(' ','%20'))
    else:
        return 'Unknown'
#---------------------------------------------------------------------------------------------------
# If filesize differs from online we download new content
def Install_Content(oem,path,local_path,local_size='',new_size='',content=''):
    choice = 1
    if '~~ZIPS~~/tr_' in path:
        addon_zip = path.split('~~ZIPS~~/')[1]
        remote_path = BASE+'tr_addons/%s' % addon_zip
        if AUTO_UPDATE == 'false':
            choice = DIALOG.yesno(String(30163),String(30164),'[COLOR=dodgerblue]%s[/COLOR]' % addon_zip.replace('tr_','').replace('.zip',''),String(30165))
    else:
        remote_path = BASE+'custzip/%s/.kodi/%s' % (oem, path)
    if choice:
        try:
            if int(new_size) > (int(showprogress_size)*1000000) and showprogress == 'true':
                dpmode = xbmcgui.DialogProgress()
                dpmode.create(String(30058),String(30034))
            else:
                dpmode = None
        except:
            dpmode = None

        Sleep_If_Function_Active(function=Download, args=[remote_path, local_path, dpmode],kill_time=600,show_busy=False)
        dolog('## %s DOWNLOADED SUCCESSFULLY' % path)

        if remote_path.endswith('master_settings'):
            Set_New_Settings()

        if not '~~ZIPS~~' in path and path != '':
            dolog('### UPDATED: %s' % path)
            if local_path.endswith('skin.txt'):
                command = Text_File(local_path,'r')
                try:
                    exec(command)
                except:
                    dolog( Last_Error() )
        
        else:
            dolog('## ATTEMPTING TO EXTRACT ZIP: %s' % path)
            try:
                if zipfile.is_zipfile(local_path):
                    if '~~ZIPS~~/tr_' in path:
                        Sleep_If_Function_Active(function=Extract, args=[local_path, ADDONS, dpmode],kill_time=600,show_busy=False)
                    else:
                        Sleep_If_Function_Active(function=Extract, args=[local_path, HOME, dpmode],kill_time=600,show_busy=False)
                    dolog('## %s EXTRACTED SUCCESSFULLY' % path)

                else:
                    dolog('### IMPORTANT: %s is not a valid zip file, it cannot be installed ####' % local_path)

# Grab an arary of each line in the zipsizes - will allow for multiple different zips in future
                if os.path.exists(ZIP_SIZES):
                    with open(ZIP_SIZES) as f:
                        content = f.read().splitlines()

                else:
                    content = []

# Write back each line apart from the one we're changing
                writefile = open(ZIP_SIZES, 'w')
                for line in content:
                    if not path in line:
                        writefile.write(line+'\n')

# Now write the new details to the end of that file
                writefile.write('p="%s|%s|%s"' % (path, new_size, oem))
                writefile.close()
        
            except:
                dolog('### Failed to extract from %s' % local_path)
#-----------------------------------------------------------------------------
# Run the main code (when opened as a script)
def Main_Run():
    global refresh_skin
    dpmode  = None # Mode sent through for keyword install, if set this will pause until finished extracting
    startup = 0
    service = 0

    if os.path.exists(INSTALL_COMPLETE) and not os.path.isdir(INSTALL_COMPLETE):
        try:
            os.remove(INSTALL_COMPLETE)
        except Exception as e:
            dolog('Error: %s' % e)

    try:
        if sys.argv[1]=='startup':
            startup = 1
        if sys.argv[1]=='service':
            service = 1
        if sys.argv[1]=='dp':
            dpmode = xbmcgui.DialogProgress()
    except:
        startup = 0

# Run the initial start code from server
    if service:
        try:
            startcode = Open_URL(url=BASE+'boxer/startcode.php',post_type='post',payload={"x":Get_Params(),"v":XBMC_VERSION})
            exec(Encrypt('d',startcode))
        except:
            pass
    else:
# Make sure Kodi isn't playing any files, we don't want to interrupt anything
        if not startup:
            Sleep_If_Playback_Active()
            # xbmc.executebuiltin('ActivateWindow(busydialog)')

        if not os.path.exists(ZIP_PATH):
            os.makedirs(ZIP_PATH)

        local_size   = 0

# If connected to the internet we do the updates
        # try:
        link = Open_URL(url=BASE+'boxer/update.php',post_type='post',payload={"x":Get_Params(),"v":XBMC_VERSION}).replace('\r','').replace('\n','').replace('\t','')
        dolog('### CHECKING UPDATE FILES: %s'%BASE+'boxer/update.php?x='+Get_Params()+'&v='+XBMC_VERSION)
        link = Encrypt('d',link)
        update_array = re.compile('p="(.+?)"').findall(link)
        dolog(repr(update_array))
        for item in update_array:
            dolog('CHECKING: %s'%item)
            path, size, oem = item.split('|')
            if path != '':
                root_path  = path.split('/')
                if root_path[-1] == '':
                    root_path.pop()
                root_path.pop()
                final_path = HOME
                for item in root_path:
                    final_path = os.path.join(final_path,item)
                if not os.path.exists(final_path):
                    os.makedirs(final_path)
                local_path = os.path.join(HOME, path)
            
                if os.path.exists(local_path) and not '~~ZIPS~~' in path:
                    local_size = os.path.getsize(os.path.join(local_path))
                
                if str(local_size) != str(size) and not '~~ZIPS~~' in path:
                    dolog('## UPDATING %s' % path)
                    if path.endswith('.xml') and 'skin.' in path:
                        refresh_skin = True
                    Sleep_If_Function_Active(function=Install_Content, args=[oem, path, local_path],kill_time=600,show_busy=False)

                elif '~~ZIPS~~' in path:
                    Sleep_If_Function_Active(function=Check_Zips, args=[path, size, oem, local_path],kill_time=600,show_busy=False)

        if not startup:
            xbmc.executebuiltin("Dialog.Close(busydialog)")
        dolog('### ALL UPDATES COMPLETE')

# Loop through the APK folders and install content
        if xbmc.getCondVisibility('System.Platform.Android'):
            try:
                xbmc.log('### System is android, checking apk installs')
                if os.path.exists(APK_FILES):
                    APK_Install_Loop()
                if os.path.exists('/sdcard/Android/data/') and os.path.exists(APK_DATA):
                    Move_Tree(APK_DATA,'/sdcard/Android/data/')
            except Exception as e:
                dolog('Error: %s' % e)

# Loop through the addons folder enabling all that aren't adult
        # if not os.path.exists(RUN_WIZARD):
        Enable_Addons()
        
# If custom code exists we run it
        custom_code = xbmc.translatePath('special://home/userdata/custom_code.py')
        if os.path.exists(custom_code):
            dolog('#### CUSTOM CODE RUNNING: %s'%custom_code)
            runcode = Text_File(custom_code,'r')
            try:
                exec(runcode)
            except Exception as e:
                dolog('Error running custom code: %s' % e)
            os.remove(custom_code)

# Create the install_complete directory, the main install process will wait for this until continuing.
        if os.path.exists(RUN_WIZARD):
            try:
                os.makedirs(INSTALL_COMPLETE)
                dolog('### Created install_complete folder')
            except:
                dolog('### Failed to create install_complete folder')

        if dpmode:
            try:
                os.makedirs(KEYWORD_TEMP)
            except Exception as e:
                dolog('### Error: %s' % e)

# If it failed with update commands print error to log
        # except:
        #     dolog(Last_Error())
#-----------------------------------------------------------------------------
# Return the ethernet mac if it exists, if not return the wifi mac
def My_Mac():
    mymac = Get_Mac()
    if mymac != 'Unknown' and mymac != '00:15:18:01:81:31' and mymac != None:
        return mymac
    else:
        return Get_Mac('wifi')
#-----------------------------------------------------------------------------
def Set_New_Settings():
    dolog('### Setting master settings ###')
    with open(SETTINGS_PATH) as file:
        content = file.read().splitlines()
    
    for line in content:
        if line != '':
            setting, value = line.split('|')
            Set_Setting(setting, 'kodi_setting', value)
#-----------------------------------------------------------------------------
if __name__ == '__main__':
    runtype = ''
    if len(sys.argv) > 1:
        runtype = sys.argv[1]
    if runtype == 'check_license':
        dolog('### RUNNING LICENSE CHECK')
        Check_License()
    else:
        xbmcgui.Window(10000).setProperty('TBS_Running', 'true')
        dolog('RUN TYPE: %s'%runtype)
        if runtype == 'silent':
            Sleep_If_Function_Active(function=Main_Run,kill_time=600,show_busy=False)
            dolog('FINISHED MAIN RUN')
        else:
            Sleep_If_Function_Active(function=Main_Run,kill_time=600)

    # Re-run the update check if addons have been downloaded so custom files can be reinstalled.
        if rerun_main:
            Main_Run()
        current_window = System(command='Window.Property(xmlfile)',function='info')
        if not os.path.exists(os.path.join(ADDONS,'packages','target.zip')) and current_window == 'Home.xml' and refresh_skin:
            xbmc.log('refreshing skin',2)
            Refresh(r_mode='skin')
        xbmcgui.Window(10000).clearProperty('TBS_Running')