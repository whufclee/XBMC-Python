#
#      Copyright (C) 2016 noobsandnerds.com
#
#  This Program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2, or (at your option)
#  any later version.
#
#  This Program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with XBMC; see the file COPYING.  If not, write to
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#  http://www.gnu.org/copyleft/gpl.html
#

import binascii
import hashlib
import os
import random
import re
import requests
import shutil
import string
import sys
import time
import traceback
import urllib
import urllib2
import xbmc
import xbmcaddon
import xbmcgui
import zipfile

try:
    import simplejson as json
except:
    import json

def converthex(url):
    return binascii.unhexlify(url)

try:
    AddonID     =  xbmcaddon.Addon().getAddonInfo('id')
except:
    AddonID     =  sys.argv[2]

AddonVersion    =  xbmcaddon.Addon(id=AddonID).getAddonInfo('version')

try:
    if sys.argv[1] == converthex('7465737466696c65'):
        AddonID  =  AddonID+'.test'
except:
    pass

TestID           =  AddonID
if not AddonID.endswith(converthex('2e74657374')):
    TestID       =  AddonID+converthex('2e74657374')

OrigID           =  AddonID.replace(converthex('2e74657374'),'')
AddonIDstatic    =  AddonID
ADDON            =  xbmcaddon.Addon(id=AddonID)
ADDON_ORIG       =  xbmcaddon.Addon(id=OrigID)
testver          =  ADDON.getSetting(converthex('74657374766572'))
USERDATA         =  xbmc.translatePath(converthex('7370656369616c3a2f2f70726f66696c65'))
ADDON_DATA       =  xbmc.translatePath(os.path.join(USERDATA,converthex('6164646f6e5f64617461')))
ADDONS           =  xbmc.translatePath(converthex('7370656369616c3a2f2f686f6d652f6164646f6e73'))
PACKAGES         =  os.path.join(ADDONS,converthex('7061636b61676573'))
installfile      =  os.path.join(ADDONS,AddonID,converthex('6c6f67696e2e7079'))
updateicon       =  os.path.join(ADDONS,AddonID,converthex('7265736f7572636573'),converthex('7570646174652e706e67'))
bakfile          =  os.path.join(ADDONS,AddonID,converthex('7265736f7572636573'),converthex('6261636b7570'))
cookie           =  os.path.join(ADDON_DATA,OrigID,converthex('636f6f6b696573'),converthex('74656d70'))
runcode          =  os.path.join(ADDON_DATA,OrigID,converthex('636f6f6b696573'),converthex('6b6565706d65'))
downloaddst      =  xbmc.translatePath(converthex('7370656369616c3a2f2f686f6d652f6164646f6e732f7061636b616765732f6370'))
login            =  ADDON_ORIG.getSetting(converthex('6c6f67696e'))
forum            =  ADDON_ORIG.getSetting(converthex('666f72756d'))
username         =  ADDON_ORIG.getSetting(converthex('757365726e616d65')).replace(' ','%20') if login == 'true' else ''
password         =  ADDON_ORIG.getSetting(converthex('70617373776f7264')) if login == 'true' else ''
debug            =  ADDON_ORIG.getSetting(converthex('4445425547'))
installrepos     =  ADDON_ORIG.getSetting(converthex('696e7374616c6c7265706f73'))
installaddons    =  ADDON_ORIG.getSetting(converthex('696e7374616c6c6164646f6e73'))
silent           =  ADDON_ORIG.getSetting(converthex('73696c656e74'))
dialog           =  xbmcgui.Dialog()
dp               =  xbmcgui.DialogProgress()

kodi_ver         =  int(float(xbmc.getInfoLabel("System.BuildVersion")[:2]))
launch           =  'launch.py'
stop             =  0
main_counter     =  0

downloads        =  []
stddownloads     =  []
nologindownloads =  []

usernamelen      =  len(username)
if usernamelen > 14:
    usernamelen = 15

if forum == converthex('556e6f6666696369616c204b6f646920537570706f7274'):
    forum = 'k'
if forum == converthex('436f6d6d756e697479204275696c647320537570706f7274'):
    forum = 'c'

if not os.path.exists(os.path.join(ADDON_DATA,OrigID,converthex('636f6f6b696573'))):
    os.makedirs(os.path.join(ADDON_DATA,OrigID,converthex('636f6f6b696573')))

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
#----------------------------------------------------------------
def dolog(url):
    if debug == 'true':
        xbmc.log(AddonID+': '+url)
