import xbmc
import xbmcaddon
import xbmcgui
import os
import sys

updateicon  = xbmc.translatePath('special://home/addons/script.trtv/resources/update.png')
temp_file   = xbmc.translatePath('special://profile/addon_data/script.trtv/update_in_progress')
ini_file    = xbmc.translatePath('special://profile/addon_data/script.trtv/addons.ini')
ini_date    = 0
cont        = 0
dp          = xbmcgui.DialogProgress()

# Check if the addons.ini.creator addon is installed
try:
    addonid   = xbmcaddon.Addon(id='plugin.video.addons.ini.creator')
    addonname = addonid.getAddonInfo('name')
    addonid.setSetting('addons.file','addons.ini')
    addonid.setSetting('addons.folder','special://home/userdata/addon_data/script.trtv/')
    cont = 1
except:
    xbmc.log('Addons ini creator not installed, cancelling update process')

if cont:
    isplaying = xbmc.Player().isPlaying()

# Make sure the system isn't playing any videos
    while isplaying:
        xbmc.sleep(60000)
        isplaying = xbmc.Player().isPlaying()

# Get last modified date of addons.ini file
    if os.path.exists(ini_file):
        ini_date = os.path.getmtime(ini_file)
    xbmc.log('### CURRENT INI DATE: %s' % ini_date)

# Check whether this is being set off as service or normally, we don't want the annoying popup displaying every 12 hours.
    loadtype = 'normal'
    if len(sys.argv) > 1:
        loadtype = sys.argv[1]
        xbmc.log('### SYS.ARGV[1] == %s' % sys.argv[1])
    if loadtype != 'full':
        xbmc.executebuiltin("XBMC.Notification(Updating TV Links,New links may not appear for up to 10 mins,10000,"+updateicon+")")

    xbmc.executebuiltin('ActivateWindow(10025,"plugin://plugin.video.addons.ini.creator/update",return)')
    xbmc.sleep(5000)
    xbmc.executebuiltin('ActivateWindow(HOME)')