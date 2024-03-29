
#       Copyright (C) 2013-2014
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

import urllib
import urllib2
import random
import re
import os

import xbmc
import xbmcaddon
import xbmcplugin
import xbmcgui

import cache
import yt

import utils as utils
import categories
    
ADDONID    = utils.ADDONID
ADDON      = utils.ADDON
HOME       = utils.HOME
PROFILE    = utils.PROFILE
TITLE      = utils.TITLE
VERSION    = utils.VERSION
ICON       = utils.ICON
FANART     = utils.FANART
ADDONS     = xbmc.translatePath('special://home/addons')
PACKAGES   = os.path.join(ADDONS,'packages')

SUPERFAVES   = 'plugin.program.super.favourites'
SF_INSTALLED = xbmc.getCondVisibility('System.HasAddon(%s)' % SUPERFAVES) == 1
SFFILE       = ''

TOOLS = 'script.tvportal.tools'
try:
    import sys
    sfAddon = xbmcaddon.Addon(id = SUPERFAVES)
    sfPath  = sfAddon.getAddonInfo('path')
    sys.path.insert(0, sfPath)

    import chooser
    import favourite

    SFFILE = os.path.join(PROFILE, 'favourites.xml')
except:
    SF_INSTALLED = False


IMAGES = os.path.join(HOME, 'resources', 'images')

AUTOSTREAM      = utils.getSetting('AUTOSTREAM') == 'true'
KIOSKMODE       = utils.getSetting('KIOSKMODE')  == 'true'
showaddons      = ADDON.getSetting('showaddons')
showbuilds      = ADDON.getSetting('showbuilds')
showdownloads   = ADDON.getSetting('showdownloads')
showhardware    = ADDON.getSetting('showhardware')
showtutorials   = ADDON.getSetting('showtutorials')
showepg         = ADDON.getSetting('showepg')
showkeywords    = ADDON.getSetting('showkeywords')
showmaintenance = ADDON.getSetting('showmaintenance')
showtv          = ADDON.getSetting('showtv')
showmovies      = ADDON.getSetting('showmovies')
showsearch      = ADDON.getSetting('showsearch')
showfaves       = ADDON.getSetting('showfaves')

GETTEXT = utils.GETTEXT


global APPLICATION


_SCRIPT          = 100
_ADDON           = 200
_SETTINGS        = 300
_YOUTUBE         = 400
_CATCHUP         = 500
_TVSHOWS         = 600
_MOVIES          = 700
_SHOWSHORTCUTS   = 800
_ADDSHORTCUT     = 900
_VPNICITY        = 1000
_SUPERSEARCH     = 1100
_REMOVESHORTCUT  = 1200
_TOOLS           = 1300
_LIBRARY         = 1400
_SUPERFAVE       = 1500
_REMOVESUPERFAVE = 1600

_CATEGORIES     = 2000
_SETTINS        = 2001
_CHANNELS       = 2002
_SKINS          = 2003
_LOGOS          = 2004
_INI            = 2005
_VPN            = 2006
_ADDONS         = 2007
_ADDONS_POPULAR = 2008
_COMMUNITY_BUILDS= 2009

WINDOWID = 10005 #music


categoriesList = categories.getSetting('categories').split('|')
if categoriesList[0] == '':
    categoriesList = []


def Capitalize(text):
    if len(text) == 0:
        return text

    if len(text) == 1:
        return text.capitalize()

    return text[0].capitalize() + text[1:]


def Main():
#    if AUTOSTREAM:
#        if xbmc.getCondVisibility('Player.HasVideo') <> 1:
#            url = xbmcaddon.Addon('script.tvportal.epg').getSetting('streamURL')
#            if len(url) > 0:
#                PlayMedia(url)

