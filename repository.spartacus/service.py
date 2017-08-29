import xbmc
if not xbmc.getCondVisibility('System.HasAddon(script.openwindow)'):
    try:
        xbmc.executebuiltin('InstallAddon(script.openwindow)')
    except:
        pass