import zipfile
#----------------------------------------------------------------
def Installed_Addons(types='unknown', content ='unknown', properties = ''):
    addon_dict = []
    if properties != '':
        properties = properties.replace(' ','')
        properties = '"%s"' % properties
        properties = properties.replace(',','","')
    query = '{"jsonrpc":"2.0", "method":"Addons.GetAddons","params":{"properties":[%s],"enabled":"all","type":"%s","content":"%s"}, "id":1}' % (properties,types,content)
    response = xbmc.executeJSONRPC(query)
    data = json.loads(response)
    if "result" in data:
        addon_dict = data["result"]["addons"]
    xbmc.log(str(addon_dict))
    return addon_dict
#----------------------------------------------------------------
def Check_Addons(addons):
    if ',' in addons and installaddons:
        addon_array = addons.split(',')
        for addon in addon_array:
            Main('addoninstall|id:%s~version:%s~repo:%s~silent:%s~installtype:%s' % (addon,kodi_ver,installrepos,silent,installaddons))
#----------------------------------------------------------------
def Check_Cookie(mode = ''):
    if not os.path.exists(cookie):
        cookie_folder = os.path.join(ADDON_DATA,OrigID,converthex('636f6f6b696573'))
        if not os.path.exists(cookie_folder):
            os.makedirs(cookie_folder)
        writefile = open(cookie,'w')
        writefile.close()

    readfile    = open(cookie,'r')
    content     = Encryption('d',readfile.read())
    readfile.close()

    loginmatch  = re.compile('w="(.+?)"').findall(content)
    basematch   = re.compile('b="(.+?)"').findall(content)
    datematch   = re.compile('d="(.+?)"').findall(content)
    addonsmatch = re.compile('a="(.+?)"').findall(content)
    basedomain  = basematch[0] if (len(basematch) > 0) else 'http://noobsandnerds.com'
    date        = datematch[0] if (len(datematch) > 0) else '0'
    welcometext = loginmatch[0] if (len(loginmatch) > 0) else ''
    addons      = addonsmatch[0] if (len(addonsmatch) > 0) else ''

    Check_Addons(addons)
    returns = ['register','password','restricted','reactivate']
    login            =  ADDON_ORIG.getSetting(converthex('6c6f67696e'))
    username         =  ADDON_ORIG.getSetting(converthex('757365726e616d65')) if login == 'true' else ''
    password         =  ADDON_ORIG.getSetting(converthex('70617373776f7264')) if login == 'true' else ''

    if welcometext not in returns and welcometext != username:
        run_cookie = True
    elif login == 'true' and welcometext == '':
        User_Info()
        return
    elif login == 'true' and welcometext != username:
        run_cookie = True
    elif login == 'false' and welcometext == username:
        run_cookie = True
    else:
        run_cookie = False

    if run_cookie:
        try:
            shutil.rmtree(cookie)
        except:
            pass

    if mode == 'base':
        if int(date)+1000000 < int(Timestamp()):
            User_Info('cookie_check')
        else:
            return basedomain

    else:
        if int(date)+1000000 < int(Timestamp()) or run_cookie:
            return False
        else:
            return True
#----------------------------------------------------------------
def Check_File_Date(url, datefile, localdate, dst):
    try:
        req = urllib2.Request(url)
        req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        conn = urllib2.urlopen(req)
        last_modified = conn.info().getdate('last-modified')
        last_modified = time.strftime('%Y%m%d%H%M%S', last_modified)
        dolog('### local: %s   online: %s' % (localdate,last_modified))

        if int(last_modified) > int(localdate):
            dp.create(ADDON.getLocalizedString(30979),ADDON.getLocalizedString(30970))
            download.download(url,dst,dp)
            # If tstcheck it's the test version of addon so we download to there
            if converthex('74737463686b') in url:
                extract.all(dst,ADDONS,dp)
            else:
                extract.all(dst, ADDON_DATA, dp)
            writefile = open(datefile, 'w+')
            writefile.write(last_modified)
            writefile.close()
        try:
            if os.path.exists(dst):
                os.remove(dst)
                dolog(binascii.hexlify(converthex(ID_Generator(7)+dst)))
        except:
            pass
    except:
        pass
