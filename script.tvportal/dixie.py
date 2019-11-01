#
#      Copyright (C) 2014 Richard Dean
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

import os

import requests.packages.urllib3
import xbmc
import xbmcaddon
import xbmcgui

requests.packages.urllib3.disable_warnings()

import pickle
import datetime

import sfile

ADDONID = 'script.tvportal'
ADDON = xbmcaddon.Addon(ADDONID)
ADDON_DATA = xbmc.translatePath(os.path.join('special://profile/addon_data/'))
HOME = ADDON.getAddonInfo('path')
ICON = os.path.join(HOME, 'icon.png')
ICON = xbmc.translatePath(ICON)
PROFILE = xbmc.translatePath(ADDON.getAddonInfo('profile'))
RESOURCES = os.path.join(HOME, 'resources')
PVRACTIVE = (xbmc.getCondVisibility('Pvr.HasTVChannels')) or (xbmc.getCondVisibility('Pvr.HasRadioChannels')) == True

showSFchannels = ADDON.getSetting('showSFchannels')
SF_CHANNELS = ADDON.getSetting('SF_CHANNELS')
debug = ADDON.getSetting('DEBUG')
chanxmlfile = os.path.join(ADDON_DATA, ADDONID, 'chan.xml')
catsxmlfile = os.path.join(ADDON_DATA, ADDONID, 'cats.xml')


def SetSetting(param, value):
    value = str(value)

    if GetSetting(param) == value:
        return

    xbmcaddon.Addon(ADDONID).setSetting(param, value)


def GetSetting(param):
    return xbmcaddon.Addon(ADDONID).getSetting(param)


def GetXBMCVersion():
    version = xbmcaddon.Addon('xbmc.addon').getAddonInfo('version')
    version = version.split('.')
    return int(version[0]), int(version[1])  # major, minor eg, 13.9.902


MAJOR, MINOR = GetXBMCVersion()
FRODO = (MAJOR == 12) and (MINOR < 9)

DIXIELOGOS = GetSetting('dixie.logo.folder')
SKIN = GetSetting('dixie.skin')
FILMON = GetSetting('FILMON')
VERSION = ADDON.getAddonInfo('version')
TITLE = 'TV Portal'
LOGOPACK = 'Colour Logo Pack'
DEBUG = GetSetting('DEBUG') == 'true'
KEYMAP_HOT = 'ottv_hot.xml'
ADULT = 'Adultos'

datapath = xbmc.translatePath(ADDON.getAddonInfo('profile'))
extras = os.path.join(datapath, 'extras')
logos = os.path.join(extras, 'logos')
cookiepath = os.path.join(datapath, 'cookies')
cookiefile = os.path.join(cookiepath, 'cookie')


def log(text):
    try:
        output = '%s V%s : %s' % (TITLE, VERSION, str(text))
        if DEBUG:
            xbmc.log(output)
        else:
            xbmc.log(output, xbmc.LOGDEBUG)
    except:
        pass


def getCategories():
    return GetSetting('categories').split('|')


def CloseBusy():
    try:
        xbmc.executebuiltin('Dialog.Close(busydialog)')
    except:
        pass


def ShowBusy():
    try:
        xbmc.executebuiltin('ActivateWindow(busydialog)')
    except:
        pass

    return None


def notify(message, length=5000):
    # CloseBusy()
    cmd = 'XBMC.notification(%s,%s,%d,%s)' % (TITLE, message, length, ICON)
    xbmc.executebuiltin(cmd)


def loadKepmap():
    try:
        file = 'zOTT_Keymap.xml'
        src = os.path.join(HOME, 'resources', file)
        dst = os.path.join('special://profile/keymaps', file)

        if not sfile.exists(dst):
            sfile.copy(src, dst)
            xbmc.sleep(1000)

        xbmc.executebuiltin('Action(reloadkeymaps)')
    except Exception, e:
        pass


def removeKepmap():
    try:
        file = 'zOTT_Keymap.xml'
        dst = os.path.join('special://profile/keymaps', file)

        if sfile.exists(dst):
            sfile.remove(dst)
            xbmc.sleep(1000)

        xbmc.executebuiltin('Action(reloadkeymaps)')
    except Exception, e:
        pass


def patchSkins():
    skinPath = os.path.join(extras, 'skins')

    srcImage = os.path.join(RESOURCES, 'changer.png')
    srcFile = os.path.join(RESOURCES, 'script-tvguide-changer.xml')

    current, dirs, files = sfile.walk(skinPath)

    for dir in dirs:
        dstImage = os.path.join(current, dir, 'resources', 'skins', 'Default', 'media', 'changer.png')
        dstFile = os.path.join(current, dir, 'resources', 'skins', 'Default', '720p', 'script-tvguide-changer.xml')

        sfile.copy(srcImage, dstImage, overWrite=False)
        sfile.copy(srcFile, dstFile, overWrite=False)


