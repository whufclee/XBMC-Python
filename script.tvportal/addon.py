# TV Portal EPG Launcher
# Copyright (C) 2016 Lee Randall (whufclee)
#

#  I M P O R T A N T :

#  You are free to use this code under the rules set out in the license below.
#  Should you wish to re-use this code please credit whufclee for the original work.
#  However under NO circumstances should you remove this license!

#  GPL:
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
#  along with this Program; see the file LICENSE.txt.  If not, write to
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#  http://www.gnu.org/copyleft/gpl.html

import os
import xbmc
import xbmcaddon
import xbmcgui

import dixie
import shutil

AddonID = 'script.tvportal'
ADDON = xbmcaddon.Addon(id=AddonID)
SFADDON = xbmcaddon.Addon(id='plugin.program.super.favourites')
showSFchannels = ADDON.getSetting('showSFchannels')
usenanchan = ADDON.getSetting('usenanchan')
usenancats = ADDON.getSetting('usenancats')
username = ADDON.getSetting('username')
password = ADDON.getSetting('password')
uselogin = ADDON.getSetting('login')
sf_channels = ADDON.getSetting('SF_CHANNELS')
showSFchannels = ADDON.getSetting('showSFchannels')
add_sf_items = ADDON.getSetting('add_sf_items')
sf_metalliq = ADDON.getSetting('SF_METALLIQ')
firstrun = ADDON.getSetting('FIRSTRUN')
update_folders = ADDON.getSetting('update_folders')
enable_players = ADDON.getSetting('enable_players')
usecatchup = ADDON.getSetting('usecatchup')
sf_folder = SFADDON.getSetting('FOLDER')
USERDATA = xbmc.translatePath(os.path.join('special://home/userdata', ''))
ADDON_DATA = xbmc.translatePath(os.path.join(USERDATA, 'addon_data'))
ADDONS = xbmc.translatePath('special://home/addons')
resources = dixie.RESOURCES
cookies = os.path.join(ADDON_DATA, AddonID, 'cookies')
datapath = dixie.PROFILE
extras = os.path.join(datapath, 'extras')
logopack_none = os.path.join(extras, 'logos', 'None')
logopack_colour = os.path.join(extras, 'logos', 'Colour Logo Pack')
channel_xml = os.path.join(resources, 'chan.xml')
xmlmaster = os.path.join(resources, 'chan.xml')
catsmaster = os.path.join(resources, 'cats.xml')
chanxml = os.path.join(datapath, 'chan.xml')
catsxml = os.path.join(datapath, 'cats.xml')
dialog = xbmcgui.Dialog()
cont = 0
#########################################################################################
if not os.path.exists(os.path.join(ADDON_DATA, AddonID)):
    dixie.log("New addon_data folder created")
    os.makedirs(os.path.join(ADDON_DATA, AddonID))
else:
    dixie.log("addon_data already exists")

if not os.path.exists(cookies):
    os.makedirs(cookies)

if not os.path.exists(logopack_none):
    os.makedirs(logopack_none)

if not os.path.exists(logopack_colour):
    os.makedirs(logopack_colour)

if not os.path.exists(chanxml) and usenanchan == 'true':
    dixie.log("Copying chan.xml to addon_data")
    shutil.copyfile(xmlmaster, chanxml)
else:
    dixie.log("Chan.xml file already exists in addon_data")

if sf_channels == '' and (
            sf_metalliq == 'true' or add_sf_items == 'true' or showSFchannels == 'true') and firstrun == 'false':
    if dialog.yesno('Super Folder Setup',
                    'Your Super Folders have not yet been setup, would you like to do so now? If you choose no you can always set it up manually later.'):
        if sf_folder == '':
            sf_folder = xbmc.translatePath('special://profile/addon_data/plugin.program.super.favourites')
        elif not os.path.exists(xbmc.translatePath(sf_folder)):
            dialog.ok('Invalid location',
                      'The location you have setup in your Super Favourites add-on is not valid. Please browse to a valid folder - we recommend using the default plugin.program.super.favourites folder in addon_data.')
            sf_folder = dialog.browse(3, 'Select the new Super Favourite data path', 'files', '', False, False)
        SFADDON.setSetting('FOLDER', sf_folder)
        SFADDON.setSetting('SHOWUNAVAIL', 'true')
        SFADDON.setSetting('SHOWNEW', 'false')
        SFADDON.setSetting('SHOWXBMC', 'false')
        SFADDON.setSetting('SHOWSEP', 'false')
        SFADDON.setSetting('ALPHA_SORT', 'true')
        default_path = os.path.join(sf_folder, 'Super Favourites', 'HOME_LIVE_TV')
        try:
            os.makedirs(default_path)
            ADDON.setSetting('SF_CHANNELS', default_path)
            ADDON.setSetting('FIRSTRUN', 'true')
        except:
            dialog.ok('Error creating folders',
                      'Sorry there was an error trying to create folders in the path specified. Please make sure you have write access to the path.')
    else:
        ADDON.setSetting('FIRSTRUN', 'true')

if firstrun == 'false' and usecatchup == 'true':
    dialog.ok('CATCHUP ENABLED',
              'To be able to use the catchup option you\'ll need certain third party add-ons installed. Please check the MetalliQ support thread at noobsandnerds.com for details of supported add-ons.')

if not os.path.exists(catsxml) and usenancats == 'true':
    dixie.log("Copying cats.xml to addon_data")
    shutil.copyfile(catsmaster, catsxml)
else:
    dixie.log("Cats.xml file exists in addon_data")

if uselogin == 'true' and (password == '' or username == ''):
    dialog.ok('ENTER LOGIN CREDENTIALS',
              'You have the login option enabled in settings but have not entered your credentials. If you aren\'t yet a member you can register for free on the forum at [COLOR=dodgerblue]noobsandnerds.com[/COLOR].')
    ADDON.openSettings()

try:
    import login

    cont = 1
    xbmc.executebuiltin("ActivateWindow(busydialog)")
except:
    xbmc.executebuiltin('ActivateWindow(Programs,addons://sources/executable)')
    xbmc.executebuiltin("Container.SetViewMode(50)")
    xbmc.sleep(2000)
    temparray = []
    listcount = xbmc.getInfoLabel('Container(id).NumItems')
    listcount = int(listcount) + 1
    counter = 0
    while counter < listcount:
        addonname = xbmc.getInfoLabel('Container(id).ListItem(%s).Label' % counter)
        temparray.append([counter, addonname])
        xbmc.log('Addon name: %s | %s' % (addonname, counter))
        counter += 1
    for item in temparray:
        if item[1] == 'TV Portal':
            pos = item[0]
            cont = 1
    xbmc.executebuiltin('Control.Move(50,%s)' % pos)
    xbmc.sleep(1000)
    if cont:
        xbmc.executebuiltin("ActivateWindow(busydialog)")
        import login

if cont:
    xbmc.executebuiltin('RunScript(special://home/addons/script.tvportal/createDB.py,normal)')
    if enable_players == 'true':
        xbmc.executebuiltin('RunPlugin(plugin://plugin.video.metalliq/settings/players/all)')
    login.User_Info()
    if update_folders == 'true':
        xbmc.executebuiltin('RunScript(special://home/addons/script.tvportal/createFolders.py,silent)')