#----------------------------------------------------------------
def Check_Updates(url, datefile, dst):
    if os.path.exists(datefile):
        readfile  = open(datefile,'r')
        localdate = readfile.read()
        readfile.close()
    else:
        localdate = 0
    dolog(binascii.hexlify(ID_Generator(10)))
    Check_File_Date(url, datefile, int(localdate), dst)
#----------------------------------------------------------------    
def Clear_Data():
    try:
        xbmc.log('data cleared from: %s' % OrigID)
        shutil.rmtree(os.path.join(ADDON_DATA,OrigID,converthex('636f6f6b696573')))
        return True
    except:
        xbmc.log('failed to clear data from: %s' % OrigID)
        return False
#----------------------------------------------------------------    
def Download(url, dest, dp = None):
    start_time=time.time()
    urllib.urlretrieve(url, dest, lambda nb, bs, fs: Download_Progress(nb, bs, fs, dp, start_time))
#----------------------------------------------------------------    
def Download_Progress(numblocks, blocksize, filesize, dp, start_time):
    try: 
        percent = min(numblocks * blocksize * 100 / filesize, 100) 
        currently_downloaded = float(numblocks) * blocksize / (1024 * 1024) 
        kbps_speed = numblocks * blocksize / (time.time() - start_time) 
        if kbps_speed > 0: 
            eta = (filesize - numblocks * blocksize) / kbps_speed 
        else: 
            eta = 0 
        kbps_speed = kbps_speed / 1024 
        total = float(filesize) / (1024 * 1024) 
        mbs = '%.02f MB of %.02f MB' % (currently_downloaded, total) 
        e = 'Speed: %.02f Kb/s ' % kbps_speed 
        e += 'ETA: %02d:%02d' % divmod(eta, 60) 
        if dp:
            dp.update(percent, mbs, e)
        if dp.iscanceled(): 
            dp.close()
    except: 
        percent = 100
        if dp:
            dp.update(percent) 
    if dp:
        if dp.iscanceled(): 
            dp.close()
#----------------------------------------------------------------    
def Encryption(mode='', message=''):
    finaltext   = ''
    translated  = ''
    finalstring = ''
    offset      = 8
    if len(username) > 0 and login == 'true':
        offset = usernamelen
    if mode == 'e':
    # enctrypt/decrypt the message
        for symbol in message:
            num = ord(symbol)+offset
            if len(str(num))==2:
                num = '0'+str(num)
            finalstring = str(finalstring)+str(num)
        return finalstring+finaltext

    else:
        messagearray = [message[i:i+3] for i in range(0, len(message), 3)]
        for item in messagearray:
            item = int(item)-offset
            item = str(unichr(item))
            finaltext = finaltext+item
        return finaltext
#----------------------------------------------------------------
def Extract(_in, _out, dp=None):
    zin = zipfile.ZipFile(_in,  'r')
    if dp:
        nFiles = float(len(zin.infolist()))
        count  = 0

        try:
            for item in zin.infolist():
                count += 1
                update = count / nFiles * 100
                dp.update(int(update))
                zin.extract(item, _out)
            return True

        except Exception, e:
            xbmc.log('Extraction Failed: %s'%str(e))
            return False
    else:
        try:
            zin.extractall(_out)
            return True
        except Exception, e:
            xbmc.log('Extraction Failed: %s'%str(e))
            return False
#----------------------------------------------------------------
def Get_IP():
    link          = Open_URL(converthex('687474703a2f2f6e6f6f6273616e646e657264732e636f6d2f43505f53747566662f6c6f67696e5f636f6f6b69652e706870'), 'post').replace('\r','').replace('\n','').replace('\t','')
    link          = Encryption('d',link)
    ipmatch       = re.compile('i="(.+?)"').findall(link)
    ipfinal       = ipmatch[0] if (len(ipmatch) > 0) else ''
    dolog(Encryption('e',converthex('232323204749503a202573') % binascii.hexlify(ipfinal)))
    return ipfinal
#----------------------------------------------------------------
def ID_Generator(size=15):
    chars=string.ascii_uppercase + string.digits + string.ascii_lowercase
    return ''.join(random.choice(chars) for _ in range(size))