def WriteKeymap(start, end):
    dest = os.path.join('special://profile/keymaps', KEYMAP_HOT)
    cmd = '<keymap><Global><keyboard><%s>XBMC.RunScript(special://home/addons/script.tvportal/osd.py)</%s></keyboard></Global></keymap>' % (
    start, end)

    f = sfile.file(dest, 'w')
    f.write(cmd)
    f.close()
    xbmc.sleep(1000)

    tries = 4
    while not sfile.exists(dest) and tries > 0:
        tries -= 1
        f = sfile.file(dest, 'w')
        f.write(cmd)
        f.close()
        xbmc.sleep(1000)

    return True


def GetDixieUrl():
    return baseurl + 'all/'


def GetKey():
    return 'ALL CHANNELS'


def GetExtraUrl():
    return resource


def GetLoginUrl():
    return loginurl


def GetVerifyUrl():
    return verifyurl


def GetChannelType():
    return GetSetting('chan.type')


def GetChannelFolder():
    CUSTOM = '1'

    channelType = GetChannelType()

    if channelType == CUSTOM:
        path = GetSetting('user.chan.folder')
        MigrateChannels(path)
    else:
        path = datapath

    return path


def GetGMTOffset():
    gmt = GetSetting('gmtfrom').replace('GMT', '')

    if gmt == '':
        offset = 0
    else:
        offset = int(gmt)

    #    offset = 0
    return datetime.timedelta(hours=offset)


def saveCookies(requests_cookiejar, filename):
    if not os.path.isfile(cookiefile):
        try:
            os.makedirs(cookiepath)
        except:
            pass

    with open(cookiefile, 'wb') as f:
        pickle.dump(requests_cookiejar, f)


def loadCookies(filename):
    if not os.path.isfile(cookiefile):
        try:
            os.makedirs(cookiepath)
        except:
            pass

        open(cookiefile, 'a').close()

    try:
        with open(cookiefile, 'rb') as f:
            return pickle.load(f)
    except:
        pass

    return ''


def resetCookies():
    try:
        if os.path.isfile(cookiefile):
            os.remove(cookiefile)
    except:
        pass


def BackupChannels():
    datapath = GetChannelFolder()

    src = os.path.join(datapath, 'channels')
    dst = os.path.join(datapath, 'channels-backup')

    try:
        sfile.rmtree(dst)
    except:
        pass

    try:
        sfile.copytree(src, dst)
    except:
        pass


def MigrateChannels(dst):
    dst = os.path.join(dst, 'channels')
    src = os.path.join(datapath, 'channels')

    if not sfile.exists(dst):
        try:
            sfile.copytree(src, dst)
        except:
            pass


def ShowSettings():
    ADDON.openSettings()


def getPreviousTime(setting):
    try:
        time_object = GetSetting(setting)
        previousTime = parseTime(time_object)

        return previousTime

    except:
        time_object = '2001-01-01 00:00:00'
        previousTime = parseTime(time_object)

        return previousTime


def parseTime(when):
    if type(when) in [str, unicode]:
        dt = when.split(' ')
        d = dt[0]
        t = dt[1]
        ds = d.split('-')
        ts = t.split(':')
        when = datetime.datetime(int(ds[0]), int(ds[1]), int(ds[2]), int(ts[0]), int(ts[1]), int(ts[2].split('.')[0]))

    return when


def validTime(setting, maxAge):
    previousTime = getPreviousTime(setting)
    now = datetime.datetime.today()
    delta = now - previousTime
    nSeconds = (delta.days * 86400) + delta.seconds

    return nSeconds <= maxAge


def validToRun(silent=False):
    setting = 'LOGIN_TIME'
    previousTime = getPreviousTime(setting)
    now = datetime.datetime.today()
    delta = now - previousTime
    nSeconds = (delta.days * 86400) + delta.seconds

    if nSeconds > 45 * 60:
        if not doLogin(silent):
            return False

        SetSetting('LOGIN_TIME', str(now))

    return True


def GetUser():
    username = GetSetting('username')
    return username


def GetPass():
    password = GetSetting('password')
    return password


def GetCats():
    path = os.path.join(PROFILE, 'cats.xml')


def GetChannels():
    path = os.path.join(PROFILE, 'chan.xml')

    return path


def DialogOK(line1, line2='', line3=''):
    d = xbmcgui.Dialog()
    d.ok(TITLE + ' - ' + VERSION, line1, line2, line3)


def DialogKB(value='', heading=''):
    kb = xbmc.Keyboard('', '')
    kb.setHeading(heading)
    kb.doModal()
    if (kb.isConfirmed()):
        value = kb.getText()
    return value


def DialogYesNo(line1, line2='', line3='', noLabel=None, yesLabel=None):
    d = xbmcgui.Dialog()
    if noLabel == None or yesLabel == None:
        return d.yesno(TITLE + ' - ' + VERSION, line1, line2, line3) == True
    else:
        return d.yesno(TITLE + ' - ' + VERSION, line1, line2, line3, noLabel, yesLabel) == True