#    if showaddons=='true':
#        AddAddon('Add-ons',   'ActivateWindow(10001,"plugin://plugin.program.totalinstaller/?url=popular";,return)', _SUPERFAVE,  icon=os.path.join(IMAGES, 'Addons.png'))
    if showaddons=='true':
        AddAddon('Add-ons',   'script.addon.portal', _SCRIPT,  icon=os.path.join(IMAGES, 'TV_Guide.png'))#    if showbuilds=='true':
    if showbuilds=='true':
        AddAddon('Community Builds',   'script.community.builds', _SCRIPT,  icon=os.path.join(IMAGES, 'TV_Guide.png'))#    if showbuilds=='true':
    if showdownloads=='true':
        AddAddon('Downloads',   'script.downloads', _SCRIPT,  icon=os.path.join(IMAGES, 'TV_Guide.png'))#    if showbuilds=='true':
    if showhardware=='true':
        AddAddon('Hardware Reviews',   'script.hardware', _SCRIPT,  icon=os.path.join(IMAGES, 'TV_Guide.png'))#    if showbuilds=='true':
    if showkeywords=='true':
        AddAddon('Keyword Installer',   'script.keywords', _SCRIPT,  icon=os.path.join(IMAGES, 'TV_Guide.png'))#    if showbuilds=='true':
    if showtutorials=='true':
        AddAddon('Tutorials',   'script.tutorials', _SCRIPT,  icon=os.path.join(IMAGES, 'TV_Guide.png'))#    if showbuilds=='true':
    if showepg=='true':
        AddAddon('TV Guide',   'script.tvportal.epg', _SCRIPT,  icon=os.path.join(IMAGES, 'TV_Guide.png'))
    if showmaintenance=='true':
        AddAddon('Maintenance',   'script.maintenance', _SCRIPT,  icon=os.path.join(IMAGES, 'TV_Guide.png'))
    if showtv=='true':
        AddLibrary('TV Shows', '',  _TVSHOWS, icon=os.path.join(IMAGES, 'TV_Shows.png'))
    if showmovies=='true':
        AddLibrary('Movies',   '',  _MOVIES,  icon=os.path.join(IMAGES, 'Movies.png'))
    if showsearch=='true':
        AddAddon('Search',     SUPERFAVES, _SUPERSEARCH, icon=os.path.join(IMAGES, 'Search.png'), desc='Search all your favourite addons all from one place')
    if showfaves=='true':
        AddAddon('Favourites', SUPERFAVES, _ADDON,       icon=os.path.join(IMAGES, 'Favourites.png'))

#    AddAddon('Maintenance',   'plugin.program.totalinstaller', _ADDON,  icon=os.path.join(IMAGES, 'Maintenance.png'))
#    AddSubFolder('Addons',   _ADDONS,  icon=os.path.join(IMAGES, 'TV_Guide.png'), desc='Install any add-on ever made from the worlds largest Kodi library - The Add-on Portal @ www.noobsandnerds.com')
#    AddSubFolder('Community Builds',   _COMMUNITY_BUILDS,  icon=os.path.join(IMAGES, 'Community_Builds.png'), desc='Install builds from the Community Builds Portal @ www.noobsandnerds.com')
#    AddSubFolder('Community Builds',   'plugin.program.totalinstaller', _ADDON,  icon=os.path.join(IMAGES, 'Addons.png'))
#    AddSubFolder('TV Catch Up', _CATCHUP, icon=os.path.join(IMAGES, 'TV_Catchup.png'), desc='Catch up on shows you have missed')


    # AddSubFolder('System',      _SYSTEM,  icon=os.path.join(IMAGES, 'System.png'),  desc='Settings and Tools')

    if not KIOSKMODE:
        ShowShortcuts()
        ShowSFShortcuts()
        icon = os.path.join(IMAGES, 'Shortcuts.png')
        AddDir('Add/Remove...', '', _ADDSHORTCUT, iconimage=icon, description='Browse and select other shortcuts', isFolder=False, isPlayable=False)
#        AddDir('Remove...', '', _REMOVEADDONSHORTCUT, iconimage=icon, description='Browse and select other shortcuts', isFolder=False, isPlayable=False)



def ShowCatchup():
    AddAddon('BBC iPlayer', 'plugin.video.bbciplayer', _ADDON, icon=os.path.join(IMAGES, 'BBC_iPlayer.png'))
    AddAddon('ITV Player',  'plugin.video.itv',        _ADDON, icon=os.path.join(IMAGES, 'ITV_Player.png'))
    AddAddon('UKTV Play',   'plugin.video.uktvplay',   _ADDON, icon=os.path.join(IMAGES, 'UKTV_Play.png'))


def ShowAddonsMenu():
    AddAddon('Most Popular',        'plugin.program.totalinstaller', _ADDONS_POPULAR , icon=os.path.join(IMAGES, 'Popular.png'), desc='View the top 100 most downloaded add-ons of all')
    AddAddon('Install Skins',       TOOLS,  _SKINS,    icon=os.path.join(IMAGES, 'install-skins.png'), desc='Install new skins and use them to change the EPG look and feel.')
    AddAddon('Install Logo-Packs',  TOOLS,  _LOGOS,    icon=os.path.join(IMAGES, 'install-logos.png'), desc='Install new logo-packs and use them in the EPG.')
    AddAddon('Update Add-on Links', TOOLS,  _INI,      icon=os.path.join(IMAGES, 'update-addons.png'), desc='Update the built-in Add-on links to 3rd party live TV add-ons available for Kodi.')