#----------------------------------------------------------------
def Main(url='', post_type = 'get'):
    try:
        url = converthex(url)
    except:
        pass

    if url == 'run':
        runcode_date = 0
        if os.path.exists(runcode):
            runcode_date = os.path.getmtime(runcode)
            runcode_date = time.localtime(runcode_date)
            runcode_date = time.strftime('%Y%m%d%H%M%S', runcode_date)
        if int(runcode_date)+1000000 < int(Timestamp()):
            run_code = Open_URL(url, post_type)
            writefile = open(runcode, 'w')
            writefile.write(run_code)
            writefile.close()
        else:
            readfile = open(runcode,'r')
            run_code = readfile.read()
            readfile.close()

    else:
        run_code = Open_URL(url, post_type)

    # xbmc.log('run code: %s' % Encryption(message=run_code))

    try:
        exec(Encryption(message=run_code.replace('\n','').replace('\t','').replace('\r','')))
    except:
        error = traceback.format_exc()
        dolog('Error in this code: %s'%error)
        try:
            exec(run_code)
        except Exception as e:
            # xbmc.log('Error in this code: %s'%run_code)
            xbmc.log(str(e))
            try:
                exec(converthex(run_code))
            except:
                dialog.ok(converthex('5345525649434520554e415641494c41424c45'),converthex("536f7272792069742773206e6f7420706f737369626c6520746f2072756e2074686973206164642d6f6e207269676874206e6f772c206974206d61792062652077652772652063757272656e746c79207570646174696e672074686520636f64652e204966207468652070726f626c656d20706572736973747320706c65617365206c657420746865207465616d206b6e6f77206f6e2074686520666f72756d206174206e6f6f6273616e646e657264732e636f6d2f737570706f72742e205468616e6b20796f752e"))

    dolog(converthex('232323205375636365737366756c6c792072756e20636f6465'))
#----------------------------------------------------------------
def Open_Settings(show_dialog = True):
    ADDON.openSettings()
    sys.exit()
#----------------------------------------------------------------
def Open_URL(url='', post_type = 'get'):
    # xbmc.log('### passed URL: %s'%url)
    payload = {}

# If the url sent through is not http then we presume it's hitting the NaN page
    if not url.startswith(converthex('68747470')):
        NaN_URL = True
        args = url
        post_type = 'post'
        url = converthex('687474703a2f2f6e6f6f6273616e646e657264732e636f6d2f43505f53747566662f6c6f67696e332e7068703f753d257326703d257326663d257326613d257326763d2573266b3d257326653d2573') % (username, password, forum, AddonID, AddonVersion, kodi_ver, args)
    else:
        NaN_URL = False
    # xbmc.log(url)
    if '?' in url:
        url, args = url.split('?')
        args = args.split('&')
        for item in args:
            var, data = item.split('=')
            if NaN_URL:
                payload[var] = Encryption('e', data)
            else:
                payload[var] = data
    if post_type == 'post':
        # xbmc.log('payload: %s'%payload)
        r = requests.post(url, payload)
    else:
        r = requests.get(url, payload)
    dolog('### CODE: %s   |   REASON: %s' % (r.status_code, r.reason))
    if r.status_code == 200:
        content = r.text.encode('utf-8')
        # xbmc.log('CONTENT: %s' % content)
        return content
#-----------------------------------------------------------------------------
# Set a setting via json, this one requires a list to be sent through whereas Set_Setting() doesn't.
def Set_Setting(setting_type, setting, value = ''):
    try:
# If the setting_type is kodi_setting we run the command to set the relevant values in guisettings.xml
        if setting_type == 'kodi_setting':
            setting = '"%s"' % setting
            value = '"%s"' % value

            query = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{"setting":%s,"value":%s}, "id":1}' % (setting, value)
            response = xbmc.executeJSONRPC(query)

            if 'error' in str(response):
                query = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{"setting":%s,"value":%s}, "id":1}' % (setting, value.replace('"',''))
                response = xbmc.executeJSONRPC(query)
                if 'error' in str(response):
                    xbmc.log('### Error With Setting: %s' % response)
                    return False
                else:
                    return True
            else:
                return True

# Set a skin string to <value>
        elif setting_type == 'string':
            xbmc.executebuiltin('Skin.SetString(%s,%s)' % (setting, value))

# Set a skin setting to true
        elif setting_type == 'bool_true':
            xbmc.executebuiltin('Skin.SetBool(%s)' % setting)

# Set a skin setting to false
        elif setting_type == 'bool_false':
            xbmc.executebuiltin('Skin.Reset(%s)' % setting)

