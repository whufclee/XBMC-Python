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

import xbmc, xbmcaddon, xbmcgui, os, re, urllib, urllib2
import time, shutil, binascii, hashlib, sys
import extract, download
#import unicodedata

def converthex(url):
    return binascii.unhexlify(url)


AddonID          =  xbmcaddon.Addon().getAddonInfo('id') 
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
USERDATA         =  xbmc.translatePath(converthex('7370656369616c3a2f2f686f6d652f7573657264617461'))
ADDON_DATA       =  xbmc.translatePath(os.path.join(USERDATA,converthex('6164646f6e5f64617461')))
ADDONS           =  xbmc.translatePath(converthex('7370656369616c3a2f2f686f6d652f6164646f6e73'))
installfile      =  os.path.join(ADDONS,AddonID,converthex('6c6f67696e2e7079'))
updateicon       =  os.path.join(ADDONS,AddonID,converthex('7265736f7572636573'),converthex('7570646174652e706e67'))
bakfile          =  os.path.join(ADDONS,AddonID,converthex('7265736f7572636573'),converthex('6261636b7570'))
cookie           =  xbmc.translatePath(os.path.join(ADDON_DATA,OrigID,converthex('636f6f6b696573'),converthex('74656d70')))
login            =  ADDON_ORIG.getSetting(converthex('6c6f67696e'))
forum            =  ADDON_ORIG.getSetting(converthex('666f72756d'))
username         =  ADDON_ORIG.getSetting(converthex('757365726e616d65')).replace(' ','%20')
password         =  ADDON_ORIG.getSetting(converthex('70617373776f7264'))
dialog           =  xbmcgui.Dialog()
downloaddst      =  xbmc.translatePath(converthex('7370656369616c3a2f2f686f6d652f6164646f6e732f7061636b616765732f6370'))
stop             =  0
launch           =  'launch.py'
downloads        =  []
stddownloads     =  []
nologindownloads =  []

if forum == converthex('556e6f6666696369616c204b6f646920537570706f7274'):
    forum = 'k'
if forum == converthex('436f6d6d756e697479204275696c647320537570706f7274'):
    forum = 'c'

xmlfile = converthex('6164646f6e2e786d6c')
addonxml = xbmc.translatePath(os.path.join(ADDONS,AddonID,xmlfile))
localaddonversion = open(addonxml, mode='r')
content = file.read(localaddonversion)
file.close(localaddonversion)
localaddonvermatch = re.compile('<ref>(.+?)</ref>').findall(content)
addonversion  = localaddonvermatch[0] if (len(localaddonvermatch) > 0) else ''
localcheck = hashlib.md5(open(installfile,'rb').read()).hexdigest()
#if addonversion != localcheck:
#  readfile = open(bakfile, mode='r')
#  content  = file.read(readfile)
#  file.close(readfile)
#  writefile = open(installfile, mode='w+')
#  writefile.write(content)
#  writefile.close()

def Check_File_Date(url, datefile, localdate, dst):
    try:
        xbmc.log('### Checking %s  |  datefile: %s  |  localdate: %s  |  dst: %s' % (url, datefile, localdate, dst))
        req = urllib2.Request(url)
        req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        conn = urllib2.urlopen(req)
        last_modified = conn.info().getdate('last-modified')
        last_modified = time.strftime('%Y%m%d%H%M%S', last_modified)
        if int(last_modified) > int(localdate):
            download.download(url,dst)
            if converthex('74737463686b') in url:
                extract.all(dst,ADDONS)
            else:
                extract.all(dst, ADDON_DATA)
            writefile = open(datefile, 'w+')
            writefile.write(last_modified)
            writefile.close()
        try:
            if os.path.exists(dst):
                os.remove(dst)
        except:
            pass
    except:
        pass

def Check_Updates(url, datefile, dst):
    if os.path.exists(datefile):
        readfile = open(datefile,'r')
        localdate = readfile.read()
        readfile.close()
    else:
        localdate = 0
    Check_File_Date(url, datefile, int(localdate), dst)