def ShowTools():
    AddAddon('Channels',            TOOLS,  _CHANNELS, icon=os.path.join(IMAGES, 'edit-channels.png'), desc='Edit your channels - Change logos, change visibility, change order or even add your own!')
    AddAddon('Install Skins',       TOOLS,  _SKINS,    icon=os.path.join(IMAGES, 'install-skins.png'), desc='Install new skins and use them to change the EPG look and feel.')
    AddAddon('Install Logo-Packs',  TOOLS,  _LOGOS,    icon=os.path.join(IMAGES, 'install-logos.png'), desc='Install new logo-packs and use them in the EPG.')
    AddAddon('Update Add-on Links', TOOLS,  _INI,      icon=os.path.join(IMAGES, 'update-addons.png'), desc='Update the built-in Add-on links to 3rd party live TV add-ons available for Kodi.')
    AddVPNicity()


def ShowSettings(addonID):
    xbmc.executebuiltin('Addon.OpenSettings(%s)' % addonID)


def OpenTools():
    xbmc.executebuiltin('XBMC.RunAddon(script.tvportal.tools)')

def PlayMedia(url, windowed=True):
    APPLICATION.setResolvedUrl(url, success=True, listItem=None, windowed=windowed)


def SelectSuperSearch(addonID):
    xbmc.executebuiltin('ActivateWindow(%d,"plugin://%s/?mode=%d")' % (WINDOWID, addonID, 25))

def RunAddonMode(id,addonID,mode):
    xbmc.executebuiltin('ActivateWindow(%d,"plugin://%s/?mode=%s")' % (WINDOWID, addonID, 25))

def ShowSFShortcuts():
    if not SF_INSTALLED:
        return

    faves        = favourite.getFavourites(SFFILE)
    mode         = _SUPERFAVE
    isFolder     = False
    isPlayable   = False
    replaceItems = False

    for fave in faves:
        name = fave[0]
        icon = fave[1]
        path = fave[2]

        #these currently don't work as they are removed by chooser.py :(
        fanart = favourite.getFanart(path) 
        desc   = favourite.getOption(path, 'desc')

        menu = []
        menu.append(('Remove %s Super Favourite' % (name), '?mode=%d&url=%s' % (_REMOVESUPERFAVE, urllib.quote_plus(path))))

        AddDir(name, path, mode, icon, desc, isFolder, isPlayable, fanart=fanart, contextMenu=menu, replaceItems=False)


def ShowShortcuts():
    addons = utils.getSetting('ADDONS').split('|')
    toSort = []
    
    for addon in addons:
        try:
            if addon:
                name = xbmcaddon.Addon(addon).getAddonInfo('name')
                toSort.append([Capitalize(name), addon])
        except:
            pass

    #toSort.sort()

    for addon in toSort:
        try:
            menu = []
            name = addon[0]
            url  = addon[1]
            menu.append(('Remove %s shortcut' % Capitalize(name), '?mode=%d&url=%s' % (_REMOVESHORTCUT, urllib.quote_plus(url))))
            print"### menu: "+str(menu)
            print"### name: "+name
            print"### url:  "+url
            if url.startswith('script'):
                AddAddon(name, url, _SCRIPT, contextMenu=menu)
            else:
                AddAddon(name, url, _ADDON, contextMenu=menu)
        except:
            pass


def RemoveSFShortcut(url):
    return favourite.removeFave(SFFILE, url)  


def RemoveShortcut(url):
    shortcuts = utils.getSetting('ADDONS')

    url += '|'

    if url not in shortcuts:
        return False

    update = shortcuts.replace(url,  '')

    utils.setSetting('ADDONS', update)

    return True


def AddShortcut():
    ADDMORE = int(utils.getSetting('ADDMORE'))

    if ADDMORE == 0:
        return AddAddonShortcut()

    if not SF_INSTALLED:
        return AddAddonShortcut()

    if ADDMORE == 2 and utils.DialogYesNo(GETTEXT(30313), GETTEXT(30314), '', GETTEXT(30315), GETTEXT(30316)):
        return AddAddonShortcut()

    return AddSFShortcut()


