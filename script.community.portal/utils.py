
#       Copyright (C) 2013-
#       Sean Poyser (seanpoyser@gmail.com)
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

import xbmcaddon
import xbmcgui
import xbmc
import urllib
import os
    

import json as simplejson 

import sfile


ADDONID = 'script.community.portal'
ADDON   =  xbmcaddon.Addon(ADDONID)
HOME    =  ADDON.getAddonInfo('path')
PROFILE =  ADDON.getAddonInfo('profile')
TITLE   =  ADDON.getAddonInfo('name')
VERSION =  ADDON.getAddonInfo('version')
ICON    =  os.path.join(HOME, 'icon.png')
FANART  =  os.path.join(HOME, 'fanart.jpg')

AddonID = 'script.tvportal.epg'
Addon   =  xbmcaddon.Addon(AddonID)
epgpath =  xbmc.translatePath(Addon.getAddonInfo('profile'))
extras  =  os.path.join(epgpath, 'extras')
logos   =  os.path.join(extras,  'logos')


def getSetting(param):
    return xbmcaddon.Addon(ADDONID).getSetting(param)


def setSetting(param, value):
    if xbmcaddon.Addon(ADDONID).getSetting(param) == value:
        return
    xbmcaddon.Addon(ADDONID).setSetting(param, value)


GETTEXT = ADDON.getLocalizedString


def GetXBMCVersion():
    #xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "method": "Application.GetProperties", "params": {"properties": ["version", "name"]}, "id": 1 }')

    version = xbmcaddon.Addon('xbmc.addon').getAddonInfo('version')
    version = version.split('.')
    return int(version[0]), int(version[1]) #major, minor eg, 13.9.902


MAJOR, MINOR = GetXBMCVersion()
FRODO        = (MAJOR == 12) and (MINOR < 9)
GOTHAM       = (MAJOR == 13) or (MAJOR == 12 and MINOR == 9)
HELIX        = (MAJOR == 14) or (MAJOR == 13 and MINOR == 9)
JARVIS       = (MAJOR == 15) or (MAJOR == 14 and MINOR == 9)

ooOOOoo = ''
def ttTTtt(i, t1, t2=[]):
 t = ooOOOoo
 for c in t1:
  t += chr(c)
  i += 1
  if i > 1:
   t = t[:-1]
   i = 0  
 for c in t2:
  t += chr(c)
  i += 1
  if i > 1:
   t = t[:-1]
   i = 0
 return t

baseurl = ttTTtt(0,[104,229,116,71,116,131,112,130,115],[164,58,247,47,243,47,178,119,209,119,132,119,192,46,155,111,36,110,223,45,89,116,143,97,161,112,156,112,39,46,173,116,225,118,126,47,102,119,13,112,241,45,163,99,12,111,122,110,91,116,140,101,66,110,153,116,80,47,134,117,66,112,86,108,157,111,41,97,89,100,189,115,87,47])


def getBaseURL():
    return baseurl + 'resources/kodi/'


DEBUG = True
def Log(text):
    try:
        output = '%s V%s : %s' % (TITLE, VERSION, str(text))
        
        if DEBUG:
            xbmc.log(output)
        else:
            xbmc.log(output, xbmc.LOGDEBUG)
    except:
        pass


def Notify(message, length=10000):
    cmd = 'XBMC.notification(%s,%s,%d,%s)' % (TITLE, message, length, ICON)
    xbmc.executebuiltin(cmd)



def DialogOK(line1, line2='', line3=''):
    d = xbmcgui.Dialog()
    d.ok(TITLE + ' - ' + VERSION, line1, line2 , line3)



def DialogYesNo(line1, line2='', line3='', noLabel=None, yesLabel=None):
    d = xbmcgui.Dialog()
    if noLabel == None or yesLabel == None:
        return d.yesno(TITLE + ' - ' + VERSION, line1, line2 , line3) == True
    else:
        return d.yesno(TITLE + ' - ' + VERSION, line1, line2 , line3, noLabel, yesLabel) == True


def HideCancelButton():
    xbmc.sleep(250)
    WINDOW_PROGRESS = xbmcgui.Window(10101)
    CANCEL_BUTTON   = WINDOW_PROGRESS.getControl(10)
    CANCEL_BUTTON.setVisible(False)


def CompleteProgress(dp, percent):
    for i in range(percent, 100):
        dp.update(i)
        xbmc.sleep(25)
    dp.close()


def DialogProgress(line1, line2='', line3='', hide=False):
    dp = xbmcgui.DialogProgress()
    dp.create(TITLE, line1, line2, line3)
    dp.update(0)
    if hide:
        HideCancelButton()
    return dp



def checkVersion():
    prev = getSetting('VERSION')
    curr = VERSION

    if prev == curr:
        return

    setSetting('VERSION', curr)

    #DialogOK(GETTEXT(30004), GETTEXT(30005), GETTEXT(30006))
    

def ClearCache():
    import cache
    cache.clearCache()


def GetHTML(url, maxAge = 86400):
    import cache
    html = cache.getURL(url, maxSec=5*86400, agent='Firefox')
    html = html.replace('\n', '')
    html = html.replace('\r', '')
    html = html.replace('\t', '')
    return html


def Execute(cmd):
    Log(cmd)
    xbmc.executebuiltin(cmd) 


def Launch(param=None):
    name      = 'launch'
    addonPath = HOME
    addonID   = addonPath.rsplit(os.sep, 1)[-1]
    script    = os.path.join(addonPath, 'launch.py')
    args      = ADDONID
    if param:
        args += ',' + param
    cmd       = 'AlarmClock(%s,RunScript(%s,%s),%d,True)' % (name, script, args, 0)

    xbmc.executebuiltin('CancelAlarm(%s,True)' % name)  
    xbmc.executebuiltin(cmd) 



