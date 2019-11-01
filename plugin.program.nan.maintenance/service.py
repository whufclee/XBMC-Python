import xbmc, xbmcaddon
#################################################
AddonID        = 'plugin.program.nan.maintenance'
ADDON          =  xbmcaddon.Addon(id=AddonID)
clean_cache    =  ADDON.getSetting('cleancache')
internetcheck  =  ADDON.getSetting('internetcheck')
#################################################
if internetcheck == 'true':
    xbmc.executebuiltin('XBMC.AlarmClock(internetloop,XBMC.RunScript(special://home/addons/'+AddonID+'/connectivity.py,silent=true),00:01:00,silent,loop)')

if clean_cache == 'true':
    xbmc.executebuiltin('XBMC.AlarmClock(internetloop,XBMC.RunScript(special://home/addons/'+AddonID+'/cleancache.py,silent=true),12:00:00,silent,loop)')