def AddSFShortcut():
    if not chooser.GetFave('TVP3'):
        return False

    path   = xbmc.getInfoLabel('Skin.String(TVP3.Path)')
    label  = xbmc.getInfoLabel('Skin.String(TVP3.Label)')
    icon   = xbmc.getInfoLabel('Skin.String(TVP3.Icon)')
    folder = xbmc.getInfoLabel('Skin.String(TVP3.IsFolder)') == 'true'

    if len(path) == 0 or path == 'noop':
        return False

    fave = [label, icon, path] 
    favourite.copyFave(SFFILE, fave)

    return True


def AddAddonShortcut():
    import glob

    path      = xbmc.translatePath(os.path.join('special://home' , 'addons', '*.*'))
    shortcuts = utils.getSetting('ADDONS').split('|')

    #don't allow sortcut to self
    shortcuts.append(ADDONID)

    names = []

    for addon in glob.glob(path):
        try:
            name = addon.lower().rsplit(os.path.sep, 1)[-1]
            if name not in shortcuts:
                realname = xbmcaddon.Addon(name).getAddonInfo('name')
                names.append([Capitalize(realname), name])
        except:
            pass

    if len(names) < 1:
        return

    names.sort()

    addons = []
    for name in names:
        addons.append(name[0])

    option = xbmcgui.Dialog().select('Select addon', addons)

    if option < 0:
        return False

    update = utils.getSetting('ADDONS') + names[option][1] + '|'

    utils.setSetting('ADDONS', update)

    return True

def RemoveAddonShortcut():
    import glob

    path      = xbmc.translatePath(os.path.join('special://home' , 'addons', '*.*'))
    shortcuts = utils.getSetting('ADDONS').split('|')

    names = []

    for addon in glob.glob(path):
        try:
            name = addon.lower().rsplit(os.path.sep, 1)[-1]
            if name in shortcuts:
                realname = xbmcaddon.Addon(name).getAddonInfo('name')
                names.append([Capitalize(realname), name])
        except:
            pass

    if len(names) < 1:
        return

    names.sort()

    addons = []
    for name in names:
        addons.append(name[0])

    option = xbmcgui.Dialog().select('Select addon to remove', addons)

    if option < 0:
        return False

    update = RemoveShortcut(names[option][1])

 #   utils.setSetting('ADDONS', update)

    return True

def AddShowShortcuts():
    icon = os.path.join(IMAGES, 'Shortcuts.png')
    AddDir('Shortcuts...', '', _SHOWSHORTCUTS, iconimage=icon, description='Custom addon shortcuts', isFolder=True, isPlayable=False)


def AddVPNicity():
    try:
        addonID    = 'plugin.program.vpnicity'
        properties = GetAddon(addonID)
        desc       = 'Select a VPN' #properties[6]
        icon       = properties[7]
        fanart     = properties[8]

        AddDir('Select VPN', addonID, _VPNICITY, icon, desc, False, fanart)
    except:
        pass


def SelectVPNicity(addonID):
    properties = GetAddon(addonID)
    script     = os.path.join(properties[1], 'manual.py')
    cmd = 'RunScript(%s)' % script
    xbmc.executebuiltin(cmd)


def PlayYT(id):
    xbmc.executebuiltin('Dialog.Show(busydialog)')

    video, links = yt.GetVideoInformation(id)

    xbmc.executebuiltin('Dialog.Close(busydialog)')

    if 'best' not in video:
        return False

    url   = video['best']          
    title = video['title']
    image = video['thumbnail']

    liz = xbmcgui.ListItem(title, iconImage=image, thumbnailImage=image)

    liz.setInfo( type="Video", infoLabels={ "Title": title} )

    windowed = utils.getSetting('PLAYBACK') == '1'

    APPLICATION.setResolvedUrl(url, success=True, listItem=liz, windowed=windowed)


def AddYT(name, id):
    video, links = yt.GetVideoInformation(id)

    url   = video['best']   
    desc  = video['title']       
    image = video['thumbnail']

    AddDir(name, id, _YOUTUBE, image, desc, False, True, image)


def GetAddon(addonID):
    addon   = xbmcaddon.Addon(addonID)
    home    = addon.getAddonInfo('path')
    profile = addon.getAddonInfo('profile')
    title   = addon.getAddonInfo('name')
    version = addon.getAddonInfo('version')
    summary = addon.getAddonInfo('summary')
    desc    = addon.getAddonInfo('description')
    icon    = os.path.join(home, 'icon.png')
    fanart  = os.path.join(home, 'fanart.jpg')

    return [addon, home, profile, title, version, summary, desc ,icon, fanart]