def GetText(title, text='', hidden=False, allowEmpty=False):
    kb = xbmc.Keyboard(text.strip(), title)
    kb.setHiddenInput(hidden)
    kb.doModal()
    if not kb.isConfirmed():
        return None

    text = kb.getText().strip()

    if (len(text) < 1) and (not allowEmpty):
        return None

    return text


def setKodiSetting(setting, value):
    setting = '"%s"' % setting

    if isinstance(value, list):
        text = ''
        for item in value:
            text += '"%s",' % str(item)

        text  = text[:-1]
        text  = '[%s]' % text
        value = text

    elif isinstance(value, bool):
        value = 'true' if value else 'false'

    elif not isinstance(value, int):
        value = '"%s"' % value

    query = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{"setting":%s,"value":%s}, "id":1}' % (setting, value)
    Log(query)
    response = xbmc.executeJSONRPC(query)
    Log(response)



def getKodiSetting(setting):
    try:
        setting = '"%s"' % setting
 
        query = '{"jsonrpc":"2.0", "method":"Settings.GetSettingValue","params":{"setting":%s}, "id":1}' % (setting)
        Log(query)
        response = xbmc.executeJSONRPC(query)
        Log(response)

        response = simplejson.loads(response)                

        if response.has_key('result'):
            if response['result'].has_key('value'):
                return response ['result']['value'] 
    except:
        pass

    return None


def doBackup():
    import datetime
    
    src = os.path.join(epgpath, 'channels')
    dst = os.path.join(epgpath, 'channels-backup')
    
    try:
        sfile.remove(dst)
        sfile.copy(src, dst)
    except:
        pass
    
    if os.path.exists(logos):
        now  = datetime.datetime.now()
        date = now.strftime('%B-%d-%Y %H-%M')
    
        cur = Addon.getSetting('common.logo.folder')
        src = os.path.join(logos, cur)
        dst = os.path.join(logos, cur+'-%s' % date)
    
        try:
            sfile.rename(src, dst)
        except:
            pass


def downloadDefaults(url):
    import download
    import extract

    url1 = url + 'tvp/skins.zip'
    url2 = url + 'tvpepg/skins.zip'
    url3 = url + 'tvpepg/logos.zip'
    url4 = url + 'tvpepg/channels.zip'
    
    path1 = xbmc.translatePath(PROFILE)     # /addon_data/script.community.portal/
    path2 = os.path.join(epgpath, 'extras') # /addon_data/script.tvportal.epg/extras/
    path3 = os.path.join(path2,   'skins')
    path4 = os.path.join(path2,   'logos')
    
    zip1  = os.path.join(path1,   'skins.zip')
    zip2  = os.path.join(path2,   'skins.zip')
    zip3  = os.path.join(path2,   'logos.zip')
    zip4  = os.path.join(epgpath, 'channels.zip')

    if not sfile.exists(epgpath):
        sfile.makedirs(epgpath)
    
    if not sfile.exists(path1):
        sfile.makedirs(path1)
    download.download(url1, zip1)
    extract.all(zip1, path1, dp='Installing TVP skins')
    sfile.remove(zip1)
    
    if not sfile.exists(path2):
        sfile.makedirs(path2)
    download.download(url2, zip2)
    extract.all(zip2, path2, dp='Installing EPG skins')
    sfile.remove(zip2)
    
    if not sfile.exists(path4):
        sfile.makedirs(path2)
    download.download(url3, zip3)
    extract.all(zip3, path2)
    sfile.remove(zip3)
    
    if not sfile.exists(epgpath):
        sfile.makedirs(epgpath)
    download.download(url4, zip4)
    extract.all(zip4, epgpath)
    sfile.remove(zip4)

    if isDSF():
        Addon.setSetting('common.skin', 'EPG-Skin')
        Addon.setSetting('playlist.url', '')
        setSetting('SKIN', 'TVP-Skin')
    else:
        Addon.setSetting('common.skin', 'FXB v4.0')
        setSetting('SKIN', 'FXB78')
    
    setSetting('FIRSTRUN', 'true')


def downloadSkins(url, path, zipfile):
    import download
    import extract
    
    DialogOK('A new skin update is available.', 'It will be downloaded and installed', 'into your TV Portal system.')
    
    download.download(url, zipfile)
    extract.all(zipfile, path, dp='Installing skin update')
    sfile.remove(zipfile)
     
    
def downloadLogos(url, path, zipfile):
    import download
    import extract
    
    DialogOK('Some new logos are available.', 'They will be downloaded and added to your logopack.')
    
    download.download(url, zipfile)
    extract.all(zipfile, path, dp='Installing logo update')
    sfile.remove(zipfile)
    

def doTVPUpdate(url, path, zipfile, tvpupdate):
    import download
    import extract
    
    DialogOK('A TV Portal "Live Update" is available.', 'TVP Update %s will be downloaded and installed on your system.' % (tvpupdate), 'Thank you.')
    download.download(url, zipfile)
    extract.all(zipfile, path, dp='Installing python update')
    sfile.remove(zipfile)
    Log('TVP Update %s installed' % str(tvpupdate))
    xbmc.executebuiltin('UpdateLocalAddons')


def doEPGUpdate(url, path, zipfile, epgupdate):
    import download
    import extract

    DialogOK('A TV Portal "Live Update" is available.', 'EPG Update %s will be downloaded and installed on your system.' % (epgupdate), 'Thank you.')
    
    download.download(url, zipfile)
    extract.all(zipfile, path, dp='Installing python update')
    sfile.remove(zipfile)
    Log('EPG Update %s installed' % str(epgupdate))
    xbmc.executebuiltin('UpdateLocalAddons')
