# -*- coding: utf-8 -*-

# plugin.program.tbs
# Total Revolution Maintenance (c) by whufclee (info@totalrevolution.tv)

# Total Revolution Maintenance is licensed under a
# Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.

# You should have received a copy of the license along with this
# work. If not, see http://creativecommons.org/licenses/by-nc-nd/4.0.

import os
import xbmc

from koding     import dolog, Addon_Setting, Text_File
#---------------------------------------------------------------------------------------------------
AddonID          = 'plugin.program.tbs'
cachecheck       =  Addon_Setting('cleancache')
flashsplash      = '/flash/oemsplash.png'
newsplash        =  xbmc.translatePath('special://home/media/branding/Splash.png')
#---------------------------------------------------------------------------------------------------
if cachecheck == 'true':
    xbmc.executebuiltin('XBMC.AlarmClock(cleancacheloop,XBMC.RunScript(special://home/addons/%s/cleancache.py,silent=true),12:00:00,silent,loop)'%AddonID)

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

# Check uploaded shares to see if any have changed locally and need reuploading
# if not os.path.exists(runwizard):
#     dolog('### SERVICE - Checking my shares to see if they need updating on server')
#     xbmc.executebuiltin('RunScript(special://home/addons/%s/checknews.py,shares)'%AddonID)

# xbmc.executebuiltin('XBMC.AlarmClock(Shareloop,XBMC.RunScript(special://home/addons/%s/checknews.py,shares),12:00:00,silent,loop)'%AddonID)
# xbmc.log('### SLEEP: %s'%sleep)