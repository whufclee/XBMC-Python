# -*- coding: utf-8 -*-

# plugin.program.tbs
# Total Revolution Maintenance (c) by whufclee (info@totalrevolution.tv)

# Total Revolution Maintenance is licensed under a
# Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.

# You should have received a copy of the license along with this
# work. If not, see http://creativecommons.org/licenses/by-nc-nd/4.0.

import os
import re
import sys
import time
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin

from koding     import dolog, Addon_Setting, Text_File
from default    import Sync_Settings, Adult_Filter
#---------------------------------------------------------------------------------------------------
AddonID          = 'plugin.program.tbs'
HOME             =  xbmc.translatePath('special://home/')
USERDATA         =  xbmc.translatePath('special://home/userdata')
ADDON_DATA       =  xbmc.translatePath(os.path.join(USERDATA,'addon_data'))
ADDONS           =  xbmc.translatePath(os.path.join(HOME,'addons'))
sleeper          =  os.path.join(ADDONS,AddonID,'resources','tmr')
internetcheck    =  Addon_Setting('internetcheck')
cachecheck       =  Addon_Setting('cleancache')
flashsplash      = '/flash/oemsplash.png'
newsplash        =  xbmc.translatePath('special://home/media/branding/Splash.png')
runwizard        =  os.path.join(ADDON_DATA,'script.openwindow','RUN_WIZARD')
install_complete =  os.path.join(ADDON_DATA,'script.openwindow','INSTALL_COMPLETE')
#---------------------------------------------------------------------------------------------------
dolog('### SERVICE - running sync settings')
Adult_Filter('false','startup')
Sync_Settings()
# Make sure this doesn't interfere with startup wizard
if not os.path.exists(runwizard) and os.path.exists(install_complete):
    dolog('### SERVICE - RUNWIZARD ALREADY DONE AND INSTALL COMPLETE. RUNNING UPDATE')
    if os.path.exists(xbmc.translatePath('special://home/addons/script.openwindow/functions.py')):
        xbmc.executebuiltin('RunScript(special://home/addons/script.openwindow/functions.py)')
    elif os.path.exists(xbmc.translatePath('special://xbmc/addons/script.openwindow/functions.py')):
        xbmc.executebuiltin('RunScript(special://xbmc/addons/script.openwindow/functions.py)')
   
if internetcheck == 'true':
    xbmc.executebuiltin('XBMC.AlarmClock(internetloop,XBMC.RunScript(special://home/addons/%s/connectivity.py,silent=true),00:01:00,silent,loop)'%AddonID)

if cachecheck == 'true':
    xbmc.executebuiltin('XBMC.AlarmClock(cleancacheloop,XBMC.RunScript(special://home/addons/%s/cleancache.py,silent=true),12:00:00,silent,loop)'%AddonID)

sleep = Text_File(sleeper,'r')

# Update the boot screen splash
if os.path.exists(flashsplash):
    flashsize = os.path.getsize(flashsplash)
else:
    flashsize = 0

if os.path.exists(newsplash):
    newsize = os.path.getsize(newsplash)
else:
    newsize = 0

if flashsize != newsize and newsize != 0 and flashsize != 0:
    try:
        os.system('mount -o remount,rw /flash')
        os.system('cp /storage/.kodi/media/branding/Splash.png /flash/oemsplash.png')
        os.system('cp /storage/.kodi/media/branding/Splash.png /storage/.kodi/media/Splash.png')
    except:
        pass

# Check the sleep is not set to a blank string, if it is we set to every 24hrs
if sleep == '':
    if os.path.exists(sleeper):
        Text_File(sleeper,'w','23:59:59')

# Check uploaded shares to see if any have changed locally and need reuploading
if not os.path.exists(runwizard):
    dolog('### SERVICE - Checking my shares to see if they need updating on server')
    xbmc.executebuiltin('RunScript(special://home/addons/%s/checknews.py,shares)'%AddonID)

xbmc.executebuiltin('XBMC.AlarmClock(Shareloop,XBMC.RunScript(special://home/addons/%s/checknews.py,shares),12:00:00,silent,loop)'%AddonID)
xbmc.log('### SLEEP: %s'%sleep)

# Set the main timer for regular update checks
if sleep != '':
    xbmc.executebuiltin('XBMC.AlarmClock(Notifyloop,XBMC.RunScript(special://home/addons/%s/checknews.py,silent),%s,silent,loop)'%(AddonID, sleep))