def Progress(line1='', line2='', line3='', hide=False):
    dp = xbmcgui.DialogProgress()
    dp.create(TITLE, line1, line2, line3)
    dp.update(0)

    if hide:
        try:
            xbmc.sleep(250)
            WINDOW_PROGRESS = xbmcgui.Window(10101)
            CANCEL_BUTTON = WINDOW_PROGRESS.getControl(10)
            CANCEL_BUTTON.setVisible(False)
        except:
            pass

    return dp


def openSettings(focus=None):
    addonID = ADDONID
    if not focus:
        return xbmcaddon.Addon(addonID).openSettings()

    try:
        xbmc.executebuiltin('Addon.OpenSettings(%s)' % addonID)

        value1, value2 = str(focus).split('.')

        if FRODO:
            xbmc.executebuiltin('SetFocus(%d)' % (int(value1) + 200))
            xbmc.executebuiltin('SetFocus(%d)' % (int(value2) + 100))
        else:
            xbmc.executebuiltin('SetFocus(%d)' % (int(value1) + 100))
            xbmc.executebuiltin('SetFocus(%d)' % (int(value2) + 200))

    except Exception, e:
        print str(e)
        return


def Create_New_Channels(channelarray):
    # Read main chan.xml into memory so we can add any new channels
    if debug == 'true':
        log('New Channels being added: ' + str(channelarray))
    if not os.path.exists(chanxmlfile):
        writefile = open(chanxmlfile, 'w+')
        writefile.write('<?xml version="1.0" encoding="UTF-8"?>\n<tv>\n</tv>\n')
        writefile.close()

    if not os.path.exists(catsxmlfile):
        writefile = open(catsxmlfile, 'w+')
        writefile.write('<?xml version="1.0" encoding="UTF-8"?>\n<Document>\n</Document>\n')
        writefile.close()

    chanxml = open(chanxmlfile, 'r')
    content = chanxml.read()
    chanxml.close()

    writefile = open(chanxmlfile, 'w+')
    replacefile = content.replace('</tv>', '')
    writefile.write(replacefile)
    writefile.close()
    writefile = open(chanxmlfile, 'a')

    # Read cats.xml into memory so we can add any new channels
    catsxml = open(os.path.join(ADDON_DATA, ADDONID, 'cats.xml'), 'r')
    content2 = catsxml.read()
    catsxml.close()

    writefile2 = open(os.path.join(ADDON_DATA, ADDONID, 'cats.xml'), 'w+')
    replacefile = content2.replace('</Document>', '')
    writefile2.write(replacefile)
    writefile2.close()
    writefile2 = open(os.path.join(ADDON_DATA, ADDONID, 'cats.xml'), 'a')

    # Set a temporary list matching channel id with real name
    log("Adding channels to channel chan.xml and cats.xml")
    for channel in channelarray:
        # Add channel to chan.xml file
        channel = channel.replace('&', '&amp;').replace('_', ' ')
        if not '<channel id="' + str(channel) + '">' in content:
            writefile.write(
                '  <channel id="' + channel + '">\n    <display-name lang="en">' + channel + '</display-name>\n  </channel>\n')
        # Add channel to cats.xml file
        if not '<channel>' + str(channel) + '</channel>' in content2:
            writefile2.write(
                ' <cats>\n    <category>Uncategorised</category>\n    <channel>' + channel + '</channel>\n </cats>\n')

    writefile.write('</tv>')
    writefile.close()
    writefile2.write('</Document>')
    writefile2.close()
    try:
        os.remove(os.path.join(ADDON_DATA, ADDONID, 'settings.cfg'))
    except:
        log("No settings.cfg file to remove")


def SF_Folder_Count(foldermode):
    channelFolder = GetChannelFolder()
    channelPath = os.path.join(channelFolder, 'channels')
    channels = []
    channelarray = []
    SFchannelarray = []

    try:
        current, dirs, files = sfile.walk(channelPath)
    except Exception, e:
        log('Error in getAllChannels - Master List: %s' % str(e))
        return channels

    for file in files:
        try:
            channels.append(file)
        except:
            log("failed to add to array: " + file)

    if showSFchannels == 'false':
        return channels

    elif showSFchannels == 'true':
        try:
            current, dirs, files = sfile.walk(SF_CHANNELS)
        except Exception, e:
            log('Error in getAllChannels - SF List: %s' % str(e))
            return SFchannelarray

        # Grab a list of SF folders not in the channels folder and add as dummy channels
        for dir in dirs:
            try:
                if os.path.exists(os.path.join(SF_CHANNELS, dir, 'favourites.xml')):
                    SFchannelarray.append(dir)
                    if not dir in channels:
                        channelarray.append(dir)
            except:
                log("Special characters in directory, skipping: " + dir)

        if debug == 'true':
            log("FINAL CHANNELARRAY:")
            log(str(SFchannelarray))

        # Add dummy channels to chan.xml and cats.xml
        if len(channelarray) > 0 and foldermode == 'create':
            Create_New_Channels(channelarray)
        # Final return of SF channels only
        return SFchannelarray