def AddAddon(name, addonID, mode, icon=None, fanart=None, desc=None, contextMenu=[], replaceItems=False):
    try:    properties = GetAddon(addonID)
    except: return

    if desc == None:
        desc = properties[6]

    if icon == None:
        icon = properties[7]

    if fanart == None:
        fanart = properties[8]
    
    AddDir(name, addonID, mode, icon, desc, False, False, fanart, contextMenu, replaceItems)


def AddonMode(name, addonID, mode, icon=None, fanart=None, desc=None, contextMenu=[], replaceItems=False):
    AddDir(name, addonID, mode, icon, desc, False, False, fanart, contextMenu, replaceItems)

def AddSubFolder(name, mode, icon=None, fanart=None, desc=''):
    if icon == None:
        icon = ICON

    if fanart == None:
        fanart = FANART

    AddDir(name, '', mode, icon, desc, True, False, fanart)


def AddLibrary(name, windowID, mode, icon=None, fanart=None, desc=''):
    if icon == None:
        icon = ICON
    
    if fanart == None:
        fanart = FANART
    
    AddDir(name, '', mode, icon, '', '', '', fanart)


def ShowCategories(categoriesList):
    d = categories.CategoriesMenu(categoriesList)
    d.doModal()
    categoriesList = d.currentCategories
    del d
    
    categories.setSetting('categories', '|'.join(categoriesList))


def AddShowCategories():
    icon = os.path.join(IMAGES, 'Categories.png')
    fanart = FANART

    AddDir('Categories', '', _CATEGORIES, icon, 'Edit which TV Portal Categories are displayed in the TV Guide', '', '', fanart)


def AddDir(name, url, mode, iconimage, description, isFolder, isPlayable, fanart='', contextMenu=[], replaceItems=False):
    u  = ''
    u += "?url="         + urllib.quote_plus(url)
    u += "&mode="        + str(mode)
    u += "&name="        + urllib.quote_plus(name)
    u += "&iconimage="   + urllib.quote_plus(iconimage)
    u += "&description=" + urllib.quote_plus(description)
    u += "&fanart="      + urllib.quote_plus(fanart)

    infoLabels = {'title':name, 'fanart':fanart, 'description':description, 'thumb':iconimage}

    APPLICATION.addDir(name, mode, u, iconimage, isFolder=isFolder, isPlayable=isPlayable, infoLabels=infoLabels, contextMenu=contextMenu, replaceItems=replaceItems)


def get_params(params):
    if not params:
        return {}

    param = {}

    cleanedparams = params.replace('?','')

    if (params[len(params)-1] == '/'):
       params = params[0:len(params)-2]

    pairsofparams = cleanedparams.split('&')    

    for i in range(len(pairsofparams)):
        splitparams = pairsofparams[i].split('=')

        if len(splitparams) == 2:
            param[splitparams[0]] = splitparams[1]

    return param

    
def onBack(application, _params):
    pass

    
