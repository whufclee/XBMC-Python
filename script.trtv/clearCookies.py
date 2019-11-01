import shutil
import xbmc
import xbmcgui
import os

PROFILE = xbmc.translatePath('special://profile')
cookies = os.path.join(PROFILE, 'addon_data', 'script.trtv', 'cookies')
dialog  = xbmcgui.Dialog()

try:
	shutil.rmtree(cookies)
	dialog.ok('Cookies Reset','Your cookie files have now been removed. If you were previously having problems logging in you can try again now.')
except:
	dialog.ok('Nothing to delete','No cookie files are on the system to delete')