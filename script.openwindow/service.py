# -*- coding: utf-8 -*-

# script.openwindow
# Startup Wizard (c) by Lee Randall (info@totalrevolution.tv)

# Total Revolution Startup Wizard is licensed under a
# Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.

# You should have received a copy of the license along with this
# work. If not, see http://creativecommons.org/licenses/by-nc-nd/4.0.

import xbmc
import os

from koding import Addon_Setting

AddonID = 'script.openwindow'
sleep   =  Addon_Setting('sleep')
Addon_Setting(addon_id='script.openwindow',setting='base',value='http://totalrevolution.xyz/')

autoexec = xbmc.translatePath('special://profile/autoexec.py')
if os.path.exists(autoexec):
    readfile = open(autoexec,'r')
    contents = readfile.read()
    readfile.close()
    if 'RUN_WIZARD' in contents:
        os.remove(autoexec)

xbmc.executebuiltin('RunScript(special://home/addons/script.openwindow/default.py,update)')

if sleep != '':
    xbmc.executebuiltin('XBMC.AlarmClock(Notifyloop,XBMC.RunScript(special://home/addons/script.openwindow/default.py,update),%s,silent,loop)'%sleep)