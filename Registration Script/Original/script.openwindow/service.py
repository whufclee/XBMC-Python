import xbmcplugin, xbmcgui, xbmc, xbmcaddon, os, sys, shutil

ADDONID                    = 'script.openwindow'
ADDON                      = xbmcaddon.Addon(ADDONID)
ADDONS                     = xbmc.translatePath(os.path.join('special://home','addons',''))
HOME                       = xbmc.translatePath('special://home/')
RestoreGUI                 = os.path.join(HOME,'userdata','addon_data','service.openelec.settings','restoregui')
RunWizard                  = os.path.join(HOME,'userdata','addon_data','service.openelec.settings','runwizard')

if os.path.exists(RunWizard):
    xbmc.executebuiltin('RunAddon(script.openwindow)')
    try:
        shutil.rmtree(RunWizard)
    except:
        pass

if os.path.exists(RestoreGUI):
    try:
        xbmc.executebuiltin('Skin.SetString(Branding,off)')
    except:
        pass