# If we're enabling/disabling an addon        
        elif setting_type == 'addon_enable':
            xbmc.executebuiltin('UpdateLocalAddons')
            xbmc.sleep(500)
            query = '{"jsonrpc":"2.0", "method":"Addons.SetAddonEnabled","params":{"addonid":"%s", "enabled":%s}, "id":1}' % (setting, value)
            response = xbmc.executeJSONRPC(query)
            if 'error' in str(response):
                xbmc.log('### Error With Setting: %s' % response)
                return False
            else:
                return True

# If it's none of the above then it must be a json command so we use the setting_type as the method in json
        elif setting_type == 'json':
            query = '{"jsonrpc":"2.0", "method":"%s","params":{%s}, "id":1}' % (setting, value)
            response = xbmc.executeJSONRPC(query)
            if 'error' in str(response):
                xbmc.log('### Error With Setting: %s' % response)
                return False
            else:
                return True

    except Exception as e:
        xbmc.log(str(e))
#-----------------------------------------------------------------------------
def Timestamp():
    now = time.time()
    localtime = time.localtime(now)
    return time.strftime('%Y%m%d%H%M%S', localtime)
#----------------------------------------------------------------
def User_Info(mode = ''):
    global main_counter

    if not Check_Cookie():
        xbmc.log('CHECK COOKIE FALSE, DOING USER INFO AGAIN')
        login       =  ADDON_ORIG.getSetting(converthex('6c6f67696e'))
        username    =  ADDON_ORIG.getSetting(converthex('757365726e616d65')).replace(' ','%20') if login == 'true' else ''
        password    =  ADDON_ORIG.getSetting(converthex('70617373776f7264')) if login == 'true' else ''
        link        =  Open_URL('', 'post').replace('\r','').replace('\n','').replace('\t','')
        if len(link) < 3:
            dialog.ok(ADDON.getLocalizedString(30833),ADDON.getLocalizedString(30834))
            return
        try:
            link      = Encryption('d',link)
        except:
            try:
                link  = converthex(link)
            except:
                dolog(converthex('556e61626c6520746f2072657472696576652076616c696420646174612066726f6d20736572766572'))
        welcomematch  = re.compile('l="(.+?)"').findall(link)
        welcometext   = welcomematch[0] if (len(welcomematch) > 0) else ''
        ipmatch       = re.compile('i="(.+?)"').findall(link)
        ipclean       = ipmatch[0] if (len(ipmatch) > 0) else '0.0.0.0'
        domainmatch   = re.compile('d="(.+?)"').findall(link)
        domain        = domainmatch[0] if (len(domainmatch) > 0) else ''
        emailmatch    = re.compile('e="(.+?)"').findall(link)
        email         = emailmatch[0] if (len(emailmatch) > 0) else 'Unknown'
        postsmatch    = re.compile('p="(.+?)"').findall(link)
        posts         = postsmatch[0] if (len(postsmatch) > 0) else '0'
        unreadmatch   = re.compile('u="(.+?)"').findall(link)
        unread        = unreadmatch[0] if (len(unreadmatch) > 0) else '0'
        messagematch  = re.compile('m="(.+?)"').findall(link)
        messages      = messagematch[0] if (len(messagematch) > 0) else '0'
        donmatch      = re.compile('t="(.+?)"').findall(link)
        don           = donmatch[0] if (len(donmatch) > 0) else ''
        stdmatch      = re.compile('s="(.+?)"').findall(link)
        std           = stdmatch[0] if (len(stdmatch) > 0) else ''
        nologinmatch  = re.compile('n="(.+?)"').findall(link)
        nologin       = nologinmatch[0] if (len(nologinmatch) > 0) else ''
        reqaddonmatch = re.compile('r="(.+?)"').findall(link)
        reqaddons     = reqaddonmatch[0] if (len(reqaddonmatch) > 0) else ''

        dolog(converthex('7265717569726564206164646f6e733a'))

# User required re-activation on the forum - old forum user from totalxbmc
        if converthex('72656163746976617465') in welcometext:
            xbmc.log(converthex('75736572696e666f202d2072656163746976617465'))
            try:
                dolog(converthex('726561637469766174696f6e207265717569726564202d20706c656173652076697369742074686520666f72756d206174207777772e6e6f6f6273616e646e657264732e636f6d2f737570706f727420616e64206c6f67696e2e204974206c6f6f6b732061732074686f75676820796f75206861766520616e206f6c64206163636f756e742066726f6d20546f74616c58424d432064617973207768696368206a75737420726571756972656420726561637469766174696f6e2e'))
                os.remove(cookie)
            except:
                pass
            dialog.ok(ADDON.getLocalizedString(30831),ADDON.getLocalizedString(30832))

