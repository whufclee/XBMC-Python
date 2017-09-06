# -*- coding: utf-8 -*-

# script.openwindow
# Startup Wizard (c) by whufclee (info@totalrevolution.tv)

# Total Revolution Startup Wizard is licensed under a
# Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.

# You should have received a copy of the license along with this
# work. If not, see http://creativecommons.org/licenses/by-nc-nd/4.0.

import os
import re
import sys
import xbmc

from koding import *

ADDON_ID            = 'plugin.program.tbs'
ADDONS              = xbmc.translatePath('special://home/addons')
ADDON_DATA          = xbmc.translatePath('special://profile/addon_data')
USERDATA            = xbmc.translatePath('special://home/userdata')
APK_FILES           = os.path.join(USERDATA,'APK_FILES')
TBS_DATA            = os.path.join(ADDON_DATA,ADDON_ID)
BASE                = Addon_Setting(setting='base')
DEBUG               = Addon_Setting(setting='debug')

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
            choice = YesNo_Dialog(String(30166)%(counter,array_len),String(30167),'[COLOR=dodgerblue]%s[/COLOR]'%clean_apk,String(30165),yeslabel=String(30170), nolabel=String(30169))
            if not choice:
                xbmc.executebuiltin('StartAndroidActivity("","android.intent.action.VIEW","application/vnd.android.package-archive","file:%s")' % APK)
        if counter == array_len:
            OK_Dialog('ANDROID APPS COMPLETE','No more Android apps to install','Please press OK to continue.')
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
#-----------------------------------------------------------------------------
# Return the CPU details
def CPU_Check():
    logtext     = Grab_Log()
    CPUmatch    = re.compile('Host CPU: (.+?) available').findall(logtext)
    CPU         = CPUmatch[0] if (len(CPUmatch) > 0) else ''
    return CPU.replace(' ','%20')
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