def Open_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent' , 'Mozilla/5.0 (Windows; U; Windows NT 10.0; WOW64; Windows NT 5.1; en-GB; rv:1.9.0.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36 Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link     = response.read()
    response.close()
    return link.replace('\r','').replace('\n','').replace('\t','')


def Timestamp():
    now = time.time()
    localtime = time.localtime(now)
    return time.strftime('%Y%m%d%H%M%S', localtime)


def User_Info():
    BaseURL       = converthex('687474703a2f2f6e6f6f6273616e646e657264732e636f6d2f43505f53747566662f6c6f67696e2e7068703f753d257326703d257326663d257326613d2573') % (username, password, forum, AddonID)
    xbmc.log('### URL: %s' % BaseURL)
    try:
        link      = Open_URL(BaseURL)
        link      = binascii.unhexlify(link)
    except:
        dialog.ok(ADDON.getLocalizedString(30833),ADDON.getLocalizedString(30834))
        return
    welcomematch  = re.compile('l="(.+?)"').findall(link)
    welcometext   = welcomematch[0] if (len(welcomematch) > 0) else ''
    ipmatch       = re.compile('i="(.+?)"').findall(link)
    ipclean       = ipmatch[0] if (len(ipmatch) > 0) else '0.0.0.0'
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

    if converthex('72656163746976617465') in welcometext:
        try:
            os.remove(cookie)
        except:
            pass
        dialog.ok(ADDON.getLocalizedString(30831),ADDON.getLocalizedString(30832))
    elif converthex('63757272656e746c792072657374726963746564') in welcometext:
        dialog.ok(ADDON.getLocalizedString(30829),ADDON.getLocalizedString(30830))
    elif converthex('57726f6e672050617373776f726420456e7465726564') in welcometext:
        try:
            os.remove(cookie)
        except:
            pass
        dialog.ok(ADDON.getLocalizedString(30825),ADDON.getLocalizedString(30826))
        ADDON.openSettings()
    elif converthex('524547495354455220464f522046524545') in welcometext and login == 'true':
        try:
            os.remove(cookie)
        except:
            pass
        dialog.ok(ADDON.getLocalizedString(30827),ADDON.getLocalizedString(30828))
        ADDON.openSettings()
    elif login == 'true' and username == '' and password == '':
        dialog.ok(ADDON.getLocalizedString(30835),ADDON.getLocalizedString(30836))
        ADDON.openSettings()        
    else:
        writefile = open(cookie, mode='w+')
        writefile.write(encryptme('e','d="'+str(Timestamp())+'"|w="'+welcometext+'"|i="'+ipclean+'"|e="'+email+'"|m="'+messages+'"|u="'+unread+'"|t="'+don+'"|s="'+std+'"|p="'+posts+'"'+'"|n="'+nologin+'"'))
        writefile.close()
        verify()

def verify(testmode = ''):
    AddonID = xbmcaddon.Addon().getAddonInfo('id') 
    try:
        if sys.argv[1] == converthex('7465737466696c65'):
            AddonID  =  AddonID+'.test'
    except:
        pass
# if login is true but no username and password we open settings
    localfile          = open(cookie, mode='r')
    content            = localfile.read()
    content            = encryptme('d',content)
    localfile.close()
    nologinmatch       = re.compile('n="(.+?)"').findall(content)

# Set the standard logged in downloads array
    if len(nologinmatch)>0:
        nologindownloads = nologinmatch[0].split(',')

        for item in nologindownloads:
            download_url = (converthex('687474703a2f2f6e6f6f6273616e646e657264732e636f6d2f43505f53747566662f')+OrigID+'/'+item+'.jpeg')
            xbmc.log('### download_url: %s' % download_url)
            Check_Updates(download_url, xbmc.translatePath(converthex('7370656369616c3a2f2f70726f66696c652f6164646f6e5f646174612f')+OrigID+'/'+item), downloaddst)

    if login == 'true' and (username == '' or password == ''):
        dialog.ok(ADDON.getLocalizedString(30835),ADDON.getLocalizedString(30836))
        ADDON.openSettings()
        return

# if test version enabled but login isn't tell user they need to ender credentials
    elif testver == 'true' and login == 'false':
        dialog.ok(ADDON.getLocalizedString(30305),ADDON.getLocalizedString(30962))
        ADDON.openSettings()
        return

# else if login is true continue
    elif login == 'true':

# if user not previously logged in call the user_info function
        if not os.path.exists(cookie):
            User_Info()

# if user previously logged in then read cookie file
        else:
            userdatematch       = re.compile('d="(.+?)"').findall(content)
            loginmatch          = re.compile('w="(.+?)"').findall(content)
            ipmatch             = re.compile('i="(.+?)"').findall(content)
            donmatch            = re.compile('t="(.+?)"').findall(content)
            stdmatch            = re.compile('s="(.+?)"').findall(content)
            updatecheck         = userdatematch[0] if (len(userdatematch) > 0) else '0'
            welcometext         = loginmatch[0] if (len(loginmatch) > 0) else ''
            ipclean             = ipmatch[0] if (len(ipmatch) > 0) else '0.0.0.0'
            myip = getIP()

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

            xbmc.executebuiltin("XBMC.Notification("+ADDON.getLocalizedString(30807)+","+ADDON.getLocalizedString(30808)+",10000,"+updateicon+")")

# if user needs to reactivate account remove cookie file and notify user they need to login at forum
            if converthex('72656163746976617465') in welcometext:
                try:
                    os.remove(cookie)
                except:
                    pass
                dialog.ok(ADDON.getLocalizedString(30831),ADDON.getLocalizedString(30832))

# if user is currently restricted they cannot continue
            elif converthex('63757272656e746c792072657374726963746564') in welcometext:
                dialog.ok(ADDON.getLocalizedString(30829),ADDON.getLocalizedString(30830))

# if user enters wrong password remove cookie and get them to re-enter details
            elif converthex('57726f6e672050617373776f726420456e7465726564') in welcometext:
                try:
                    os.remove(cookie)
                except:
                    pass
                dialog.ok(ADDON.getLocalizedString(30825),ADDON.getLocalizedString(30826))
                ADDON.openSettings()

# if they aren't registered remove the cookie file and open settings
            elif converthex('524547495354455220464f522046524545') in welcometext:
                try:
                    os.remove(cookie)
                except:
                    pass
                dialog.ok(ADDON.getLocalizedString(30827),ADDON.getLocalizedString(30828))
                ADDON.openSettings()

# if the date in cookie is not up and the ip matches the one in cookie we can continue
            elif int(updatecheck)+1000000 > int(Timestamp()) and ipclean == myip:
                if testver == 'true':
                    for item in downloads:
                        download_url = (converthex('687474703a2f2f6e6f6f6273616e646e657264732e636f6d2f43505f53747566662f')+AddonID+'/'+item+'.jpeg')
                        cleanitem = item.replace('test','')
                        if xbmcaddon.Addon(id=TestID).getSetting(cleanitem) == 'true':
                            Check_Updates(download_url, xbmc.translatePath(converthex('7370656369616c3a2f2f70726f66696c652f6164646f6e5f646174612f')+TestID+'/'+item), downloaddst)
                for item in stddownloads:
                    download_url = (converthex('687474703a2f2f6e6f6f6273616e646e657264732e636f6d2f43505f53747566662f')+OrigID+'/'+item+'.jpeg')
                    if ADDON.getSetting(item) == 'true':
                        Check_Updates(download_url, xbmc.translatePath(converthex('7370656369616c3a2f2f70726f66696c652f6164646f6e5f646174612f')+OrigID+'/'+item), downloaddst)
                xbmc.executebuiltin('Dialog.Close(busydialog)')
                main()
            
            else:
                User_Info()
    elif login == 'false':
        main()

def getIP():
    BaseURL       = converthex('687474703a2f2f7768617469736d796970616464726573732e636f6d')
    link          = Open_URL(BaseURL).replace('\n','').replace('\r','')
    ipmatch       = re.compile(converthex('7768617469736d796970616464726573732e636f6d2f')+'ip/(.+?)"').findall(link)
    ipfinal       = ipmatch[0] if (len(ipmatch) > 0) else ''
    return ipfinal
    

def encryptme(mode, message):
    finaltext = ''
    if mode == 'e':
        finaltext = ''
        offset = len(username)
    # enctrypt/decrypt the message
        translated = ''
        finalstring = ''
        for symbol in message:
                num = ord(symbol)+offset
                if len(str(num))==2:
                    num = '0'+str(num)
                finalstring = str(finalstring)+str(num)
        return finalstring+finaltext
    else:
        key    = len(username)
        messagearray = [message[i:i+3] for i in range(0, len(message), 3)]
        for item in messagearray:
            item = int(item)-key
            item = str(unichr(item))
            finaltext = finaltext+item
        return finaltext

def main():          
        windowID = xbmcgui.Window(10000).getProperty('TVP_WINDOW')
        try:
            windowID = int(windowID)
            xbmc.executebuiltin('ActivateWindow(%d)' % windowID)  
            return
        except:
            pass

        if testver == 'true' and login == 'true':
            script = os.path.join(ADDONS, TestID, 'login.py')
            args   = launch
        else:
            script = os.path.join(ADDONS, AddonID, launch)
            args = ''

        name   = AddonID + ' Launcher'
        cmd    = 'AlarmClock(%s,RunScript(%s,%s),%d,True)' % (name, script, args, 0)

        xbmc.executebuiltin('CancelAlarm(%s,True)' % name)        
        xbmc.executebuiltin(cmd)

try:
    if sys.argv[1] == converthex('7465737466696c65') and login == 'true':
        if os.path.exists(os.path.join(ADDONS,OrigID)) and os.path.exists(os.path.join(ADDONS,TestID)):
            verify('true')
    if sys.argv[1] == converthex('73657474696e6773'):
        if not os.path.exists(os.path.join(ADDONS,TestID)):
            dialog.ok(ADDON.getLocalizedString(30901),ADDON.getLocalizedString(30902))
        else:
            xbmcaddon.Addon(id=TestID).openSettings()
except:
    pass