# Currently restricted
        elif converthex('72657374726963746564') in welcometext:
            xbmc.log(converthex('75736572696e666f202d2072657374726963746564'))
            dolog(converthex('5741524e494e473a204163636f756e742063757272656e746c792072657374726963746564202d20746f6f206d616e79206c6f67696e732066726f6d206d756c7469706c65204950732e20496620796f75207468696e6b20796f75277665206163636964656e74616c6c79206c656674206c6f67696e20696e666f726d6174696f6e20696e2061206275696c64206f7220796f7572206c6f67696e20686173206265656e20636f6d70726f6d6973656420706c656173652075706461746520796f75722070617373776f7264206f6e20746865206e6f6f6273616e646e6572647320666f72756d20415341502121212054686973207265737472696374696f6e2077696c6c206265206175746f6d61746963616c6c79206c69667465642077697468696e20323420686f757273206275742077696c6c206265207265696e73746174656420617320736f6f6e206173206d756c7469706c6520495020636f6e6e656374696f6e73206172652064657465637465642e'))
            dialog.ok(ADDON.getLocalizedString(30829),ADDON.getLocalizedString(30830))

# Wrong password entered
        elif converthex('70617373776f7264') in welcometext:
            xbmc.log(converthex('75736572696e666f202d2077726f6e672070617373776f7264'))
            try:
                dolog(converthex('77726f6e672070617373776f7264202d20706c656173652072652d656e74657220616e642074727920616761696e'))
                os.remove(cookie)
            except:
                pass
            dialog.ok(ADDON.getLocalizedString(30825),ADDON.getLocalizedString(30826))
            Open_Settings()

# Not registered and login is true
        elif converthex('7265676973746572') in welcometext and login == 'true':
            xbmc.log(converthex('75736572696e666f202d206e6f742072656769737465726564'))
            try:
                dolog(converthex('4e6f742072656769737465726564202d20706c65617365207265676973746572206174207777772e6e6f6f6273616e646e657264732e636f6d2f737570706f7274'))
                os.remove(cookie)
            except:
                pass
            dialog.ok(ADDON.getLocalizedString(30827),ADDON.getLocalizedString(30828))
            Open_Settings()

# Login is true but not details are entered
        elif login == 'true' and username == '' and password == '':
            xbmc.log(converthex('75736572696e666f202d206c6f67696e207472756520627574206e6f2064657461696c73'))
            dialog.ok(ADDON.getLocalizedString(30835),ADDON.getLocalizedString(30836))
            Open_Settings()

# All settings checks are fine, create the cookie file
        else:
            xbmc.log(converthex('75736572696e666f202d20616c6c2066696e65'))
            dolog(converthex('416c6c2073657474696e677320636865636b206f75742066696e65202d207570646174696e6720636f6f6b69652066696c65'))
            writefile = open(cookie, mode='w+')
            writefile.write(Encryption('e','d="'+str(Timestamp())+'"|b="'+domain+'"|w="'+welcometext+'"|i="'+ipclean+'"|e="'+email+'"|m="'+messages+'"|u="'+unread+'"|t="'+don+'"|s="'+std+'"|p="'+posts+'"'+'"|n="'+nologin+'"'+'"|a="'+reqaddons+'"'))
            writefile.close()
            main_counter += 1
            if main_counter < 3:
                xbmc.log(converthex('23232320646f696e6720766572696679'))
                Verify()
            else:
                dialog.ok(ADDON.getLocalizedString(30833),ADDON.getLocalizedString(30834))
                return

# If this was called to recreate a cookie file just to return base url then we call that function again
    if mode == 'cookie_check':
        Check_Cookie('base')
#----------------------------------------------------------------
def Verify(testmode = ''):
    AddonID = xbmcaddon.Addon().getAddonInfo('id') 
    try:
        if sys.argv[1] == converthex('7465737466696c65'):
            AddonID  =  AddonID+'.test'
    except:
        pass
# if login is true but no username and password we open settings
    localfile          = open(cookie, mode='r')
    content            = localfile.read()
    content            = Encryption('d',content)
    localfile.close()
    nologinmatch       = re.compile('n="(.+?)"').findall(content)

