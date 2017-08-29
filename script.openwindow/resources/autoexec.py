# STARTUP WIZARD AUTOEXEC
import os
import xbmc
import xbmcgui
import xbmcaddon

ADDON_ID         = 'script.openwindow'
ADDON            = xbmcaddon.Addon(id=ADDON_ID)
BASE             = 'http://totalrevolution.tv/'
NON_REGISTERED   = xbmc.translatePath('special://profile/addon_data/script.openwindow/unregistered')
AUTOEXEC         = xbmc.translatePath('special://home/userdata/autoexec.py')
ADDON_DATA       = xbmc.translatePath('special://profile/addon_data')
RUN_WIZARD       = os.path.join(ADDON_DATA, ADDON_ID, 'RUN_WIZARD')
STARTUP_WIZARD   = os.path.join(ADDON_DATA, ADDON_ID, 'STARTUP_WIZARD')
INSTALL_COMPLETE = os.path.join(ADDON_DATA, ADDON_ID, 'INSTALL_COMPLETE')
#---------------------------------------------------------------------------------------------------
ADDON.setSetting(id='base', value=BASE)
xbmc.log('### AUTOEXEC RUNNING')
if not os.path.exists(STARTUP_WIZARD) and not os.path.exists(RUN_WIZARD):
    try:
        os.makedirs(RUN_WIZARD)
    except:
        pass
try:
    xbmc.executebuiltin('RunScript(special://home/addons/script.openwindow/functions.py,check_license)')
except:
    if not os.path.exists(NON_REGISTERED):
        os.makedirs(NON_REGISTERED)

if os.path.exists(RUN_WIZARD):
    if os.path.exists(xbmc.translatePath('special://home/addons/script.openwindow/default.py')):
        xbmc.executebuiltin('RunScript(special://home/addons/script.openwindow/default.py,service)')
    elif os.path.exists(xbmc.translatePath('special://xbmc/addons/script.openwindow/default.py')):
        xbmc.executebuiltin('RunScript(special://xbmc/addons/script.openwindow/default.py,service)')
    updates_running = 'true'
    xbmcgui.Window(10000).setProperty('TBS_Running', 'true')
    counter = 2
    while updates_running == 'true':
        xbmc.sleep(2000)
        updates_running = xbmcgui.Window(10000).getProperty('TBS_Running')
        xbmc.log('### TBS_RUNNING: %ss'%counter,2)
        counter += 2
    xbmc.sleep(1000)
    xbmc.log('### UPDATES COMPLETE, RELOADING SKIN',2)
    xbmc.executebuiltin('ReloadSkin')
    
elif os.path.exists(INSTALL_COMPLETE):
    if os.path.exists(xbmc.translatePath('special://home/addons/script.openwindow/functions.py')):
        xbmc.executebuiltin('RunScript(special://home/addons/script.openwindow/functions.py,service)')
    elif os.path.exists(xbmc.translatePath('special://xbmc/addons/script.openwindow/functions.py')):
        xbmc.executebuiltin('RunScript(special://xbmc/addons/script.openwindow/functions.py,service)')