def onParams(application, _params):
    global APPLICATION
    APPLICATION = application

    params = get_params(_params)
    mode   = None

    try:    mode = int(urllib.unquote_plus(params['mode']))
    except: pass

    try:    url = urllib.unquote_plus(params['url'])
    except: url = None
    

    if mode == _SCRIPT:
        cmd = 'RunScript(%s)' % url
        xbmc.executebuiltin(cmd)
    elif mode == _ADDON:
        xbmc.executebuiltin('ActivateWindow(%d,"plugin://%s/",return)' % (WINDOWID, url))
    elif mode == _SUPERFAVE:
        xbmc.executebuiltin(url)
    elif mode == _REMOVESUPERFAVE:
        if RemoveSFShortcut(url):
            APPLICATION.containerRefresh()
    elif mode == _MOVIES:
        if utils.getSetting('KodiLib') == 'true':
            sfmovies = xbmc.translatePath('special://profile/addon_data/plugin.program.super.favourites/Super Favourites/Movies')
            if not os.path.exists(sfmovies):
                try:
                    os.makedirs(sfmovies)
                except:
                    pass
            xbmc.executebuiltin('ActivateWindow(10001,plugin://plugin.program.super.favourites/?label=Movies&mode=400&path=special://profile/addon_data/plugin.program.super.favourites/Super Favourites/Movies,return)')
        else:
            xbmc.executebuiltin('ActivateWindow(10025,videodb://1/2,return)')
    elif mode == _TVSHOWS:
        if utils.getSetting('KodiLib') == 'true':
            sftvshows = xbmc.translatePath('special://profile/addon_data/plugin.program.super.favourites/Super Favourites/TV Shows')
            if not os.path.exists(sftvshows):
                try:
                    os.makedirs(sftvshows)
                except:
                    pass
            xbmc.executebuiltin('ActivateWindow(10001,plugin://plugin.program.super.favourites/?label=TV Shows&mode=400&path=special://profile/addon_data/plugin.program.super.favourites/Super Favourites/TV Shows,return)')
        else:
            xbmc.executebuiltin('ActivateWindow(10025,videodb://2/2,return)')
    elif mode == _CATEGORIES:
        ShowCategories(categoriesList)
    elif mode == _SETTINGS:
        ShowSettings()
    elif mode == _INI:
        cmd = 'XBMC.RunScript(special://home/addons/script.tvportal.epg/getIni.py)'
        xbmc.executebuiltin(cmd)
    elif mode == _ADDONS_POPULAR:
        xbmc.executebuiltin('ActivateWindow(10001,plugin://plugin.program.totalinstaller/?mode=addonmenu,return)')
        #put while folder is the CP addons folder sleep 500
        path = str(xbmc.getInfoLabel('ListItem.FolderPath'))
        while 'addon' in path:
            xbmc.sleep(500)
            path = str(xbmc.getInfoLabel('ListItem.FolderPath'))
        xbmc.executebuiltin('RunScript(special://home/addons/script.community.portal/?mode=_ADDONS_POPULAR)')# % (WINDOWID, url, 'addonsmenu'))
    elif mode == _CHANNELS:
        xbmc.executebuiltin('ActivateWindow(%d,"plugin://%s/?mode=%d")' % (WINDOWID, TOOLS, 1900))
    elif mode == _SKINS:
        xbmc.executebuiltin('ActivateWindow(%d,"plugin://%s/?mode=%d")' % (WINDOWID, TOOLS, 2000))
    elif mode == _LOGOS:
        xbmc.executebuiltin('ActivateWindow(%d,"plugin://%s/?mode=%d")' % (WINDOWID, TOOLS, 2100))
    elif mode == _TOOLS:
        ShowTools()
    elif mode == _YOUTUBE:
        PlayYT(url)
    elif mode == _VPNICITY:
        SelectVPNicity(url)
    elif mode == _CATCHUP:
        ShowCatchup() 
    elif mode == _COMMUNITY_BUILDS:
        communitybuildpath = xbmc.translatePath('special://home/addons/script.community.builds')
        if os.path.exists(communitybuildpath):
            xbmc.executebuiltin('RunScript(special://home/addons/script.community.builds/default.py)')
        else:
            choice = utils.DialogYesNo('Add-on Required','You need the Community Builds module installed to access this section. Would you like to install now?')
            if choice == 1:
                print"download function required"
                try:
                    download.download('http://github.com/noobsandnerds/zips/script.community.builds/script.community.builds.zip', os.path.join(PACKAGES,'update.zip'))
                    extract.all(os.path.join(PACKAGES,'update.zip'), ADDONS)
                except:
                    print"### Failed to download and extract Community Builds add-on"
#        ShowAddonsMenu() 
    elif mode == _ADDONS:
        addonportalpath = xbmc.translatePath('special://home/addons/script.addon.portal')
        if os.path.exists(addonportalpath):
            xbmc.executebuiltin('RunScript(special://home/addons/script.addon.portal/default.py)')
        else:
            choice = utils.DialogYesNo('Add-on Required','You need the Add-on Portal module installed to access this section. Would you like to install now?')
            if choice == 1:
                print"download function required"
                try:
                    download.download('http://github.com/noobsandnerds/zips/script.addon.portal/script.addon.portal.zip', os.path.join(PACKAGES,'update.zip'))
                    extract.all(os.path.join(PACKAGES,'update.zip'), ADDONS)
                except:
                    print"### Failed to download and extract Addon Portal"
    elif mode == _SUPERSEARCH:
        SelectSuperSearch(url)
    elif mode == _SHOWSHORTCUTS:
        ShowShortcuts()
    elif mode == _ADDSHORTCUT:
        if AddShortcut():
            APPLICATION.containerRefresh()
    elif mode == _REMOVESHORTCUT:
        if RemoveShortcut(url):
            APPLICATION.containerRefresh()

#    elif mode == _REMOVEADDONSHORTCUT:
#        RemoveAddonShortcut()
        
    else:
        Main()