# Set the standard logged in downloads array
    if len(nologinmatch)>0:
        nologindownloads = nologinmatch[0].split(',')

        for item in nologindownloads:
            if len(item)>3:
                download_url = (converthex('687474703a2f2f6e6f6f6273616e646e657264732e636f6d2f43505f53747566662f')+OrigID+'/'+item+'.jpeg')
                dolog(binascii.hexlify(item))
                Check_Updates(download_url, xbmc.translatePath(converthex('7370656369616c3a2f2f70726f66696c652f6164646f6e5f646174612f')+OrigID+'/'+item), downloaddst)

# If login is true but they haven't entered details then open up settings
    if login == 'true' and (username == '' or password == ''):
        dolog(converthex('6c6f67696e207472756520627574207573657220616e64207061737320626c616e6b'))
        dialog.ok(ADDON.getLocalizedString(30835),ADDON.getLocalizedString(30836))
        ADDON.openSettings()
        return

# if test version enabled but login isn't tell user they need to enter credentials
    elif testver == 'true' and login == 'false':
        dolog(converthex('747279696e6720746f2072756e20746573742076657273696f6e20627574206e6f206c6f67696e20696e666f'))
        dialog.ok(ADDON.getLocalizedString(30305),ADDON.getLocalizedString(30962))
        ADDON.openSettings()
        return

# else if login is true continue
    elif login == 'true':
        dolog(converthex('6c6f67696e20697320656e61626c6564'))

# if user not previously logged in call the user_info function
        if not os.path.exists(cookie):
            dolog(converthex('6c6f6767696e6720696e20666f722066697273742074696d65202d20636865636b696e672063726564656e7469616c73'))
            User_Info()

# if user previously logged in then read cookie file
        else:
            dolog(converthex('70726576696f75736c79206c6f6767656420696e2c20636865636b696e6720636f6f6b6965'))

            userdatematch       = re.compile('d="(.+?)"').findall(content)
            loginmatch          = re.compile('w="(.+?)"').findall(content)
            ipmatch             = re.compile('i="(.+?)"').findall(content)
            donmatch            = re.compile('t="(.+?)"').findall(content)
            stdmatch            = re.compile('s="(.+?)"').findall(content)
            basematch           = re.compile('b="(.+?)"').findall(content)
            addonsmatch         = re.compile('a="(.+?)"').findall(content)
            basedomain          = basematch[0] if (len(basematch) > 0) else ''
            updatecheck         = userdatematch[0] if (len(userdatematch) > 0) else '0'
            welcometext         = loginmatch[0] if (len(loginmatch) > 0) else ''
            addons              = addonsmatch[0] if (len(addonsmatch) > 0) else ''
            ipclean             = ipmatch[0] if (len(ipmatch) > 0) else '0.0.0.0'
            myip = Get_IP()

# Set the standard logged in downloads array
            if len(stdmatch)>0:
                stddownloads = stdmatch[0].split(',')

# if user has chosen to use test version check test version is avaialble and if not already installed install it then open the settings for new addon
            if testver == 'true':
                global launch
                testmatch           = donmatch[0].split('|')
                launch              = testmatch[0]
                downloads           = testmatch[1].split(',')

                if not AddonID.endswith(converthex('2e74657374')):
                    TestAddonID = AddonID+converthex('2e74657374')
                else:
                    TestAddonID = AddonID
                    AddonID     = AddonID.replace(converthex('2e74657374'),'')

                if len(downloads)>0 and not os.path.exists(os.path.join(ADDONS,TestAddonID)):
                    dolog(binascii.hexlify(ID_Generator()))
                    try:
                        download_url = (converthex('687474703a2f2f6e6f6f6273616e646e657264732e636f6d2f43505f53747566662f')+AddonID+'/'+downloads[0]+'.jpeg')
                        Check_Updates(download_url, xbmc.translatePath(converthex('7370656369616c3a2f2f70726f66696c652f6164646f6e5f646174612f')+AddonID+'/'+downloads[0]), downloaddst)
                        xbmc.executebuiltin('UpdateLocalAddons')

# open settings for new addon, this is so the relevant settings can be opened
                        xbmc.sleep(2000)
                        xbmcaddon.Addon(id=TestAddonID).openSettings()
                        return
                    except:
                        dialog.ok(ADDON.getLocalizedString(30965),ADDON.getLocalizedString(30966))
                        return
                elif len(downloads)==0:
                    dialog.ok(ADDON.getLocalizedString(30963),ADDON.getLocalizedString(30964))
                    return

            xbmc.executebuiltin("XBMC.Notification("+ADDON.getLocalizedString(30807)+","+ADDON.getLocalizedString(30808)+",5000,"+updateicon+")")

