# -*- coding: utf-8 -*-

# script.openwindow
# Startup Wizard (c) by Lee Randall (info@totalrevolution.tv)

# Total Revolution Startup Wizard is licensed under a
# Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.

# You should have received a copy of the license along with this
# work. If not, see http://creativecommons.org/licenses/by-nc-nd/4.0.

import xbmc
import os

autoexec = xbmc.translatePath('special://profile/autoexec.py')
if os.path.exists(autoexec):
    readfile = open(autoexec,'r')
    contents = readfile.read()
    readfile.close()
    if '# STARTUP WIZARD AUTOEXEC' in contents:
        os.remove(autoexec)

if xbmc.getInfoLabel('Skin.String(Branding)') == 'off':
    xbmc.executebuiltin('RunScript(special://home/addons/script.openwindow/default.py,update)')