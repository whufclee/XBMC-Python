# -*- coding: utf-8 -*-

# script.openwindow
# Startup Wizard (c) by Lee Randall (info@totalrevolution.tv)

# Total Revolution Startup Wizard is licensed under a
# Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.

# You should have received a copy of the license along with this
# work. If not, see http://creativecommons.org/licenses/by-nc-nd/4.0.

import os
import shutil
import xbmc
import xbmcaddon

from functions import *
from koding    import *

ADDON_ID         = 'script.openwindow'
ADDON_PATH       = xbmcaddon.Addon(ADDON_ID).getAddonInfo("path")
NON_REGISTERED   = xbmc.translatePath('special://profile/addon_data/script.openwindow/unregistered')
ADDONS           = xbmc.translatePath('special://home/addons')
AUTOEXEC         = xbmc.translatePath('special://home/userdata/autoexec.py')
ADDON_DATA       = xbmc.translatePath('special://profile/addon_data')
GUISETTINGS      = xbmc.translatePath('special://profile/guisettings.xml')
MEDIA            = xbmc.translatePath('special://home/media')
PACKAGES         = os.path.join(ADDONS, 'packages')
RUN_ORIG         = os.path.join(PACKAGES,'RUN_WIZARD')
RUN_WIZARD       = os.path.join(ADDON_DATA, ADDON_ID, 'RUN_WIZARD')
STARTUP_ORIG     = os.path.join(PACKAGES, 'STARTUP_WIZARD')
STARTUP_WIZARD   = os.path.join(ADDON_DATA, ADDON_ID, 'STARTUP_WIZARD')
INSTALL_ORIG     = os.path.join(PACKAGES, 'INSTALL_COMPLETE')
INSTALL_COMPLETE = os.path.join(ADDON_DATA, ADDON_ID, 'INSTALL_COMPLETE')
TBS              = os.path.join(ADDONS, 'plugin.program.tbs')
INTERNET_ICON    = os.path.join(ADDON_PATH,'resources','images','internet.png')
AUTOEXEC_PATH    = os.path.join(ADDON_PATH,'resources','autoexec.py')
#---------------------------------------------------------------------------------------------------
# Base domain checker
def My_Base():
    try:
        BASE = Addon_Setting('base')
        my_base = Open_URL(url=BASE)
        if my_base.startswith('This url could not be opened') or my_base == False:
            try:
                BASE = converthex(message=Open_URL('https://raw.githubusercontent.com/totalrevolution/testing/master/temp_files/BASE.txt'))
            except:
                dolog('Unable to access any valid base domain')
    except:
        pass
    Addon_Setting(setting='base',value=BASE)
#---------------------------------------------------------------------------------------------------
My_Base()

try:
    Check_License()
except:
    dolog(Last_Error())
    if not os.path.exists(NON_REGISTERED):
        os.makedirs(NON_REGISTERED)

if not os.path.exists(STARTUP_WIZARD) and not os.path.exists(RUN_WIZARD):
    try:
        os.makedirs(RUN_WIZARD)
    except:
        pass

# Check to see if the autoexec file exists
autoexec_exists = False
if os.path.exists(AUTOEXEC):
    contents = Text_File(AUTOEXEC,'r')
    if '# STARTUP WIZARD AUTOEXEC' in contents:
        autoexec_exists = True

# LEGACY CODE
if not autoexec_exists:
    if not os.path.exists(AUTOEXEC):
        shutil.copyfile(AUTOEXEC_PATH,AUTOEXEC)
    
    while xbmc.Player().isPlaying():
        xbmc.sleep(500)

    if not os.path.exists(PACKAGES):
        os.makedirs(PACKAGES)

    if os.path.exists(INSTALL_ORIG):
        try:
            os.makedirs(INSTALL_COMPLETE)
            shutil.rmtree(INSTALL_ORIG, ignore_errors=True)
        except Exception as e:
            xbmc.log(str(e))

    if os.path.exists(RUN_ORIG):
        try:
            os.makedirs(RUN_WIZARD)
            shutil.rmtree(RUN_ORIG, ignore_errors=True)
        except Exception as e:
            xbmc.log(str(e))

    if os.path.exists(STARTUP_ORIG):
        try:
            os.makedirs(STARTUP_WIZARD)
            shutil.rmtree(STARTUP_ORIG, ignore_errors=True)
        except Exception as e:
            xbmc.log(str(e))

    if os.path.exists(RUN_WIZARD):
        if os.path.exists(xbmc.translatePath('special://home/addons/script.openwindow/default.py')):
            xbmc.executebuiltin('RunScript(special://home/addons/script.openwindow/default.py,service)')
        elif os.path.exists(xbmc.translatePath('special://xbmc/addons/script.openwindow/default.py')):
            xbmc.executebuiltin('RunScript(special://xbmc/addons/script.openwindow/default.py,service)')

    elif os.path.exists(INSTALL_COMPLETE):
        if os.path.exists(xbmc.translatePath('special://home/addons/script.openwindow/functions.py')):
            xbmc.executebuiltin('RunScript(special://home/addons/script.openwindow/functions.py,service)')
        elif os.path.exists(xbmc.translatePath('special://xbmc/addons/script.openwindow/functions.py')):
            xbmc.executebuiltin('RunScript(special://xbmc/addons/script.openwindow/functions.py,service)')