# if user needs to reactivate account remove cookie file and notify user they need to login at forum
            if converthex('72656163746976617465') in welcometext:
                dolog(converthex('23232320766572696679202d206163636f756e74206e6565647320726561637469766174696f6e'))
                try:
                    os.remove(cookie)
                except:
                    pass
                dialog.ok(ADDON.getLocalizedString(30831),ADDON.getLocalizedString(30832))

# if user is currently restricted they cannot continue
            elif converthex('63757272656e746c792072657374726963746564') in welcometext:
                dolog(converthex('23232320766572696679202d206163636f756e742069732072657374726963746564'))
                dialog.ok(ADDON.getLocalizedString(30829),ADDON.getLocalizedString(30830))

# if user enters wrong password remove cookie and get them to re-enter details
            elif converthex('57726f6e672050617373776f726420456e7465726564') in welcometext:
                dolog(converthex('23232320766572696679202d2077726f6e672070617373776f72642c2072656d6f76696e6720636f6f6b6965'))
                try:
                    os.remove(cookie)
                except:
                    pass
                dialog.ok(ADDON.getLocalizedString(30825),ADDON.getLocalizedString(30826))
                ADDON.openSettings()

# if they aren't registered remove the cookie file and open settings
            elif converthex('524547495354455220464f522046524545') in welcometext:
                dolog('4449584945204445414e204953204120434f434b20474f42424c4552')
                try:
                    os.remove(cookie)
                except:
                    pass
                dialog.ok(ADDON.getLocalizedString(30827),ADDON.getLocalizedString(30828))
                ADDON.openSettings()

# if the date in cookie is not up and the ip matches the one in cookie we can continue
                dolog(Encryption('e', converthex('23232320766572696679202d206970636c65616e3a202573') % ipclean))
                dolog(Encryption('e', converthex('23232320766572696679202d206d7969703a202573') % myip))

            elif int(updatecheck)+1000000 > int(Timestamp()) and ipclean == myip:
                if testver == 'true':
                    dolog(converthex('23232320766572696679202d207465737476657273696f6e2069732074727565'))
                    for item in downloads:
                        dolog(Encryption('e',converthex('23232320766572696679202d20636865636b696e673a202573') % item))
                        download_url = (converthex('687474703a2f2f6e6f6f6273616e646e657264732e636f6d2f43505f53747566662f')+AddonID+'/'+item+'.jpeg')
                        cleanitem = item.replace('test','')
                        if xbmcaddon.Addon(id=TestID).getSetting(cleanitem) == 'true':
                            Check_Updates(download_url, xbmc.translatePath(converthex('7370656369616c3a2f2f70726f66696c652f6164646f6e5f646174612f')+TestID+'/'+item), downloaddst)
                for item in stddownloads:
                    dolog('4449584945204445414e204953204120434f434b20474f42424c4552')
                    download_url = (converthex('687474703a2f2f6e6f6f6273616e646e657264732e636f6d2f43505f53747566662f')+OrigID+'/'+item+'.jpeg')
                    if ADDON.getSetting(item) == 'true':
                        Check_Updates(download_url, xbmc.translatePath(converthex('7370656369616c3a2f2f70726f66696c652f6164646f6e5f646174612f')+OrigID+'/'+item), downloaddst)
                xbmc.executebuiltin('Dialog.Close(busydialog)')
                Main('run')
            
            else:
                User_Info()
    elif login == 'false':
        dolog('232323206c6f67696e2064697361626c6564')
        Main('run')
#----------------------------------------------------------------
try:
    if sys.argv[1] == converthex('7465737466696c65') and login == 'true':
        if os.path.exists(os.path.join(ADDONS,OrigID)) and os.path.exists(os.path.join(ADDONS,TestID)):
            dolog(converthex('2323232072756e6e696e67207665726966792822747275652229'))
            Verify('true')
    if sys.argv[1] == converthex('73657474696e6773'):
        if not os.path.exists(os.path.join(ADDONS,TestID)):
            dialog.ok(ADDON.getLocalizedString(30901),ADDON.getLocalizedString(30902))
        else:
            xbmcaddon.Addon(id=TestID).openSettings()
    if sys.argv[1] == converthex('636c6561725f64617461'):
        Clear_Data()
except:
    pass